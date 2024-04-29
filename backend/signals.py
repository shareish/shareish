from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from mymap.models import User  # Importez votre modèle utilisateur personnalisé
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

@receiver(post_save, sender=SocialAccount)
def activate_user(sender, instance, created, **kwargs):
    if created:
        social_account_user_id = instance.user_id
        print("ID du SocialAccount created :", social_account_user_id)
        user = User.objects.get(id=social_account_user_id)
        user.is_active = True
        user.save()
        print("is_active put at True.")
