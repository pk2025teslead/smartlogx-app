def handler(request):
    import json
    
    response_data = {
        'message': 'Simple Python function working!',
        'method': request.method if hasattr(request, 'method') else 'Unknown',
        'status': 'success'
    }
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response_data)
    }