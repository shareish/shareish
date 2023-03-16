import base64
import json
import re
from datetime import datetime, timezone

from django.db.models import Q
from django.http import FileResponse, JsonResponse
from django.contrib.auth import get_user_model

from .models import Conversation, Item, ItemImage, Message, UserImage

User = get_user_model()

from rest_framework import filters, viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .pagination import ActivePaginationClass
from .serializers import (
    ItemSerializer, UserSerializer, ItemImageSerializer,
    ConversationSerializer, MessageSerializer, UserImageSerializer, MapNameAndDescriptionSerializer
)
from .permissions import IsOwnerProfileOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated

from .ai import findClass

from geopy.geocoders import Nominatim

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


class ItemTypeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        item_type = request.query_params.get('item_type')
        if item_type is not None:
            return queryset.filter(item_type=item_type)
        return queryset


class ItemCategoryFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category')
        if category is not None:
            return queryset.filter(
                Q(category1=category) | Q(category2=category) | Q(category3=category)
            )
        return queryset


class ActiveItemFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            Q(in_progress=True),
            Q(enddate__isnull=True) | Q(enddate__gte=datetime.now())
        )


class UserItemFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.query_params.get('id')
        if user is not None:
            return queryset.filter(user_id=int(user))
        else:
            return queryset.filter(user=request.user)


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
    ordering = ['-startdate']

    def retrieve(self, request, *args, **kwargs):
        # Solution to view ended item, maybe temporary
        # Previously, used ?kind=user but only owner could see the item, not cool
        pk = int(kwargs['pk'])
        try:
            instance = Item.objects.get(pk=pk)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response("Item doesn't exist.", status=status.HTTP_404_NOT_FOUND)

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
            if item.item_type != "EV":
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
    ordering = ['-startdate']

    def get_queryset(self):
        return Item.objects.filter(is_recurrent=True, user=self.request.user)


class ActiveItemViewSet(ItemViewSet):
    filter_backends = [filters.OrderingFilter, ActiveItemFilterBackend]
    pagination_class = ActivePaginationClass
    ordering = ['-startdate']


class UserItemViewSet(ItemViewSet):
    filter_backends = [filters.OrderingFilter, UserItemFilterBackend]
    ordering = ['-startdate']


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

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(Q(owner=user) | Q(buyer=user))

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            already_exist = Conversation.objects.filter(
                owner_id=data['owner_id'],
                buyer_id=data['buyer_id'],
                item_id=data['item_id']
            )
            if already_exist:
                serializer = ConversationSerializer(already_exist[0], many=False)
                return Response(serializer.data['id'], status=status.HTTP_200_OK)

            to_serialize = {}

            # Retrieving objects instead of ids
            item = Item.objects.get(pk=data['item_id'])
            if item.enddate is not None and item.enddate < datetime.now(timezone.utc):
                return Response("You can't start a conversation on this item, it has already ended.", status=status.HTTP_400_BAD_REQUEST)
            owner = User.objects.get(pk=data['owner_id'])
            buyer = User.objects.get(pk=data['buyer_id'])

            # Generating conversation slug
            to_serialize['name'] = str(data['item_id']) + "-" + str(data['owner_id']) + "-" + str(data['buyer_id'])
            to_serialize['slug'] = item.name + " (" + owner.username + " and " + buyer.username + ")"

            serializer = self.get_serializer(data=to_serialize)
            if serializer.is_valid():
                serializer.save(owner=owner, buyer=buyer, item=item)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data['id'], status=status.HTTP_201_CREATED, headers=headers)
            return Response({'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response("Couldn't create the new conversation.", status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation = Conversation.objects.get(pk=self.kwargs['conversation_id'])
        return Message.objects.filter(conversation=conversation)


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

        if searched['name'] is None and searched['item_type'] is None and searched['category'] is None:
            serialized_items = ItemSerializer(queryset, many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK)

        if searched['name'] is not None:
            items_name = queryset.filter(name__icontains=searched['name'])
            items_description = queryset.filter(description__icontains=searched['name'])
            items = items | items_description | items_name
        if searched['item_type'] is not None:
            items_item_type = queryset.filter(item_type__exact=searched['item_type'])
            items = items | items_item_type
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
            Q(conversation__owner=user) | Q(conversation__buyer=user)
        ).count()

    user = request.user

    if request.method == 'GET':
        return Response(_get_unread_messages(user), status=status.HTTP_200_OK)
    elif request.method == 'POST':
        try:
            conversation = Conversation.objects.get(pk=request.data['conversation_id'])
            if conversation.buyer != user and conversation.owner != user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Set all messages sent by other user as seen by current user for this conversation
            Message.objects.filter(
                Q(conversation__id=request.data['conversation_id']),
                Q(id__lte=request.data['last_message_id']),
                ~Q(user=user)
            ).update(seen=True)

            # Return unread messages count for all conversations
            return Response(_get_unread_messages(user), status=status.HTTP_200_OK)
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
            UserImage.objects.get(pk=userimage_id).delete()
            return Response(status=status.HTTP_200_OK)
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
