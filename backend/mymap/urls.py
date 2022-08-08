from django.urls import path, include
from . import views
from .views import ItemViewSet, ItemImageViewSet, UserViewSet, ConversationViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("items", ItemViewSet, basename="items")
router.register("images", ItemImageViewSet, basename="images")
router.register("users", UserViewSet, basename="users")
router.register("conversations", ConversationViewSet, basename="conversations")
router.register("messages", MessageViewSet, basename="messages")

urlpatterns = [
    path('', include(router.urls)),
    path('request/', views.searchItem, name='search_item'),
    path('address/', views.getAddress, name='get_address')
]