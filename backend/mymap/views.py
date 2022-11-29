from datetime import datetime

from django.db.models import Q
from django.http import FileResponse, JsonResponse
from django.contrib.auth import get_user_model

from .models import Conversation, Item, ItemImage, Message, UserImage

User = get_user_model()

from rest_framework import filters, viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .pagination import ActivePaginationClass
from mymap.serializers import (
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


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]

    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter,
        ItemTypeFilterBackend, ItemCategoryFilterBackend,
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
                    data['location'] = None

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
                    return Response(
                        {"message": "Bad location."}, status=status.HTTP_400_BAD_REQUEST
                    )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecurrentItemViewSet(ItemViewSet):
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter,
        ItemTypeFilterBackend, ItemCategoryFilterBackend,
    ]  # Do not need ActiveItemFilterBackend

    def get_queryset(self):
        return Item.objects.filter(is_recurrent=True, user=self.request.user)


class ActiveItemViewSet(ItemViewSet):
    pagination_class = ActivePaginationClass

    def get_queryset(self):
        return Item.objects.filter(in_progress=True)


class UserItemFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.query_params.get('id')
        if user is not None:
            return queryset.filter(user_id=int(user))
        else:
            return queryset.filter(user=request.user)


class UserItemViewSet(ItemViewSet):
    queryset = Item.objects.all()
    filter_backends = [UserItemFilterBackend]


# TODO: why not model view set ?
class ItemImageViewSet(viewsets.ViewSet):
    def list(self, request):
        images = ItemImage.objects.all()
        serializer = ItemImageSerializer(images, many=True)
        return Response(serializer.data)

    def create(self, request):
        item = Item.objects.get(pk=request.POST['itemID'])
        existings = ItemImage.objects.filter(item=item)
        for existing in existings:
            existing.delete()
        images = request.FILES.getlist('files')
        if request.FILES.get('image') is not None:
            images += [request.FILES.get('image')]

        print(images)
        for image in images:
            new_image = ItemImage(image=image, item=item)
            new_image.save()
            serialized_image = ItemImageSerializer(new_image)
        return Response(serialized_image.data, status=status.HTTP_201_CREATED)

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


class UserImageViewSet(viewsets.ViewSet):
    def list(self, request):
        images = UserImage.objects.all()
        serializer = UserImageSerializer(images, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = User.objects.get(pk=request.POST['userID'])
        existings = UserImage.objects.filter(user=user)
        for existing in existings:
            existing.delete()
        images = [request.FILES.get('image')]
        for image in images:
            new_image = UserImage(image=image, user=user)
            new_image.save()
            serialized_image = UserImageSerializer(new_image)
        return Response(serialized_image.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            image = UserImage.objects.get(pk=pk)
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserImageSerializer(image)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            image = UserImage.objects.get(pk=pk)
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            image = UserImage.objects.get(pk=pk)
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(owner=user) | Conversation.objects.filter(buyer=user)

    def create(self, request, *args, **kwargs):
        data = request.data
        owner = User.objects.get(pk=data['owner'])
        buyer = User.objects.get(pk=data['buyer'])
        item = Item.objects.get(pk=data['item'])
        already_exist = Conversation.objects.filter(
            owner=owner, buyer=buyer, item=item, name=data['name']
        )
        if already_exist:
            serializer = ConversationSerializer(already_exist[0], many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        data['owner'] = None
        data['buyer'] = None
        data['item'] = None
        data['slug'] = None
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            slug = getattr(item, 'name') + ' (' + getattr(owner, 'username') + ' and ' + getattr(
                buyer, 'username'
            ) + ')'
            self.perform_create(serializer, owner, buyer, item, slug)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, owner, buyer, item, slug):
        serializer.save(owner=owner, buyer=buyer, item=item, slug=slug)


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
        address = request.data['SRID']
        address = address.split(' ')
        address[1] = address[1][1:]
        address[2] = address[2][:-1]
        geoloc = locator.reverse((address[1], address[2]), exactly_one=True)
        if geoloc is not None:
            return Response(geoloc.address, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def searchItemFilter(request):
    if request.method == "POST":
        searched = request.data
        items = Item.objects.none()
        queryset = Item.objects.filter(in_progress=True)

        if searched['name'] == "":
            searched['name'] = None

        if (searched['name'] is None
                and searched['item_type'] is None
                and searched['category'] is None):
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
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def predictClass(request):
    if request.method == "POST":
        if request.FILES.get('files[]'):
            class_found, detected_text = findClass(request.FILES.get('files[]'))
            response = {
                "suggested_class": class_found,
                "detected_text": detected_text
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def getNotifications(request):
    def _get_unread_messages(user):
        return Message.objects.filter(
            Q(conversation__owner=user) | Q(conversation__buyer=user),
            Q(seen=False), ~Q(user=user)
        ).count()

    if request.method == 'GET':
        user = request.user
        response = {
            "unread_messages": _get_unread_messages(user)
        }
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user = request.user
        data = request.data
        conversation = Conversation.objects.get(pk=data['conversation'])
        if conversation is None \
                or (conversation.buyer != user and conversation.owner != user):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Set all messages sent by other user as seen by current user for this conversation
        count = Message.objects.filter(
            Q(conversation__id=data['conversation']),
            Q(id__lte=data['last_message']),
            ~Q(user=user)
        ).update(seen=True)
        print(count)

        # Return unread messages count for all conversations
        response = {
            "unread_messages": _get_unread_messages(user)
        }
        return Response(response, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getFirstItemImage(request, id):
    if request.method == 'GET':
        item = Item.objects.get(pk=id)
        images = ItemImage.objects.filter(item=item)
        print(images)
        if len(images) > 0:
            image = images[0]
            serialized_image = ItemImageSerializer(image, many=False)
            return Response(serialized_image.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def getUserImage(request, id):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        image = UserImage.objects.get(pk=id)
        return FileResponse(open(image.path, 'rb'))
    except UserImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: use short living token instead of allowing any
def getItemImage(request, id):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        image = ItemImage.objects.get(pk=id)
        return FileResponse(open(image.path, 'rb'))
    except ItemImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
