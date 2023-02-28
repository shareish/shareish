from django.core.exceptions import ObjectDoesNotExist
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from .models import Conversation, Item, ItemImage, Message, User, UserImage


class ItemSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'location', 'in_progress', 'is_recurrent', 'startdate', 'enddate', 'item_type',
            'category1', 'category2', 'category3', 'user', 'images', 'hitcount'
        ]


class ItemImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = ItemImage
        fields = [
            'id', 'image', 'item', 'url'
        ]


class MapItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id', 'location'
        ]


class MapNameAndDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description'
        ]


class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all(), allow_null=True)
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'sign_in_date', 'homepage_url', 'facebook_url',
            'instagram_url', 'ref_location', 'use_ref_loc', 'dwithin_notifications', 'description', 'is_active',
            'mail_notif_freq_conversations', 'mail_notif_freq_events', 'mail_notif_freq_items', 'items', 'images'
        ]


class UserImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = UserImage
        fields = [
            'id', 'image', 'user', 'url'
        ]


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = [
            'id', 'email', 'password', 'username', 'first_name', 'last_name'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    unread_messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'name', 'owner', 'buyer', 'item', 'slug', 'lastmessagedate', 'unread_messages'
        ]

    def get_unread_messages(self, obj):
        request = self.context.get("request")
        if request is not None:
            return Message.objects.filter(conversation=obj, seen=False).exclude(user=request.user.id).count()
        return 0


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'content', 'user', 'date', 'seen'
        ]
