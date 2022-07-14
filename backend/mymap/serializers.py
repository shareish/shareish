from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from mymap.models import Item, ItemImage, User

class ItemSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=ItemImage.objects.all(), allow_null=True)
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'location', 'in_progress', 'item_type', 'category1', 'category2', 'category3', 'user', 'images']

class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all(), allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'items', 'description', 'image']

class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'password', 'username', 'first_name', 'last_name',)

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['image', 'item']