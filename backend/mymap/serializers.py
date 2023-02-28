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


class ItemImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = ItemImage
        fields = [
            'id', 'image', 'item', 'url'
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
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'name', 'owner', 'buyer', 'item', 'slug', 'lastmessagedate', 'unread_messages', 'last_message'
        ]

    def get_unread_messages(self, obj):
        request = self.context.get("request")
        if request is None:
            return 0

        user = request.user
        return Message.objects.filter(conversation=obj, seen=False).exclude(
            user=user.id).count()

    def get_last_message(self, obj):
        try:
            last_message = Message.objects.filter(conversation=obj).latest('date')
            return MessageSerializer(last_message).data
        except ObjectDoesNotExist:
            return None


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'content', 'user', 'date', 'seen'
        ]
