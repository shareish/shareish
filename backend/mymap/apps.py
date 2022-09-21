from django.apps import AppConfig


class MymapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mymap'

    def ready(self):
        from djoser.views import UserViewSet
        from django.conf import settings
        from djoser.compat import get_user_email

        def perform_update(self, serializer):
            super(UserViewSet, self).perform_update(serializer)
            user = serializer.instance
            # should we send activation email after update?
            if settings.DJOSER['SEND_ACTIVATION_EMAIL'] and not user.is_active:
                context = {"user": user}
                to = [get_user_email(user)]
                settings.EMAIL.activation(self.request, context).send(to)

        UserViewSet.perform_update = perform_update
