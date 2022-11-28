from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
    ActiveItemViewSet, ConversationViewSet, ItemImageViewSet, ItemViewSet,
    MapNameAndDescriptionViewSet, MessageViewSet, RecurrentItemViewSet, UserImageViewSet,
    UserItemViewSet, UserViewSet
)

router = DefaultRouter()
router.register("items", ItemViewSet, basename="items")
router.register("images", ItemImageViewSet, basename="images")
router.register("webusers", UserViewSet, basename="webusers")
router.register("conversations", ConversationViewSet, basename="conversations")
router.register(r'conversations/(?P<conversation_id>\d+)/messages', MessageViewSet,
                basename="messages")
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
    path('predictClass/', views.predictClass, name='predict_class'),
    path('notifications/', views.getNotifications, name='notifications'),
    path('item/<int:id>/image/first', views.getFirstItemImage, name='get_first_item_image'),
    path('item_image/<int:id>/image', views.getItemImage, name='get_item_image'),
    path('user_image/<int:id>/image', views.getUserImage, name='get_user_image'),
]
