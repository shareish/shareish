from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework.authtoken.models import Token as RestToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from mymap.models import UserMapExtraCategories

User = get_user_model()

#Override default behavior of django-allauth
class SocialAccountAdapter(DefaultSocialAccountAdapter):
    #save the user on the djangoallauth socialaccount table AND on the user table
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        data = sociallogin.account.extra_data
        provider = sociallogin.account.provider
        uid = sociallogin.account.uid
        
        if provider == 'google':
            user.first_name = data.get('given_name', '')
            user.last_name = data.get('family_name', '')
            user.username = (data.get('given_name', '') + '.' + data.get('family_name', '') + '.' + uid)[:20]
        elif provider == 'mediawiki':
            user.first_name = data.get('firstname', '')
            user.last_name = data.get('lastname', '')
            user.username = (data.get('firstname', '') + '.' + data.get('lastname', '') + '.' + uid)[:20]
        elif provider == 'openstreetmap':
            user.username = (data.get('preferred_username', 'User') + uid)[:20]
        elif provider == 'microsoft':
            user.first_name = data.get('given_name', '')
            user.last_name = data.get('surname', '')
            display_name = data.get('display_name', 'User')
            user.username = (display_name + uid)[:20]
        elif provider == 'github':
            user.first_name = (data.get('name', 'User') + uid)[:20]
        
        user.is_active = True 
        user.last_login = timezone.now()
        user.save()

        if not user.map_ecats.exists():
            from .models import UserMapExtraCategory, UserMapExtraCategories
            for category_code, category_name in UserMapExtraCategories.choices:
                UserMapExtraCategory.objects.get_or_create(
                    user=user, 
                    category=category_code,
                    defaults={'selected': True}
                )
        
        RestToken.objects.get_or_create(user=user)

        return user

    #link the oidc account with an existing account 
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return 
        
        email = sociallogin.user.email
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                sociallogin.connect(request, user)
                if not user.is_active:
                    user.is_active = True 
                    user.save()
            except User.DoesNotExist:
                pass

    def on_authentication_error(self, request, provider, error=None, exception=None, extra_context=None):
        print(f"--- ERREUR AUTH ---")
        print(f"Provider: {provider}")
        print(f"Request: {request}")
        print(f"Error: {error}") # Ex: "invalid_grant" ou "access_denied"
        print(f"Exception: {exception}")
        print(f"Extra: {extra_context}")