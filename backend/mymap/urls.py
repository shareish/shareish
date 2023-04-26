from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
    ActiveItemViewSet, ConversationViewSet, ItemImageViewSet, ItemViewSet, MessageViewSet,
    RecurrentItemViewSet, UserImageViewSet, UserItemViewSet, UserViewSet, ItemCommentViewSet,
    UserMapExtraCategoriesViewSet
)

router = DefaultRouter()
router.register("items", ItemViewSet, basename='items')
router.register(r'items/(?P<item_id>\d+)/comments', ItemCommentViewSet, basename='items_comments')
router.register("images", ItemImageViewSet, basename='images')
router.register("webusers", UserViewSet, basename='webusers')
router.register("conversations", ConversationViewSet, basename='conversations')
router.register(r'conversations/(?P<conversation_id>\d+)/messages', MessageViewSet, basename='messages')
router.register("conversations/messages", MessageViewSet, basename='messages')
router.register("recurrents", RecurrentItemViewSet, basename='recurrents')
router.register("actives", ActiveItemViewSet, basename='actives')
router.register("user_items", UserItemViewSet, basename='user_items')
router.register("user_images", UserImageViewSet, basename='user_images')
router.register("map_ecats", UserMapExtraCategoriesViewSet, basename='map_ecats')

urlpatterns = [
    path("", include(router.urls)),
    path("address", views.get_address, name='get_address'),
    path("address/reverse", views.get_address_reverse, name='get_address_reverse'),
    path("predictClass/", views.predict_class, name='predict_class'),
    path("notifications/", views.get_notifications, name='notifications'),
    path("users/images/<int:userimage_id>", views.get_userimage, name='get_userimage'),
    path("users/images/<int:userimage_id>/base64", views.get_userimage_base64, name='get_userimage_base64'),
    path("items/images/<int:itemimage_id>", views.get_itemimage, name='get_itemimage'),
    path("items/<int:item_id>/images/base64", views.get_item_images_base64, name='get_item_images_base64'),
]
