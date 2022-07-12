from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from mymap.models import Barter, BarterImage, User

class BarterSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=BarterImage.objects.all(), allow_null=True)
    class Meta:
        model = Barter
        fields = ['id', 'name', 'description', 'location', 'in_progress', 'barter_type', 'category1', 'category2', 'category3', 'user', 'images']

class UserSerializer(serializers.ModelSerializer):
    barters = serializers.PrimaryKeyRelatedField(many=True, queryset=Barter.objects.all(), allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'barters']

class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'password', 'username', 'first_name', 'last_name',)

class BarterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterImage
        fields = ['image', 'barter']