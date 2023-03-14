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
router.register(r'conversations/(?P<conversation_id>\d+)/messages', MessageViewSet, basename="messages")
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
    path('craft/', views.craft, name='craft'),
    path('notifications/', views.getNotifications, name='notifications'),
    path('items/<int:item_id>/has_images', views.itemHasImage, name='item_has_images'),
    path('items/<int:item_id>/images/first', views.getItemFirstImage, name='get_item_first_image'),
    path('items/<int:new_item_id>/images/republish_from/<int:parent_item_id>', views.republishItemImagesFromItem, name='republish_item_images_from_item'),
    path('items/<int:item_id>/increase_hitcount', views.increaseHitcountItem, name='increase_item_hitcount'),
    path('items/images/<int:itemimage_id>', views.getItemImage, name='get_item_image'),
    path('users/images/<int:userimage_id>', views.getUserImage, name='get_user_image'),
]
