from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
import json
from .models import Barter, BarterImage
from .forms import SignUpForm, LoginForm, BarterForm
from django.contrib.auth import get_user_model
User = get_user_model()

import logging
logger = logging.getLogger('django')

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from mymap.serializers import BarterSerializer, UserSerializer, BarterImageSerializer

from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="shareish")

#@login_required
def index(request):
    best_barter_list = Barter.objects.order_by('id')[:3]

    context = {'best_barter_list': best_barter_list, 'user' : request.user}
    return render(request, 'mymap/index.html', context)

#@login_required
def addBarter(request):
    if request.method == "POST":
        """
        I should maybe create a class controller where i do all this stuff ? TODO ask Mr Marée about that
        """
        form = BarterForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['name']
            type = request.POST['barter_type']
            cat1 = request.POST['category1']
            cat2 = request.POST.get('cat2', None)
            cat3 = request.POST.get('cat3', None)
            description = request.POST['description']
            images = request.FILES.getlist('images')
            if len(images)!=0:
                barter = Barter(name = name, barter_type = type, category1 = cat1, category2 = cat2, category3 = cat3, description = description, user=request.user, image = images[0])
            else:
                barter = Barter(name = name, barter_type = type, category1 = cat1, category2 = cat2, category3 = cat3, description = description, user=request.user)
            barter.save()
            for image in images:
                newImage = BarterImage(image = image, barter = barter)
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
                'id': barter.id
            })
    else:
        form = BarterForm()
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
    item['barter_type'] = changeBType(item['barter_type'])
    if item['category1']:
        item['category1'] = changeCategory(item['category1'])
    if item['category2']:
        item['category2'] = changeCategory(item['category2'])
    if item['category3']:
        item['category3'] = changeCategory(item['category3'])
    return BarterImage.objects.filter(barter_id = item['id']).order_by('id')

class BarterViewSet(viewsets.ModelViewSet):
    serializer_class = BarterSerializer
    queryset = Barter.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        address = data['location']
        if address != '':
            geoloc = locator.geocode(address)[-1]
            if geoloc != None:
                data['location'] = "SRID=4326;POINT (" + str(geoloc[1]) + " " + str(geoloc[0]) + ")"

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            print('salut')
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #TODO il faut changer deux trois trucs ici

    def retrieve(self, request, pk=None):
        totalImages = []
        try:
            barter = Barter.objects.get(pk=pk)
        except Barter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BarterSerializer(barter)
        totalImages.append(changeInstance(serializer.data))
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            barter = Barter.objects.get(pk=pk)
        except Barter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BarterSerializer(barter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            barter = Barter.objects.get(pk=pk)
        except Barter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        barter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BarterImageViewSet(viewsets.ViewSet):

    def list(self, request):
        images = BarterImage.objects.all()
        serializer = BarterImageSerializer(images, many=True)
        return Response(serializer.data)

    def create(self, request):
        barter = Barter.objects.get(pk = request.POST['barterID'])
        print(request.FILES)
        images = request.FILES.getlist('files')
        for image in images:
            print('coucou')
            newImage = BarterImage(image = image, barter = barter)
            newImage.save()
            print(newImage)
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            image = BarterImage.objects.get(pk=pk)
        except BarterImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BarterImageSerializer(image)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            image = BarterImage.objects.get(pk=pk)
        except BarterImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BarterImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            image = BarterImage.objects.get(pk=pk)
        except BarterImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

#@login_required
def showContent(request):
    return HttpResponse("Hello. You're at the content.")

#@login_required
@api_view(['POST'])
def searchBarter(request):
    if request.method == "POST":
        searched = request.data
        barters_name = None
        barters_barter_type = None
        barters_category = None
        barters = Barter.objects.none()
        if 'name' in searched:
            barters_name = Barter.objects.filter(name__icontains=searched['name'])
            barters_description = Barter.objects.filter(description__icontains=searched['name'])
            barters = barters | barters_description | barters_name
        if 'barter_type' in searched:
            barters_barter_type = Barter.objects.filter(barter_type__exact=searched['barter_type'])
            barters = barters | barters_barter_type
        if 'category' in searched:
            barters_category1 = Barter.objects.filter(category1__exact='FD')
            barters_category2 = Barter.objects.filter(category2__exact=searched['category'])
            barters_category3 = Barter.objects.filter(category3__exact=searched['category'])
            barters = barters | barters_category1 | barters_category2 | barters_category3

            serialized_barters = serializers.serialize('jsonl', list(barters), fields=('id', 'name', 'location'))
        return Response(serialized_barters, status=status.HTTP_200_OK)
    else:
        return render(request, 'mymap/search_barter.html', {'user': request.user})

#@login_required
def profil(request, user_id):
    print(user_id)
    user_information = get_object_or_404(User, pk=user_id)
    barter_list = Barter.objects.filter(user__email = user_information.email).order_by('-id')[:2] #two last if the user wants more we should pt a button "see all barters"
    return render(request, 'mymap/profil.html', {'user': request.user, 'barter_list': barter_list, 'user_information': user_information})

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
    barter_list = Barter.objects.all()
    location_x = []
    location_y = []
    name = []
    for barter in barter_list:
        if barter.location != None:
            location_x.append(barter.location.x)
            location_y.append(barter.location.y)
        else:
            location_x.append(None)
            location_y.append(None)
        name.append(barter.name)


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