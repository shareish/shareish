from datetime import datetime

from django.db.models import Q, F
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

locator = Nominatim(user_agent="shareish")

LOCATION_PREFIX = "SRID=4326;POINT"


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

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'location' in data:
            address = data['location']
            if address != '' and address is not None:
                geoloc = locator.geocode(address)
                if geoloc is not None:
                    data['location'] = "{} ({} {})".format(
                        LOCATION_PREFIX,
                        str(geoloc.latitude),
                        str(geoloc.longitude)
                    )
                else:
                    print("Warning: {} given but no location found.".format(address))
                    del data['location']
            else:
                del data['location']

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        if 'location' in request.data:
            address = request.data['location']
            if address != '' and address is not None and not address.startswith(LOCATION_PREFIX):
                geoloc = locator.geocode(address)
                if geoloc is not None:
                    request.data['location'] = "{} ({} {})".format(
                        LOCATION_PREFIX,
                        str(geoloc.latitude),
                        str(geoloc.longitude)
                    )
                else:
                    return Response({"message": "Bad location."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecurrentItemViewSet(ItemViewSet):
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter, ItemTypeFilterBackend, ItemCategoryFilterBackend,
    ]  # Do not need ActiveItemFilterBackend

    def get_queryset(self):
        return Item.objects.filter(is_recurrent=True, user=self.request.user)


class ActiveItemViewSet(ItemViewSet):
    pagination_class = ActivePaginationClass

    def get_queryset(self):
        return Item.objects.filter(in_progress=True)


class UserItemViewSet(ItemViewSet):
    queryset = Item.objects.all()
    filter_backends = [UserItemFilterBackend]


class ItemImageViewSet(viewsets.ViewSet):
    def list(self, request):
        images = ItemImage.objects.all()
        serializer = ItemImageSerializer(images, many=True)
        return Response(serializer.data)

    def create(self, request):
        item = Item.objects.get(pk=request.POST['item_id'])
        image = request.FILES.get('image')
        new_image = ItemImage(image=image, item=item)
        new_image.save()
        serialized_image = ItemImageSerializer(new_image)
        return Response(serialized_image.data['url'], status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            image = ItemImage.objects.get(pk=pk)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemImageSerializer(image)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            image = ItemImage.objects.get(pk=pk)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            image = ItemImage.objects.get(pk=pk)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]

    def get_instance(self):
        return self.request.user

    @action(["put", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'ref_location' in data:
            address = data['ref_location']
            if address != '' and address is not None:
                geoloc = locator.geocode(address)
                if geoloc is not None:
                    data['ref_location'] = "{} ({} {})".format(
                        LOCATION_PREFIX,
                        str(geoloc.latitude),
                        str(geoloc.longitude)
                    )
                else:
                    print("Warning: {} given but no location found.".format(address))
                    data['ref_location'] = None

        serializer = self.get_serializer(data=data)
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
        if 'ref_location' in request.data:
            address = request.data['ref_location']
            if address is not None:
                if isinstance(address, str):
                    address = address.strip()
                    if address == '':
                        request.data['ref_location'] = None
                    elif not address.startswith(LOCATION_PREFIX):
                        location = locator.geocode(address)
                        if location is not None:
                            request.data['ref_location'] = "{} ({} {})".format(
                                LOCATION_PREFIX,
                                str(location.latitude),
                                str(location.longitude)
                            )
                        else:
                            return Response("Couldn't find location.", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Bad address received.", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        return Response({"serializer_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserImageViewSet(viewsets.ViewSet):
    def create(self, request):
        user = User.objects.get(pk=request.POST['user_id'])
        image = request.FILES.get('image')
        new_image = UserImage(image=image, user=user)
        new_image.save()
        serialized_image = UserImageSerializer(new_image)
        return Response(serialized_image.data['url'], status=status.HTTP_201_CREATED)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(Q(owner=user) | Q(buyer=user))

    def create(self, request, *args, **kwargs):
        data = request.data
        already_exist = Conversation.objects.filter(
            owner_id=data['owner_id'],
            buyer_id=data['buyer_id'],
            item_id=data['item_id']
        )
        if already_exist:
            serializer = ConversationSerializer(already_exist[0], many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        to_serialize = {}

        # Retrieving objects instead of ids
        owner = User.objects.get(pk=data['owner_id'])
        buyer = User.objects.get(pk=data['buyer_id'])
        item = Item.objects.get(pk=data['item_id'])

        # Generating conversation slug
        to_serialize['name'] = str(data['item_id']) + '-' + str(data['owner_id']) + '-' + str(data['buyer_id'])
        to_serialize['slug'] = item.name + ' (' + owner.username + ' and ' + buyer.username + ')'

        serializer = self.get_serializer(data=to_serialize)
        if serializer.is_valid():
            serializer.save(owner=owner, buyer=buyer, item=item)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    if request.method == "POST":
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
    if request.method == "POST":
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
    if request.method == "POST":
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
    if request.method == "POST":
        image = request.FILES.get('image')
        if image:
            class_found, category_found, detected_text = findClass(image)
            response = {
                "suggested_class": class_found,
                "suggested_category": category_found,
                "detected_text": detected_text
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def getNotifications(request):
    def _get_unread_messages(user):
        return Message.objects.filter(
            ~Q(user=user), Q(seen=False),
            Q(conversation__owner=user) | Q(conversation__buyer=user)
        ).count()

    if request.method == 'GET':
        return Response({"unread_messages": _get_unread_messages(request.user)}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user = request.user
        data = request.data
        try:
            conversation = Conversation.objects.get(pk=data['conversation_id'])
            if conversation.buyer != user and conversation.owner != user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Set all messages sent by other user as seen by current user for this conversation
            Message.objects.filter(
                Q(conversation__id=data['conversation_id']),
                Q(id__lte=data['last_message_id']),
                ~Q(user=user)
            ).update(seen=True)

            # Return unread messages count for all conversations
            return Response({"unread_messages": _get_unread_messages(user)}, status=status.HTTP_200_OK)
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


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def getUserImage(request, userimage_id):
    if request.method == 'GET':
        try:
            image = UserImage.objects.get(pk=userimage_id)
            return FileResponse(open(image.path, 'rb'))
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
