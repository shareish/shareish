from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

#Override default behavior of django-allauth
class SocialAccountAdapter(DefaultSocialAccountAdapter):
    #save the user on the djangoallauth socialaccount table AND on the user table
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.is_active = True
        data = sociallogin.account.extra_data
        if sociallogin.account.provider == 'google':
            user.first_name = data.get('given_name', '')
            user.last_name = data.get('family_name', '')
            username = data.get('given_name', '') + data.get('family_name', '') + sociallogin.account.uid
            user.username = username[:20]

        elif sociallogin.account.provider == 'mediawiki':
            user.first_name = data.get('firstname', '')
            user.last_name = data.get('lastname', '')
            username = data.get('firstname', 'User') + data.get('lastname', '') + sociallogin.account.uid
            user.username = username[:20]

        elif sociallogin.account.provider == 'openstreetmap':
            username = data.get('preferred_username', 'User') + sociallogin.account.uid
            user.username = username[:20]

        elif sociallogin.account.provider == 'microsoft':
            first_name = data.get('givenName', '') 
            last_name = data.get('surname', '')
            base_name = data.get('displayName', 'User')
            if(base_name == 'User'):
                user.username = base_name + sociallogin.account.uid
            else: 
                user.username = base_name
        elif sociallogin.account.provider == 'github':
            username = data.get("name", "User") + sociallogin.account.uid
            user.username = username[:20]
             
        user.save()

        Token.objects.get_or_create(user=user)

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