from django.urls import path, include
from . import views
from .views import ActiveItemViewSet, ItemViewSet, ItemImageViewSet, UserViewSet, ConversationViewSet, MessageViewSet, RecurrentItemViewSet, ActiveItemViewSet, UserItemViewSet, UserImageViewSet, MapNameAndDescriptionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("items", ItemViewSet, basename="items")
router.register("images", ItemImageViewSet, basename="images")
router.register("webusers", UserViewSet, basename="webusers")
router.register("conversations", ConversationViewSet, basename="conversations")
router.register("messages", MessageViewSet, basename="messages")
router.register("recurrents", RecurrentItemViewSet, basename="recurrents")
router.register("actives", ActiveItemViewSet, basename="actives")
router.register("user_items", UserItemViewSet, basename='user_items')
router.register("user_image", UserImageViewSet, basename="user_image")
router.register("mapnd", MapNameAndDescriptionViewSet, basename="mapnd")

urlpatterns = [
    path('', include(router.urls)),
    path('requestFilter/', views.searchItemFilter, name='search_item_filter'),
    path('address/', views.getAddress, name='get_address'),
    path('requestItems/', views.searchItems, name='search_items'),
    path('predictClass/', views.predictClass, name='predict_class')
]