from .models import Item
import random
from django.contrib.auth import get_user_model
User = get_user_model()

def testAddItems(nb_items, user):
    for i in range(nb_items):
        name = 'Test Serializer ' + str(i)
        latitude = random.uniform(50.668157, 50.155765)
        longitude = random.uniform(5.077769, 6.132183)
        item_type = random.choice(['BR', 'LN', 'DN'])
        location = 'SRID=4326;POINT (' + str(latitude) + ' ' + str(longitude) + ')'
        item = Item(name=name, description='Test description', location=location, user=user, item_type=item_type)
        item.save()

def testDeleteItems():
    Item.objects.filter(name__icontains='Test Serializer').delete()

def shell_script():
    #Momalle
    # latitude = random.uniform(50.689977, 50.66965)
    # longitude = random.uniform(5.363759, 5.383826)

    #Belgique
    # latitude = random.uniform(49.503271, 51.494549)
    # longitude = random.uniform(6.405264, 2.551261)

    #Province de liège
    # latitude = random.uniform(50.668157, 50.155765)
    # longitude = random.uniform(5.077769, 6.132183)


    from mymap.scripts import testAddItems
    from mymap.scripts import testDeleteItems
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(pk=7)
    testAddItems(1000, user)