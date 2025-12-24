from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db import connection
from django.contrib.auth.hashers import check_password
from .models import UserProfile


def get_user_master_by_email(email):
    """Get user from users_master table by email"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, 
                   PASSWORD, IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT
            FROM users_master
            WHERE EMAIL = %s
        """, [email])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
    return None


def get_user_master_by_emp_id(emp_id):
    """Get user from users_master table by EMP_ID"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, 
                   PASSWORD, IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT
            FROM users_master
            WHERE EMP_ID = %s
        """, [emp_id])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
    return None


@csrf_protect
def login_view(request):
    """Login view with raw SQL validation for users_master"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/adminpanel/dashboard/')
        return redirect('/logs/dashboard/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # First, try to authenticate with Django's built-in auth (for admin users)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check user status using raw SQL
            user_data = UserProfile.get_user_by_credentials_raw(username, password)
            
            if user_data and user_data['is_active'] and user_data['profile_active']:
                login(request, user)
                
                # Role-based redirect
                if user.is_staff:
                    return redirect('/adminpanel/dashboard/')
                else:
                    return redirect('/logs/dashboard/')
            else:
                messages.error(request, 'Your account has been deactivated. Please contact administrator.')
        else:
            # Try to authenticate against users_master table
            # Username could be EMP_ID or EMAIL
            user_master = get_user_master_by_emp_id(username)
            if not user_master:
                user_master = get_user_master_by_email(username)
            
            if user_master:
                # Verify password
                if check_password(password, user_master['PASSWORD']):
                    # Check if first login
                    if user_master['IS_FIRST_LOGIN']:
                        # Store user ID in session and redirect to password change
                        request.session['first_login_user_id'] = user_master['ID']
                        messages.info(request, 'Please change your password to continue.')
                        return redirect('adminpanel:change_password')
                    else:
                        # Store user_master ID in session for user panel access
                        request.session['user_master_id'] = user_master['ID']
                        request.session['user_master_name'] = user_master['EMP_NAME']
                        request.session['user_master_role'] = user_master['ROLE']
                        messages.success(request, f'Welcome back, {user_master["EMP_NAME"]}!')
                        # Redirect to user dashboard
                        return redirect('userpanel:dashboard')
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logout view"""
    # Clear user_master session data
    if 'user_master_id' in request.session:
        del request.session['user_master_id']
    if 'user_master_name' in request.session:
        del request.session['user_master_name']
    if 'user_master_role' in request.session:
        del request.session['user_master_role']
    
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/accounts/login/')


def register_view(request):
    """Registration view (optional)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'accounts/register.html')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create user profile
        UserProfile.objects.create(user=user)

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('/accounts/login/')

    return render(request, 'accounts/register.html')
