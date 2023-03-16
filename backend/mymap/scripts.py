import random

from django.contrib.auth import get_user_model

from .models import Item

User = get_user_model()


# Theses scripts are used to do scalability tests on the platform

def testAddItems(nb_items, user):
    for i in range(nb_items):
        name = 'Test Serializer ' + str(i)
        latitude = random.uniform(50.668157, 50.155765)
        longitude = random.uniform(5.077769, 6.132183)
        type = random.choice(['RQ', 'LN', 'DN'])
        location = 'SRID=4326;POINT (' + str(latitude) + ' ' + str(longitude) + ')'
        item = Item(
            name=name, description='Test description', location=location, user=user,
            type=type
        )
        item.save()


def testDeleteItems():
    Item.objects.filter(name__icontains='Test Serializer').delete()
