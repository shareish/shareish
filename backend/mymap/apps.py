from django.apps import AppConfig
from geopy.geocoders import Nominatim
from rest_framework.response import Response
from rest_framework import status

locator = Nominatim(user_agent="shareish")
LOCATION_PREFIX = "SRID=4326;POINT"


class MymapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mymap'
    
    def ready(self):
        from djoser.views import UserViewSet
        from django.conf import settings
        from djoser.compat import get_user_email
        import signals

        def perform_update(self, serializer):
            request = self.request
            user = self.request.user
            instance = self.get_object()
            if 'ref_location' in request.data:
                address = request.data['ref_location']
                if address != '' and address is not None and not address.startswith(LOCATION_PREFIX):
                    geoloc = locator.geocode(address)
                    if geoloc is not None:
                        request.data['ref_location'] = "{} ({} {})".format(
                            LOCATION_PREFIX,
                            str(geoloc.latitude),
                            str(geoloc.longitude)
                        )
                        #we will use by default the reference location for computing distance for notifications
                        request.data['use_ref_loc'] = True
                    else:
                        return Response(
                            {"message": "Bad location."}, status=status.HTTP_400_BAD_REQUEST
                        )
            ##partial=True? for new user?
            if user.is_active:
                partial=True
            else:
                partial=False
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                super(UserViewSet, self).perform_update(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, headers=headers)
                
            user = serializer.instance
            # should we send activation email after update?
            if settings.DJOSER['SEND_ACTIVATION_EMAIL'] and not user.is_active:
                context = {"user": user}
                to = [get_user_email(user)]
                settings.EMAIL.activation(self.request, context).send(to)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        UserViewSet.perform_update = perform_update

        # Start mail scheduler
        from .mail import start_mail_scheduler
        start_mail_scheduler()

        from .scheduler import start_scheduler
        start_scheduler()

