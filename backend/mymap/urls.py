from django.urls import path, include
from . import views
from .views import BarterViewSet, BarterImageViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("barters", BarterViewSet, basename="barters")
router.register("images", BarterImageViewSet, basename="images")
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
]