from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
import json
from .models import Item, ItemImage, Conversation, Message
from .forms import SignUpForm, LoginForm, ItemForm
from django.contrib.auth import get_user_model
User = get_user_model()

import logging
logger = logging.getLogger('django')

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from mymap.serializers import ItemSerializer, UserSerializer, ItemImageSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsOwnerProfileOrReadOnly
from rest_framework.permissions import IsAuthenticated

from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="shareish")

#@login_required
def index(request):
    best_item_list = Item.objects.order_by('id')[:3]

    context = {'best_item_list': best_item_list, 'user' : request.user}
    return render(request, 'mymap/index.html', context)

#@login_required
def addItem(request):
    if request.method == "POST":
        """
        I should maybe create a class controller where i do all this stuff ? TODO ask Mr Marée about that
        """
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['name']
            type = request.POST['item_type']
            cat1 = request.POST['category1']
            cat2 = request.POST.get('cat2', None)
            cat3 = request.POST.get('cat3', None)
            description = request.POST['description']
            images = request.FILES.getlist('images')
            if len(images)!=0:
                item = Item(name = name, item_type = type, category1 = cat1, category2 = cat2, category3 = cat3, description = description, user=request.user, image = images[0])
            else:
                item = Item(name = name, item_type = type, category1 = cat1, category2 = cat2, category3 = cat3, description = description, user=request.user)
            item.save()
            for image in images:
                newImage = ItemImage(image = image, item = item)
                newImage.save()
            return render(request, 'mymap/addBarter.html',
            {
                'name': name,
                'type': type,
                'cat1': cat1,
                'cat2': cat2,
                'cat3': cat3,
                'description': description,
                'user': request.user,
                'id': item.id
            })
    else:
        form = ItemForm()
    return render(request, 'mymap/addBarter.html', {'user': request.user, 'form': form})

def changeBType(btype):
    if btype == 'LN':
        return 'Loan'
    elif btype == 'DN':
        return 'Donation'
    else:
        return 'Barter'

def changeCategory(cat):
    if cat == 'FD':
        return 'Food'
    elif cat == 'AN':
        return 'Animals'
    elif cat == 'EN':
        return 'Arts and Entertainment'
    elif cat == 'CL':
        return 'Collectors'
    elif cat == 'HL':
        return 'Helping Hand'
    elif cat == 'DY':
        return 'DIY'
    elif cat == 'BT':
        return 'Beauty and Well-being'
    elif cat == 'CH':
        return 'Childhood'
    elif cat == 'IT':
        return 'IT and Multimedia'
    elif cat == 'GD':
        return 'Garden'
    elif cat == 'HS':
        return 'House'
    elif cat == 'HD':
        return 'Holidays and Week-end'
    elif cat == 'BK':
        return 'Books, CDs and DVDs'
    elif cat == 'SP':
        return 'Sports and Leisure'
    elif cat == 'TS':
        return 'Transport and vehicle'
    else:
        return 'Other'

def changeInstance(item):
    item['item_type'] = changeBType(item['item_type'])
    if item['category1']:
        item['category1'] = changeCategory(item['category1'])
    if item['category2']:
        item['category2'] = changeCategory(item['category2'])
    if item['category3']:
        item['category3'] = changeCategory(item['category3'])
    return ItemImage.objects.filter(item_id = item['id']).order_by('id')

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
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
        address = request.data['location']
        if address != '':
            geoloc = locator.geocode(address)
            if geoloc != None:
                request.data['location'] = "SRID=4326;POINT (" + str(geoloc.latitude) + " " + str(geoloc.longitude) + ")"
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemImageViewSet(viewsets.ViewSet):

    def list(self, request):
        images = ItemImage.objects.all()
        serializer = ItemImageSerializer(images, many=True)
        return Response(serializer.data)

    def create(self, request):
        item = Item.objects.get(pk = request.POST['itemID'])
        print(request.FILES)
        images = request.FILES.getlist('files')
        for image in images:
            print('coucou')
            newImage = ItemImage(image = image, item = item)
            newImage.save()
            print(newImage)
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

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

@api_view(['POST'])
def getAddress(request):
    if request.method == "POST":
        address = request.data['SRID']
        print(address)
        address = address.split(' ')
        address[1] = address[1][1:]
        address[2] = address[2][:-1]
        geoloc = locator.reverse((address[1], address[2]), exactly_one=True)
        if geoloc != None:
            return Response(geoloc.address)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#@login_required
def showContent(request):
    return HttpResponse("Hello. You're at the content.")

#@login_required
@api_view(['POST'])
def searchItem(request):
    if request.method == "POST":
        searched = request.data
        items_name = None
        items_item_type = None
        items_category1 = None
        items_category2 = None
        items_category3 = None
        items = Item.objects.none()
        if 'name' in searched:
            items_name = Item.objects.filter(name__icontains=searched['name'])
            items_description = Item.objects.filter(description__icontains=searched['name'])
            items = items | items_description | items_name
        if 'item_type' in searched:
            items_item_type = Item.objects.filter(item_type__exact=searched['item_type'])
            items = items | items_item_type
        if 'category' in searched:
            items_category1 = Item.objects.filter(category1__exact=searched['category'])
            items_category2 = Item.objects.filter(category2__exact=searched['category'])
            items_category3 = Item.objects.filter(category3__exact=searched['category'])
            items = items | items_category1 | items_category2 | items_category3
        
        serialized_items = ItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

#@login_required
def profil(request, user_id):
    print(user_id)
    user_information = get_object_or_404(User, pk=user_id)
    item_list = Item.objects.filter(user__email = user_information.email).order_by('-id')[:2] #two last if the user wants more we should pt a button "see all items"
    return render(request, 'mymap/profil.html', {'user': request.user, 'item_list': item_list, 'user_information': user_information})

#@login_required
def groups(request):
    return HttpResponse("Hello. You're at the groups.")

def mapTest(request):
    '''
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = get_client_ip(request)
    g = GeoIP2()
    if ip != '127.0.0.1':
        lat_lon = g.lat_lon(ip)
    else:
        lat_lon = g.lat_lon('2a02:a03f:a18f:5f00:6d80:7c8d:b686:3f60')
    '''
    item_list = Item.objects.all()
    location_x = []
    location_y = []
    name = []
    for item in item_list:
        if item.location != None:
            location_x.append(item.location.x)
            location_y.append(item.location.y)
        else:
            location_x.append(None)
            location_y.append(None)
        name.append(item.name)


    return render(request, 'mymap/mapTest.html', {'location_x': json.dumps(location_x), 'location_y': json.dumps(location_y), 'name': json.dumps(name)})

def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            logger.info(user)
            if user:
                auth_login(request, user)
                return redirect('index')
            #else:
                #Envoyer un message d'erreur de login
    return render(request, 'mymap/login.html', {'form':form})

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password = raw_password)
            if account is not None:
                auth_login(request, account)
                redirect('index')
    return render(request, 'mymap/sign_up.html', {'form': form})

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return redirect('login')

"""TODO A travailler le login et logout"""