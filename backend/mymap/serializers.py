from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from mymap.models import Item, ItemImage, User, Conversation, Message

class ItemSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=ItemImage.objects.all(), allow_null=True)
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'location', 'in_progress', 'is_recurrent', 'item_type', 'category1', 'category2', 'category3', 'user', 'images']

class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all(), allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'items', 'description', 'image']

class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id', 'email', 'password', 'username', 'first_name', 'last_name', )

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'image', 'item']

class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all(), allow_null=True)
    class Meta:
        model = Conversation
        fields = ['id', 'name', 'owner', 'buyer', 'messages']
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content', 'user', 'date']