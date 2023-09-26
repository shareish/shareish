import base64
import json
import re
from datetime import datetime


from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import Q, Count
from django.http import FileResponse, JsonResponse, QueryDict
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token as RestToken
from rest_framework.authtoken.views import ObtainAuthToken

from .filters import ItemTypeFilterBackend, ConversationContentFilterBackend, ItemCategoryFilterBackend, \
    ActiveItemFilterBackend, UserItemFilterBackend, ConversationSelectedCategoryFilterBackend, ItemViewFilterBackend, \
    ItemAvailabilityFilterBackend, ItemLocationFilterBackend, ItemMinCreationdateFilterBackend, \
    ItemMapBoundsFilterBackend, UserDisabledFilterBackend, ItemVisibilityFilterBackend, ItemClosedReasonFilterBackend, \
    ItemUserDisabledFilterBackend
from .functions import verif_location
from .mail import send_mail_recover_account, send_mail_start_delete_account_process
from .models import Conversation, Item, ItemImage, Message, UserImage, ItemComment, ItemView, UserMapExtraCategory, \
    ConversationUser, Token, ScheduledAccountDeletion

from rest_framework import filters, viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .pagination import ActivePaginationClass, MessagePaginationClass
from .serializers import (
    ItemSerializer, UserSerializer, UserLightSerializer, ItemImageSerializer, ConversationSerializer, MessageSerializer,
    UserImageSerializer, ItemCommentSerializer, UserMapExtraCategorySerializer, TokenSerializer
)
from .permissions import IsOwnerProfileOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated

from .ai import findClass

from geopy.geocoders import Nominatim

