import re

from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from .models import Conversation, Item, ItemImage, Message, User, UserImage, ItemComment, ItemView, \
    UserMapExtraCategory, ConversationUser, Token, ScheduledAccountDeletion


class UserImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = UserImage
        fields = [
            'id', 'image', 'user', 'url'
        ]


class UserLightSerializer(serializers.ModelSerializer):
    images = UserImageSerializer(many=True, allow_null=True, default=None)
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'sign_up_date', 'homepage_url', 'facebook_url', 'instagram_url',
            'is_active', 'images', 'description',
            'is_disabled'
        ]



class UserMapExtraCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMapExtraCategory
        fields = [
            'id', 'category', 'selected', 'update_date', 'creation_date'
        ]

class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all(), allow_null=True)
    images = UserImageSerializer(many=True, allow_null=True, default=None)
    map_ecats = UserMapExtraCategorySerializer(many=True, allow_null=True, default=None)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'sign_up_date', 'homepage_url', 'facebook_url',
            'instagram_url', 'ref_location', 'use_ref_loc', 'dwithin_notifications', 'description', 'is_active',
            'mail_notif_freq_conversations', 'mail_notif_freq_events', 'mail_notif_freq_items', 'items', 'images',
            'map_ecats', 'save_item_viewing', 'is_disabled'
        ]

    def validate(self, data):
        errors = {}

        # Check Facebook url
        if 'facebook_url' in data and isinstance(data['facebook_url'], str) and data['facebook_url'] != "":
            facebook_regex = r"^((http[s]?:\/\/)|(www\.))(www\.)?facebook\.com\/.*$"
            if not re.match(facebook_regex, data['facebook_url']):
                errors['facebook_url'] = "Facebook profile/url is invalid."

        # Check Instagram url
        if 'instagram_url' in data and isinstance(data['instagram_url'], str) and data['instagram_url'] != "":
            instagram_username_regex = r"([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
            if not re.match("^" + instagram_username_regex + "$", data['instagram_url']):
                instagram_regex = r"((http[s]?:\/\/)|(www\.))(www\.)?instagram\.com\/" + instagram_username_regex + "(\/|(\?=.+))?"
                if not re.match("^" + instagram_regex + "$", data['instagram_url']):
                    errors['instagram_url'] = "Instagram profile/url is invalid."

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return data

    def to_representation(self, obj):
        rep = super(UserSerializer, self).to_representation(obj)
        new_rep = rep.copy()

        if 'request' in self.context:
            columns = self.context['request'].query_params.getlist('columns[]')
            if len(columns) > 0:
                for column in rep:
                    if column not in columns:
                        new_rep.pop(column)

        return new_rep

    



        
class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = [
            'id', 'email', 'password', 'username', 'first_name', 'last_name'
        ]


class ItemSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    user = UserLightSerializer(allow_null=True, default=None)
    comments_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'location', 'is_recurrent', 'creationdate', 'startdate', 'enddate', 'type',
            'category1', 'category2', 'category3', 'visibility', 'user_id', 'images', 'views_count', 'user',
            'closed_reason', 'is_closed', 'comments_count'
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
        if data.get('startdate') is not None and data.get('enddate') is not None:
            if data.get('enddate') <= data.get('startdate'):
                errors['enddate'] = "The end date can't be earlier or equal to the start date."

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return data

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_views_count(self, obj):
        return obj.views.count()


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


class ConversationUserSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()

    class Meta:
        model = ConversationUser
        fields = [
            'id', 'conversation_id', 'user_id', 'joining_date', 'updated_date', 'created_date', 'user'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    unread_messages = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    item = ItemSerializer()
    users = ConversationUserSerializer(many=True, allow_null=True, default=None)

    class Meta:
        model = Conversation
        fields = [
            'id', 'item_id', 'is_closed', 'lastmessagedate', 'unread_messages', 'last_message', 'item', 'users'
        ]

    def get_unread_messages(self, obj):
        request = self.context.get('request')
        if request is not None:
            return Message.objects.filter(conversation=obj, seen=False).exclude(user=request.user.id).count()
        return 0

    def get_last_message(self, obj):
        request = self.context.get('request')
        if request is not None:
            last_message = Message.objects.filter(conversation=obj).first()
            if last_message is not None:
                return last_message.content
        return None


class MessageSerializer(serializers.ModelSerializer):
    user = UserLightSerializer(allow_null=True, default=None)

    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'content', 'user_id', 'date', 'seen', 'user'
        ]

        
class ItemCommentSerializer(serializers.ModelSerializer):
    user = UserLightSerializer(allow_null=True, default=None)
    item = ItemSerializer(allow_null=True, default=None)

    class Meta:
        model = ItemComment
        fields = [
            'id', 'content', 'creationdate', 'item_id', 'user_id', 'item', 'user'
        ]


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(allow_null=True, default=None)

    class Meta:
        model = Token
        fields = [
            'id', 'user_id', 'token', 'action', 'used_at', 'lifespan', 'updated_at', 'created_at', 'user'
        ]


class ScheduledAccountDeletionSerializer(serializers.ModelSerializer):
    user = UserSerializer(allow_null=True, default=None)

    class Meta:
        model = ScheduledAccountDeletion
        fields = [
            'id', 'interval', 'request_date', 'user', 'user_id', 'is_due'
        ]

