import base64
import json
import re
from datetime import datetime, timezone

from django.db.models import Q
from django.http import FileResponse, JsonResponse
from django.contrib.auth import get_user_model

from .filters import ItemTypeFilterBackend, ConversationContentFilterBackend, ItemCategoryFilterBackend, \
    ActiveItemFilterBackend, UserItemFilterBackend, ConversationSelectedCategoryFilterBackend
from .models import Conversation, Item, ItemImage, Message, UserImage, ItemComment

from rest_framework import filters, viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .pagination import ActivePaginationClass
from .serializers import (
    ItemSerializer, UserSerializer, ItemImageSerializer,
    ConversationSerializer, MessageSerializer, UserImageSerializer, MapNameAndDescriptionSerializer,
    ItemCommentSerializer
)
from .permissions import IsOwnerProfileOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated

from .ai import findClass

from geopy.geocoders import Nominatim


User = get_user_model()
locator = Nominatim(user_agent='shareish')
LOCATION_PREFIX = "SRID=4326;POINT"


def verif_location(data):
    if isinstance(data, str):
        address = data.strip()
        if address == "":
            return {'success': ""}
    elif data is None:
        return {'success': ""}
    else:
        return {'error': "No suitable address to process."}

    if not address.startswith(LOCATION_PREFIX):
        location = locator.geocode(address)
        if location is not None:
            return {'success': "{} ({} {})".format(
                LOCATION_PREFIX,
                str(location.latitude),
                str(location.longitude)
            )}
        else:
            return {'error': "Couldn't find location."}
    else:
        return {'success': address}


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter, ItemTypeFilterBackend, ItemCategoryFilterBackend,
        ActiveItemFilterBackend
    ]
    search_fields = ['name', 'description']
    ordering_fields = '__all__'

    def retrieve(self, request, *args, **kwargs):
        # Solution to view ended item, maybe temporary
        # Previously, used ?kind=user but only owner could see the item, not cool
        pk = int(kwargs['pk'])
        try:
            instance = Item.objects.get(pk=pk)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response("This item doest not exist.", status=status.HTTP_404_NOT_FOUND)

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


class RecurrentItemViewSet(ItemViewSet):
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        return Item.objects.filter(is_recurrent=True, user=self.request.user)