User = get_user_model()
locator = Nominatim(user_agent='shareish')


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all().annotate(comments_count=Count('comments'), views_count=Count('views'))
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
    search_fields = ['name', 'description']
    ordering_fields = '__all__'

    def retrieve(self, request, *args, **kwargs):
        # Solution to view ended item, maybe temporary
        # Previously, used ?kind=user but only owner could see the item, not cool
        pk = int(kwargs['pk'])
        try:
            instance = Item.objects.get(pk=pk)
            serializer = self.get_serializer(instance)

            if 'view_date' in request.query_params and request.user.save_item_viewing:
                try:
                    ItemView.objects.create(item=instance, user=request.user,
                                            view_date=request.query_params['view_date'])
                except IntegrityError:
                    # Item already viewed
                    pass

            if instance.visibility == Item.Visibility.DRAFT and request.user != instance.user and not request.user.is_staff:
                return Response({'key': 'ITEM_DOESNT_EXIST'}, status=status.HTTP_404_NOT_FOUND)

            if instance.is_closed:
                if instance.user != request.user:
                    return Response({'key': 'ITEM_IS_CLOSED'}, status=status.HTTP_403_FORBIDDEN)

            if instance.user.is_disabled:
                return Response({'key': 'ITEM_DOESNT_EXIST'}, status=status.HTTP_404_NOT_FOUND)
            
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response({'key': 'ITEM_DOESNT_EXIST'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        result = verif_location(request.data['location'])
        if 'success' in result:
            request.data['location'] = result['success']
        else:
            return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        item = serializer.save(user=self.request.user)
        if item.location is not None:
            if item.type != "EV":
                from .mail import send_mail_notif_new_single_item_published
                send_mail_notif_new_single_item_published(item, self.request.user)
            else:
                from .mail import send_mail_notif_new_single_event_published
                send_mail_notif_new_single_event_published(item, self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.user == request.user:
            result = verif_location(request.data['location'])
            if 'success' in result:
                request.data['location'] = result['success']
            else:
                return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, headers=headers)
            return Response({'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'key': 'NOT_ITEM_OWNER'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'key': 'NOT_ITEM_OWNER'}, status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        instance.delete()


class RecurrentItemViewSet(ItemViewSet):
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        return Item.objects.filter(is_recurrent=True, user=self.request.user)


class ActiveItemViewSet(ItemViewSet):
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter, ActiveItemFilterBackend, ItemCategoryFilterBackend,
        ItemTypeFilterBackend, ItemViewFilterBackend, ItemAvailabilityFilterBackend, ItemLocationFilterBackend,
        ItemMinCreationdateFilterBackend, ItemMapBoundsFilterBackend, ItemVisibilityFilterBackend, ItemClosedReasonFilterBackend, ItemUserDisabledFilterBackend
    ]
    search_fields = ['name', 'description', 'user__username']
    pagination_class = ActivePaginationClass

    def paginate_queryset(self, queryset):
        if 'page' in self.request.query_params:
             return super().paginate_queryset(queryset)
        return None


class UserItemViewSet(ItemViewSet):
    filter_backends = [filters.OrderingFilter, UserItemFilterBackend]


class ItemCommentViewSet(viewsets.ModelViewSet):
    serializer_class = ItemCommentSerializer

    def get_queryset(self):
        if 'item_id' in self.kwargs:
            item = Item.objects.get(pk=self.kwargs['item_id'])
            return ItemComment.objects.filter(item=item)
        else:
            return ItemComment.objects.all()

    def create(self, request, *args, **kwargs):
        if 'item_id' in self.kwargs:
            try:
                item = Item.objects.get(pk=self.kwargs['item_id'])
                if not item.is_closed:
                    serializer = self.get_serializer(data=request.data)
                    if serializer.is_valid():
                        self.perform_create(serializer)
                        headers = self.get_success_headers(serializer.data)
                        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                    return Response({'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                return Response("You cannot post a comment on a closed item.", status=status.HTTP_403_FORBIDDEN)
            except Item.DoesNotExist:
                return Response("This item does not exist.", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("You must provide and item id to post a comment.", status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        try:
            item = Item.objects.get(pk=self.kwargs['item_id'])
            serializer.save(user=self.request.user, item=item)
        except Item.DoesNotExist:
            return Response("This item does not exist.", status=status.HTTP_404_NOT_FOUND)


class ItemImageViewSet(viewsets.ViewSet):
    def create(self, request):
        # Remove all previous images if any (edition case)
        ItemImage.objects.filter(item_id=request.POST['item_id']).delete()

        # Add all news images received (add/edition cases)
        item = Item.objects.get(pk=request.POST['item_id'])
        images = request.FILES.getlist('images')
        for i in range(0, len(images)):
            new_image = ItemImage(image=images[i], position=i, item=item)
            new_image.save()
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            image = ItemImage.objects.get(pk=pk)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemImageSerializer(image)
        return Response(serializer.data)



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
    filter_backends = [UserDisabledFilterBackend]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (request.user.id == instance.id):
            serializer = UserSerializer(instance)
        else:
            serializer = UserLightSerializer(instance)
        return Response(serializer.data)
    
    def get_instance(self):
        return self.request.user

    @action(['get', 'put', 'patch'], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        result = verif_location(request.data['ref_location'])
        if 'success' in result:
            request.data['ref_location'] = result['success']
        else:
            return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_instance()

        data = request.data

        if 'map_ecats' in data:
            for map_ecat in data['map_ecats']:
                try:
                    instance = UserMapExtraCategory.objects.get(user=request.user, category=map_ecat['category'])
                    instance.selected = map_ecat['selected']
                    instance.save()
                except UserMapExtraCategory.DoesNotExist:
                    return Response(
                        "A map extra category isn't correctly linked to your account. Can't process to save.",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except UserMapExtraCategory.MultipleObjectsReturned:
                    return Response(
                        "Multiple occurrences of an map extra category detected on your account. Can't process to save.",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            del data['map_ecats']
            if len(data) == 0:
                return Response(status=status.HTTP_200_OK)

        if 'ref_location' in data:
            result = verif_location(data['ref_location'])
            if 'success' in result:
                data['ref_location'] = result['success']
            else:
                return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)

        if 'instagram_url' in data:
            instagram_username_regex = r"([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
            if re.match("^" + instagram_username_regex + "$", data['instagram_url']):
                data['instagram_url'] = "https://www.instagram.com/" + data['instagram_url'] + "/"

        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        return Response({'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserImageViewSet(viewsets.ViewSet):
    def create(self, request):
        user = User.objects.get(pk=request.POST['user_id'])
        image = request.FILES.get('image')
        new_image = UserImage(image=image, user=user)
        new_image.save()
        serialized_image = UserImageSerializer(new_image)
        return Response(serialized_image.data, status=status.HTTP_201_CREATED)


class UserMapExtraCategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = UserMapExtraCategorySerializer
    queryset = UserMapExtraCategory.objects.all()


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [ConversationContentFilterBackend, ConversationSelectedCategoryFilterBackend]

    def get_queryset(self):
        return Conversation.objects.filter(users__user=self.request.user)

    def create(self, request, *args, **kwargs):

        data = request.data
        try:
            item = Item.objects.get(pk=data['item_id'])
        except Item.DoesNotExist:
            return Response("This item does not exist.", status=status.HTTP_400_BAD_REQUEST)

        if item.user_id == request.user.id:
            return Response("You cannot start a conversation on an item you own.", status=status.HTTP_403_FORBIDDEN)

        if item.is_closed:
            return Response("You cannot start a conversation on a closed item.", status=status.HTTP_403_FORBIDDEN)

        item_conversations_containing_user = Conversation.objects.filter(users__user=request.user, item=item)
        if len(item_conversations_containing_user) > 0:
            # User is part of at least one conversation for this item
            item_conversations_containing_user_still_valid = item_conversations_containing_user.filter(users__user=item.user)
            if len(item_conversations_containing_user_still_valid) == 0:
                # None of the conversations selected above still have both the current user and the item owner in it
                # Create a new conversation with the item owner for this item
                return self.create_conversation(item, [request.user, item.user])
            elif len(item_conversations_containing_user_still_valid) == 1:
                # Normal existing conversation case, one conversation is still valid for the combo user/item owner/item
                # Return the conversation id straightforward
                return Response(item_conversations_containing_user_still_valid.first().id, status=status.HTTP_200_OK)
            else:
                # Shouldn't happen, more than one conversation for the combo user/item owner/item
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # User is not member of any conversations for this item
            # Create a new conversation with the item owner for this item
            return self.create_conversation(item, [request.user, item.user])

    @staticmethod
    def create_conversation(item, users):
        # Verify that the item is still active
        if item.enddate is not None and item.enddate < datetime.now(timezone.utc):
            return Response("You cannot start a conversation on this item, it has already ended.", status=status.HTTP_400_BAD_REQUEST)

        # Create the conversation
        conversation = Conversation.objects.create(item=item)

        # Add users to the conversation
        for user in users:
            ConversationUser.objects.create(conversation=conversation, user=user)

        return Response(conversation.id, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    pagination_class = MessagePaginationClass

    def get_queryset(self):
        if 'conversation_id' in self.kwargs:
            conversation = Conversation.objects.get(pk=self.kwargs['conversation_id'])
            return Message.objects.filter(conversation=conversation)
        else:
            return Message.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user.id == request.user.id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("You can't delete a message that do not belongs to you.", status=status.HTTP_403_FORBIDDEN)


class CustomLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        if 'authValue' in request.data and 'password' in request.data:
            auth_value = request.data['authValue']
            try:
                user = User.objects.get(email=auth_value)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(username=auth_value)
                except User.DoesNotExist:
                    return Response({'key': 'ACCOUNT_DOESNT_EXIST'}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_active:
                if not user.is_disabled:
                    if user.check_password(request.data['password']):
                        # Update user's last login date
                        user.last_login = timezone.now()
                        user.save()

                        # Generate auth token
                        token, created = RestToken.objects.get_or_create(user=user)
                        return Response({
                            'token': token.key,
                            'id': user.pk
                        })
                    return JsonResponse({'key': 'INVALID_PASSWORD'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        schedule = ScheduledAccountDeletion.objects.get(user=user)
                        if schedule.due_date() > timezone.now():
                            days_left = (schedule.due_date() - timezone.now()).days
                        else:
                            days_left = 0
                        return Response({'key': 'SCHEDULED_DELETION_ACCOUNT', 'days_left': days_left}, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        print(e)
                        return Response({'key': 'DISABLED_ACCOUNT'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'key': 'NOT_VALIDATED_YET'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'key': 'MISSING_INTERNAL_FIELDS'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_address_reverse(request):
    if request.method == 'POST':
        if isinstance(request.data, QueryDict):
            coords = request.data['SRID'].split(' ')[1:]
            latitude = float(coords[0][1:])
            longitude = float(coords[1][:-1])
        elif isinstance(request.data, dict) and 'latitude' in request.data and 'longitude' in request.data:
            latitude = float(request.data['latitude'])
            longitude = float(request.data['longitude'])
        else:
            return Response("Couldn't find location.", status=status.HTTP_400_BAD_REQUEST)
        try:
            location = locator.reverse((latitude, longitude), exactly_one=True)
            if location is not None:
                return Response(location.address, status=status.HTTP_200_OK)
            return Response("Couldn't find location.", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Third party geolocation service did not work properly.", status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def get_address(request):
    if request.method == 'POST':
        try:
            location = locator.geocode(request.POST['address'])
            if location is not None:
                return Response((location.longitude, location.latitude), status=status.HTTP_200_OK)
            return Response("Couldn't find location.", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Third party geolocation service did not work properly.", status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def predict_class(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            return JsonResponse(findClass(image), status=status.HTTP_200_OK, safe=False)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    user = request.user

    if request.method == 'GET':
        conversation_unread_messages_count = Message.objects.filter(
            ~Q(user=user), Q(seen=False), Q(conversation__users__user=user)
        ).count()
        return Response(conversation_unread_messages_count, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        try:
            conversation = Conversation.objects.get(pk=request.data['conversation_id'])
            if not conversation.users.filter(user=user).exists():
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Set all messages sent by other user as seen by current user for this conversation
            Message.objects.filter(
                Q(conversation__id=request.data['conversation_id']),
                ~Q(user=user),
                Q(date__lte=request.data['last_message_date']),
                Q(seen=False)
            ).update(seen=True)

            conversation_unread_messages_count = Message.objects.filter(
                Q(conversation__id=request.data['conversation_id']),
                ~Q(user=user),
                Q(seen=False)
            ).count()

            # Return unread messages count for all conversations
            return Response(conversation_unread_messages_count, status=status.HTTP_200_OK)
        except Conversation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'DELETE'])
@permission_classes([AllowAny])
def get_userimage(request, userimage_id):
    if request.method == 'GET':
        try:
            image = UserImage.objects.get(pk=userimage_id)
            return FileResponse(open(image.path, 'rb'))
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            try:
                user_image = UserImage.objects.get(pk=userimage_id)
                if user_image.user_id == request.user.id:
                    user_image.delete()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({'key': 'NOT_IMAGE_OWNER'}, status=status.HTTP_403_FORBIDDEN)
            except UserImage.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({'key': 'MUST_BE_AUTHENTICATED'}, status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_userimage_base64(request, userimage_id):
    if request.method == 'GET':
        try:
            userimage = UserImage.objects.get(pk=userimage_id)
            response = {
                "name": str(userimage.image.name),
                "base64_url": "data:image/png;base64," + str(
                    base64.b64encode(userimage.image.file.read()).decode("utf-8"))
            }
            return Response(json.dumps(response), status=status.HTTP_200_OK)
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_itemimage(request, itemimage_id):
    if request.method == 'GET':
        try:
            image = ItemImage.objects.get(pk=itemimage_id)
            return FileResponse(open(image.path, 'rb'))
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_item_images_base64(request, item_id):
    if request.method == 'GET':
        item_images = ItemImage.objects.filter(item_id=item_id)
        images = []
        for item_image in item_images:
            images.append({
                "name": str(item_image.image.name),
                "base64_url": "data:image/png;base64," + str(
                    base64.b64encode(item_image.image.file.read()).decode("utf-8"))
            })
        return Response(json.dumps(images), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def close_all_conversations_from_item(request, item_id):
    if request.method == 'PATCH':
        item = Item.objects.get(pk=item_id)
        if item.user_id == request.user.id:
            Conversation.objects.filter(item_id=item_id).update(is_closed=True)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("You are not the owner of this item.", status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_user(request, user_id):
    if request.method == 'POST':
        if 'password' in request.data:
            if user_id == request.user.id or request.user.is_staff:
                # Retrieve the user to modify
                try:
                    user = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    return Response({'key': 'ACCOUNT_DOESNT_EXIST'}, status=status.HTTP_404_NOT_FOUND)

                # Verify that the password entered is correct
                if not user.check_password(request.data['password']):
                    return Response({'key': 'INVALID_PASSWORD'}, status=status.HTTP_400_BAD_REQUEST)

                if not user.is_disabled:
                    try:
                        with transaction.atomic():
                            # Disable the user
                            user.is_disabled = True
                            user.save()

                            # Closing 1to1 conversations where user was part of
                            conversations_user = ConversationUser.objects.filter(user=user, conversation__max_users=2)
                            for conversation_user in conversations_user:
                                conversation_to_close = conversation_user.conversation
                                conversation_to_close.is_closed = True
                                conversation_to_close.save()

                            return Response(status=status.HTTP_200_OK)
                    except:
                        return Response({'key': 'INTERNAL_ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'key': 'ACCOUNT_ALREADY_DISABLED'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'key': 'NOT_ACCOUNT_OWNER'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'key': 'MISSING_INTERNAL_FIELDS'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_send_delete_confirmation(request, user_id):
    if request.method == 'POST':
        if 'password' in request.data:
            if user_id == request.user.id or request.user.is_staff:
                # Retrieve the user to contact
                try:
                    user = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    return JsonResponse({'key': 'ACCOUNT_DOESNT_EXIST'}, status=status.HTTP_404_NOT_FOUND)

                # Verify that the password entered is correct
                if not user.check_password(request.data['password']):
                    return JsonResponse({'key': 'INVALID_PASSWORD'}, status=status.HTTP_400_BAD_REQUEST)

                # Generate and store a delete_account token for the user
                token = Token.get_or_create(user, Token.TokenActions.DELETE_ACCOUNT)

                # Send the user an email containing a link to start the deletion process of its account
                send_mail_start_delete_account_process(user, token.token)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'key': 'NOT_ACCOUNT_OWNER'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'key': 'MISSING_INTERNAL_FIELDS'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_token(request, token):
    if request.method == 'GET':
        check = Token.check_token(token, request.GET.get('action'))
        if 'success' in check:
            token = check['success']

            tk_serializer = TokenSerializer(instance=token)
            serialized_token = tk_serializer.data
            return JsonResponse(serialized_token, status=status.HTTP_200_OK)
        else:
            error_key = check['error']
            if error_key == 'TOKEN_DOESNT_EXIST':
                return Response({'key': error_key}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'key': error_key}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def recover_account(request):
    """
    Form received when a user clicked on the recover button from the /recover-account page

    :param request: The request made by the user
    :type request: WSGIRequest
    :return: A HTTP response send back to the user
    :rtype: Response
    """
    if request.method == 'POST':
        if 'accountValue' in request.data:
            auth_value = request.data['accountValue']

            # Fetch the user based on the auth value
            try:
                user = User.objects.get(email=auth_value)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(username=auth_value)
                except User.DoesNotExist:
                    return Response({'key': 'ACCOUNT_DOESNT_EXIST'}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_disabled:
                # Generate and store a recover_account token for the user
                token = Token.get_or_create(user, Token.TokenActions.RECOVER_ACCOUNT)

                # Send the user an email containing a link to recover its account
                send_mail_recover_account(user, token.token)

                return Response(user.email, status=status.HTTP_201_CREATED)
            return Response({'key': 'ACCOUNT_NOT_DISABLED'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'key': 'MISSING_INTERNAL_FIELDS'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])
def recover_account_confirm_token(request, token):
    """
    Apply the action of recovering an account based on a token

    :param request: The request made by the user
    :type request: WSGIRequest
    :param token: The token required to apply the account recovering
    :type token: str
    :return: A HTTP response send back to the user
    :rtype: Response
    """
    if request.method == 'GET':
        check = Token.check_token(token, 'recover_account')
        if 'success' in check:
            token = check['success']
            user = token.user

            # Here we don't check whether the account is disabled or not to prevent any error that may have
            # occurred. We still do all the checks to prevent undesired account deletion.

            try:
                with transaction.atomic():
                    # Recover the account
                    user.is_disabled = False
                    user.save()

                    # Use the token
                    token.use()

                    # Remove the account from the deletion scheduling if it was present
                    ScheduledAccountDeletion.objects.filter(user=user).delete()

                    return Response(status=status.HTTP_200_OK)
            except:
                return Response({'key': 'INTERNAL_ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            error_key = check['error']
            if error_key == 'TOKEN_DOESNT_EXIST':
                return Response({'key': error_key}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'key': error_key}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])
def delete_account_confirm_token(request, token):
    """
    Start the process of account deleting

    :param request: The request made by the user
    :type request: WSGIRequest
    :param token: The token required to start the process
    :type token: str
    :return: A HTTP response send back to the user
    :rtype: Response
    """
    if request.method == 'GET':
        check = Token.check_token(token, 'delete_account')
        if 'success' in check:
            token = check['success']
            user = token.user

            try:
                with transaction.atomic():
                    # Disable the user account
                    user.is_disabled = True
                    user.save()

                    # Use the token
                    token.use()

                    # Add the user inside the deletion scheduling system
                    ScheduledAccountDeletion.objects.create(user=user, interval=settings.INTERVAL_ACCOUNT_DELETION)

                    return Response(status=status.HTTP_200_OK)
            except:
                return Response({'key': 'INTERNAL_ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            error_key = check['error']
            if error_key == 'TOKEN_DOESNT_EXIST':
                return Response({'key': error_key}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'key': error_key}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def close_item(request, item_id):
    if request.method == 'POST':
        if 'reason' in request.data:
            reason = request.data['reason']
            if reason in Item.ClosedReason.values:
                try:
                    item = Item.objects.get(pk=item_id)

                    if item.user_id != request.user.id:
                        return Response("You cannot close an item you do not own.", status=status.HTTP_403_FORBIDDEN)

                    item.closed_reason = reason
                    item.save()
                    return Response(status=status.HTTP_200_OK)
                except Item.DoesNotExist:
                    return Response({'key': 'ITEM_DOESNT_EXIST'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'key': 'ITEM_CLOSING_REASON_DOESNT_EXIST'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'key': 'MISSING_INTERNAL_FIELDS'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
