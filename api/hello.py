from django.http import JsonResponse

def handler(request):
    return JsonResponse({
        'message': 'Hello from Vercel!',
        'status': 'working'
    })