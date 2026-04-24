from django.conf import settings 

def site_settings(request):
    return {
        'APP_URL': settings.APP_URL,
    }