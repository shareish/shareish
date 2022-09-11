from email import message

from django.http import FileResponse

from .models import Item, ItemImage, Conversation, Message, UserImage
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .pagination import ActivePaginationClass
from mymap.serializers import ItemSerializer, UserSerializer, ItemImageSerializer, ConversationSerializer, MessageSerializer, UserImageSerializer, MapItemSerializer, MapNameAndDescriptionSerializer
from .permissions import IsOwnerProfileOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated

from .ai import findClass

from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="shareish")

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'location' in data:
            address = data['location']
            if address != '':
                geoloc = locator.geocode(address)
                if geoloc != None:
                    data['location'] = "SRID=4326;POINT (" + str(geoloc.latitude) + " " + str(geoloc.longitude) + ")"

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if 'location' in request.data:
            address = request.data['location']
            if address != '' and address != None and address.startswith("SRID=4326;POINT") == False:
                geoloc = locator.geocode(address)
                if geoloc != None:
                    request.data['location'] = "SRID=4326;POINT (" + str(geoloc.latitude) + " " + str(geoloc.longitude) + ")"
                else:
                    return Response({"message": "Bad location."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class RecurrentItemViewSet(ItemViewSet):
    def get_queryset(self):
        return Item.objects.filter(is_recurrent=True, user=self.request.user)

class ActiveItemViewSet(ItemViewSet):
    pagination_class = ActivePaginationClass
    def get_queryset(self):
        return Item.objects.filter(in_progress=True)

class UserItemViewSet(ItemViewSet):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemImageViewSet(viewsets.ViewSet):

    def list(self, request):
        images = ItemImage.objects.all()
        serializer = ItemImageSerializer(images, many=True)
        return Response(serializer.data)

    def create(self, request):
        item = Item.objects.get(pk = request.POST['itemID'])
        images = request.FILES.getlist('files')
        print(images)
        for image in images:
            newImage = ItemImage(image = image, item = item)
            newImage.save()
        return Response(status=status.HTTP_201_CREATED)

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
        user = User.objects.get(pk = request.POST['userID'])
        images = request.FILES.getlist('image')
        for image in images:
            newImage = UserImage(image = image, user = user)
            newImage.save()
            serialized_image = UserImageSerializer(newImage)
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
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(owner=user) | Conversation.objects.filter(buyer=user)

    def create(self, request, *args, **kwargs):
        data = request.data
        owner= User.objects.get(pk=data['owner'])
        buyer = User.objects.get(pk=data['buyer'])
        item = Item.objects.get(pk=data['item'])
        already_exist = Conversation.objects.filter(owner=owner, buyer=buyer, item=item, name=data['name'])
        if already_exist:
            serializer = ConversationSerializer(already_exist[0], many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        data['owner'] = None
        data['buyer'] = None
        data['item'] = None
        data['slug'] = None
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            slug = getattr(item, 'name') + ' (' + getattr(owner, 'username')+ ' and ' + getattr(buyer, 'username') + ')'
            self.perform_create(serializer, owner, buyer, item, slug)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, owner, buyer, item, slug):
        serializer.save(owner=owner, buyer=buyer, item=item, slug=slug)
    

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

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
        if geoloc != None:
            return Response(geoloc.address, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def searchItemFilter(request):
    if request.method == "POST":
        searched = request.data
        items_name = None
        items_item_type = None
        items_category1 = None
        items_category2 = None
        items_category3 = None
        items = Item.objects.none()
        queryset = Item.objects.filter(in_progress=True)
        if 'name' not in searched and searched['item_type'] == 'null' and 'category' not in searched:
            serialized_items = MapItemSerializer(queryset, many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK)
        if 'name' in searched:
            items_name = queryset.filter(name__icontains=searched['name'])
            items_description = queryset.filter(description__icontains=searched['name'])
            items = items | items_description | items_name
        if searched['item_type'] != 'null':
            items_item_type = queryset.filter(item_type__exact=searched['item_type'])
            items = items | items_item_type
        if 'category' in searched:
            items_category1 = queryset.filter(category1__exact=searched['category'])
            items_category2 = queryset.filter(category2__exact=searched['category'])
            items_category3 = queryset.filter(category3__exact=searched['category'])
            items = items | items_category1 | items_category2 | items_category3
        serialized_items = MapItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

from rest_framework.pagination import LimitOffsetPagination

@api_view(['POST'])
def searchItems(request):
    if request.method == "POST":
        paginator = ActivePaginationClass()
        search = request.data['search']
        items = Item.objects.none()
        if search != None:
            items_name = Item.objects.filter(name__icontains=search)
            items_description = Item.objects.filter(description__icontains=search)
            items = items | items_description | items_name
        items = paginator.paginate_queryset(items, request)
        serialized_items = ItemSerializer(items, many=True)
        return paginator.get_paginated_response(serialized_items.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

from PIL import Image

@api_view(['POST'])
def predictClass(request):
    if request.method == "POST":
        if(request.FILES.get('files[]')):
            class_found, detected_text = findClass(request.FILES.get('files[]'))
            print("predict output:")
            print(class_found)
            print(detected_text)
            #to do: send response with class and detected text
            return Response(class_found, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getNotifications(request):
    if request.method == 'GET':
        user = request.user
        notifications = 0
        conversations_owner = Conversation.objects.filter(owner=user)
        conversations_buyer = Conversation.objects.filter(buyer=user)
        for conversation in conversations_owner:
            if conversation.up2date_owner == False:
                notifications += 1
        for conversation in conversations_buyer:
            if conversation.up2date_buyer == False:
                notifications += 1
        return Response(notifications, status=status.HTTP_200_OK)
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
