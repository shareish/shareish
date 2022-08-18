from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from mymap.models import Item, ItemImage, User, Conversation, Message, UserImage

class ItemSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=ItemImage.objects.all(), allow_null=True)
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'location', 'in_progress', 'is_recurrent', 'startdate', 'enddate', 'item_type', 'category1', 'category2', 'category3', 'user', 'images']

class MapItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'location']

class MapNameAndDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']

class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all(), allow_null=True)
    image = serializers.PrimaryKeyRelatedField(many=True, queryset=UserImage.objects.all(), allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'items', 'description', 'image']

class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id', 'email', 'password', 'username', 'first_name', 'last_name', )

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'image', 'user']

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'image', 'item']

class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all(), allow_null=True)
    class Meta:
        model = Conversation
        fields = ['id', 'name', 'owner', 'buyer', 'item', 'slug', 'messages']
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content', 'user', 'date']