class ActiveItemViewSet(ItemViewSet):
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter, ActiveItemFilterBackend, ItemCategoryFilterBackend,
        ItemTypeFilterBackend
    ]
    search_fields = ['name', 'description', 'user__username']
    pagination_class = ActivePaginationClass


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
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return Response({'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You must provide and item id to post a comment.", status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        try:
            item = Item.objects.get(pk=self.kwargs['item_id'])
            serializer.save(user=self.request.user, item=item)
        except Item.DoesNotExist:
            return Response("This item doest not exist.", status=status.HTTP_400_BAD_REQUEST)
        except Item.MultipleObjectsReturned:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

    def get_instance(self):
        return self.request.user

    @action(['put', 'patch'], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)

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

        result = verif_location(request.data['ref_location'])
        if 'success' in result:
            request.data['ref_location'] = result['success']
        else:
            return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)

        instagram_username_regex = r"([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
        if re.match("^" + instagram_username_regex + "$", request.data['instagram_url']):
            request.data['instagram_url'] = "https://www.instagram.com/" + request.data['instagram_url'] + "/"

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
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


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [ConversationContentFilterBackend, ConversationSelectedCategoryFilterBackend]

    def get_queryset(self):
        starter = self.request.user
        return Conversation.objects.filter(Q(starter=starter) | Q(item__user=starter))

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            item = Item.objects.get(pk=data['item_id'])
        except Item.DoesNotExist:
            return Response("This item doest not exist.", status=status.HTTP_400_BAD_REQUEST)
        except Item.MultipleObjectsReturned:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if item.user_id == request.user.id:
            return Response("You cannot start a conversation on an item you own.", status=status.HTTP_403_FORBIDDEN)

        try:
            conversation = Conversation.objects.get(
                starter_id=request.user.id,
                item=item
            )
            serializer = ConversationSerializer(conversation, many=False)
            return Response(serializer.data['id'], status=status.HTTP_200_OK)
        except Conversation.DoesNotExist:
            if item.enddate is not None and item.enddate < datetime.now(timezone.utc):
                return Response("You cannot start a conversation on this item, it has already ended.", status=status.HTTP_400_BAD_REQUEST)
            starter = User.objects.get(pk=request.user.id)

            conversation = Conversation.objects.create(starter=starter, item=item)
            return Response(conversation.id, status=status.HTTP_201_CREATED)
        except Conversation.MultipleObjectsReturned:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        if 'conversation_id' in self.kwargs:
            conversation = Conversation.objects.get(pk=self.kwargs['conversation_id'])
            return Message.objects.filter(conversation=conversation)
        else:
            return Message.objects.all()


class MapNameAndDescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = MapNameAndDescriptionSerializer
    queryset = Item.objects.filter(in_progress=True)


@api_view(['POST'])
def getAddress(request):
    if request.method == 'POST':
        coords = request.data['SRID'].split(' ')[1:]
        latitude = coords[0][1:]
        longitude = coords[1][:-1]
        location = locator.reverse((latitude, longitude), exactly_one=True)
        if location is not None:
            return Response(location.address, status=status.HTTP_200_OK)
        return Response("Couldn't find location.", status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def searchItemFilter(request):
    if request.method == 'POST':
        searched = request.data
        items = Item.objects.none()
        queryset = Item.objects.filter(in_progress=True)

        if searched['name'] == "":
            searched['name'] = None

        if searched['name'] is None and searched['type'] is None and searched['category'] is None:
            serialized_items = ItemSerializer(queryset, many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK)

        if searched['name'] is not None:
            items_name = queryset.filter(name__icontains=searched['name'])
            items_description = queryset.filter(description__icontains=searched['name'])
            items = items | items_description | items_name
        if searched['type'] is not None:
            items_type = queryset.filter(type__exact=searched['type'])
            items = items | items_type
        if searched['category'] is not None:
            items_category1 = queryset.filter(category1__exact=searched['category'])
            items_category2 = queryset.filter(category2__exact=searched['category'])
            items_category3 = queryset.filter(category3__exact=searched['category'])
            items = items | items_category1 | items_category2 | items_category3
        serialized_items = ItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def searchItems(request):
    if request.method == 'POST':
        paginator = ActivePaginationClass()
        search = request.data['search']
        items = Item.objects.none()
        if search is not None:
            items_name = Item.objects.filter(name__icontains=search)
            items_description = Item.objects.filter(description__icontains=search)
            items = items | items_description | items_name
        items = paginator.paginate_queryset(items, request)
        serialized_items = ItemSerializer(items, many=True)
        return paginator.get_paginated_response(serialized_items.data)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def predictClass(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            return JsonResponse(findClass(image), status=status.HTTP_200_OK, safe=False)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # TODO: use short living token instead of allowing any
def getNotifications(request):
    def _get_unread_messages(user):
        return Message.objects.filter(
            ~Q(user=user), Q(seen=False),
            Q(conversation__starter=user) | Q(conversation__item__user=user)
        ).count()

    user = request.user

    if request.method == 'GET':
        return Response(_get_unread_messages(user), status=status.HTTP_200_OK)
    elif request.method == 'POST':
        try:
            conversation = Conversation.objects.get(pk=request.data['conversation_id'])
            if conversation.starter != user and conversation.item.user != user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Set all messages sent by other user as seen by current user for this conversation
            Message.objects.filter(
                Q(conversation__id=request.data['conversation_id']),
                ~Q(user=user),
                Q(date__lte=request.data['last_message_date']),
                Q(seen=False)
            ).update(seen=True)

            conversation_unread_messages_count =  Message.objects.filter(
                Q(conversation__id=request.data['conversation_id']),
                ~Q(user=user),
                Q(seen=False)
            ).count()

            # Return unread messages count for all conversations
            return Response(conversation_unread_messages_count, status=status.HTTP_200_OK)
        except Conversation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def itemHasImage(request, item_id):
    if request.method == 'GET':
        try:
            images = ItemImage.objects.filter(item_id=item_id)
            if len(images) > 0:
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def getItemFirstImage(request, item_id):
    if request.method == 'GET':
        try:
            image = ItemImage.objects.filter(item_id=item_id).first()
            if image is not None:
                return FileResponse(open(image.path, 'rb'))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # TODO: use short living token instead of allowing any
def republishItemImagesFromItem(request, new_item_id, parent_item_id):
    if request.method == 'GET':
        try:
            new_item = Item.objects.get(pk=new_item_id)
            parent_item = Item.objects.get(pk=parent_item_id)
            if new_item.user == request.user and parent_item.user == request.user:
                parent_item_images = ItemImage.objects.filter(item=parent_item)
                if len(parent_item_images) > 0:
                    for new_item_image in parent_item_images:
                        new_item_image.pk = None
                        new_item_image.item_id = new_item_id
                        new_item_image.save()
                    return Response(status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'DELETE'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def userImage(request, userimage_id):
    if request.method == 'GET':
        try:
            image = UserImage.objects.get(pk=userimage_id)
            return FileResponse(open(image.path, 'rb'))
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        try:
            user_image = UserImage.objects.get(pk=userimage_id)
            if user_image.user_id == request.user.id:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response("You are not the owner of this image.", status=status.HTTP_403_FORBIDDEN)
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def getItemImage(request, itemimage_id):
    if request.method == 'GET':
        try:
            image = ItemImage.objects.get(pk=itemimage_id)
            return FileResponse(open(image.path, 'rb'))
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def increaseHitcountItem(request, item_id):
    if request.method == 'GET':
        try:
            item = Item.objects.get(pk=item_id)
            item.hitcount += 1
            item.save()
            return Response(status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def getItemImagesBase64(request, item_id):
    if request.method == 'GET':
        try:
            item_images = ItemImage.objects.filter(item_id=item_id)
            images = []
            for item_image in item_images:
                images.append({
                   "name": str(item_image.image.name),
                   "base64_url": "data:image/png;base64," + str(base64.b64encode(item_image.image.file.read()).decode("utf-8"))
                })
            return Response(json.dumps(images), status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def getUserImageBase64(request, userimage_id):
    if request.method == 'GET':
        try:
            userimage = UserImage.objects.get(pk=userimage_id)
            response = {
               "name": str(userimage.image.name),
               "base64_url": "data:image/png;base64," + str(base64.b64encode(userimage.image.file.read()).decode("utf-8"))
            }
            return Response(json.dumps(response), status=status.HTTP_200_OK)
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
