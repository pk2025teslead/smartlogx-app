from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.db import connection
from django.contrib import messages
import json


def landing_page(request):
    """Public landing page"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/adminpanel/dashboard/')
        return redirect('/user/dashboard/')
    
    # Check if user is logged in via session (users_master)
    if request.session.get('user_master_id'):
        return redirect('/user/dashboard/')
    
    return render(request, 'public/landing.html')


@csrf_protect
@require_POST
def contact_submit(request):
    """Handle contact form submission"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        company = data.get('company', '').strip()
        message = data.get('message', '').strip()
        
        if not all([name, email, message]):
            return JsonResponse({'success': False, 'error': 'Please fill all required fields'})
        
        # Store contact inquiry in database
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO contact_inquiries (NAME, EMAIL, COMPANY, MESSAGE, CREATED_AT)
                VALUES (%s, %s, %s, %s, NOW())
            """, [name, email, company, message])
        
        return JsonResponse({'success': True, 'message': 'Thank you! We will get back to you soon.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
