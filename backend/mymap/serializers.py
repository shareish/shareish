import re

from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from .models import Conversation, Item, ItemImage, Message, User, UserImage

class UserImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = UserImage
        fields = [
            'id', 'image', 'user', 'url'
        ]


class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all(), allow_null=True)
    images = UserImageSerializer(many=True, allow_null=True, default=None)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'sign_up_date', 'homepage_url', 'facebook_url',
            'instagram_url', 'ref_location', 'use_ref_loc', 'dwithin_notifications', 'description', 'is_active',
            'mail_notif_freq_conversations', 'mail_notif_freq_events', 'mail_notif_freq_items', 'items', 'images'
        ]

    def validate(self, data):
        errors = {}

        # Check Facebook url
        if data.get('facebook_url') != "":
            facebook_regex = r"^((http[s]?:\/\/)|(www\.))(www\.)?facebook\.com\/.*$"
            if not re.match(facebook_regex, data.get('facebook_url')):
                errors['facebook_url'] = "Facebook profile/url is invalid."

        # Check Instagram url
        if data.get('instagram_url') != "":
            instagram_username_regex = r"([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
            if not re.match("^" + instagram_username_regex + "$", data.get('instagram_url')):
                instagram_regex = r"((http[s]?:\/\/)|(www\.))(www\.)?instagram\.com\/" + instagram_username_regex + "(\/|(\?=.+))?"
                if not re.match("^" + instagram_regex + "$", data.get('instagram_url')):
                    errors['instagram_url'] = "Instagram profile/url is invalid."

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return data


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = [
            'id', 'email', 'password', 'username', 'first_name', 'last_name'
        ]


class ItemSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    user = UserSerializer(allow_null=True, default=None)

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'location', 'in_progress', 'is_recurrent', 'creationdate', 'startdate',
            'enddate', 'type', 'category1', 'category2', 'category3', 'user_id', 'images', 'hitcount', 'user'
        ]

    def validate(self, data):
        errors = {}

        # Check categories uniqueness
        categories = []
        if 'category1' in data:
            categories.append(data['category1'])
        if 'category2' in data:
            if data['category2'] in categories:
                errors['category2'] = "Each category can only be used once."
            categories.append(data['category2'])
        if 'category3' in data:
            if data['category3'] != "" and data['category3'] in categories:
                errors['category3'] = "Each category can only be used once."

        # Check end date
        if data.get('startdate') != None and data.get('enddate') != None:
            if data.get('enddate') <= data.get('startdate'):
                errors['enddate'] = "The end date can't be earlier or equal to the start date."

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return data


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


class ConversationSerializer(serializers.ModelSerializer):
    unread_messages = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    starter = UserSerializer()
    item = ItemSerializer()

    class Meta:
        model = Conversation
        fields = [
            'id', 'item_id', 'starter_id', 'lastmessagedate', 'unread_messages', 'last_message',
            'starter', 'item'
        ]

    def get_unread_messages(self, obj):
        request = self.context.get('request')
        if request is not None:
            return Message.objects.filter(conversation=obj, seen=False).exclude(user=request.user.id).count()
        return 0

    def get_last_message(self, obj):
        request = self.context.get('request')
        if request is not None:
            last_message = Message.objects.filter(conversation=obj).last()
            if last_message is not None:
                return last_message.content
        return None


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(allow_null=True, default=None)

    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'content', 'user_id', 'date', 'seen', 'user'
        ]
