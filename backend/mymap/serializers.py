from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from mymap.models import Conversation, Item, ItemImage, Message, User, UserImage


class ItemSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'location', 'in_progress', 'is_recurrent',
            'startdate', 'enddate', 'item_type', 'category1', 'category2', 'category3',
            'user', 'images'
        ]


class MapItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'location']


class MapNameAndDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']


class ItemImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = ItemImage
        fields = ['id', 'image', 'item', 'url']


class UserImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = UserImage
        fields = ['id', 'image', 'user', 'url']


class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Item.objects.all(), allow_null=True
        )
    image = serializers.StringRelatedField(
        many=True
        )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'homepage_url', 'facebook_url', 'instagram_url',
            'items', 'description', 'image', 'is_active',
        ]


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id', 'email', 'password', 'username', 'first_name', 'last_name',)


class ConversationSerializer(serializers.ModelSerializer):
    unread_messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'owner', 'buyer', 'item', 'slug', 'unread_messages']

    def get_unread_messages(self, obj):
        user = self.context.get("request").user
        return Message.objects.filter(conversation=obj, seen=False).exclude(
            user=user.id).count()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content', 'user', 'date', 'seen']
