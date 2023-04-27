import json
from datetime import datetime

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point, GEOSGeometry, Polygon
from django.db.models import Q, F
from rest_framework import filters

from mymap.models import Item


class ActiveItemFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(enddate__isnull=True) | Q(enddate__gte=datetime.now()))


class ItemCategoryFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        categories = request.query_params.getlist('categories[]')
        if len(categories) > 0:
            return queryset.filter(
                Q(category1__in=categories) | Q(category2__in=categories) | Q(category3__in=categories)
            )
        return queryset


class ItemTypeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        types = request.query_params.getlist('types[]')
        if len(types) < len(Item.ItemType.choices): # Prevents filtering if all types are selected
            if len(types) > 0:
                return queryset.filter(type__in=types)
            else:
                return queryset.none()
        return queryset


class ItemViewFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        only_new = request.query_params.get('onlyUnseen') == "true"
        if only_new:
            return queryset.exclude(views__user=request.user)
        return queryset


class ItemAvailabilityFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        avf = request.query_params.get('availableFrom')
        avu = request.query_params.get('availableUntil')

        includeAfterAVF = (request.query_params.get('includeAfterAvailableFrom') == 'true')
        includeBeforeAVU = (request.query_params.get('includeBeforeAvailableUntil') == 'true')

        if avf:
            if includeAfterAVF:
                queryset = queryset.filter((Q(enddate__gt=avf) | Q(enddate__isnull=True)))
            else:
                queryset = queryset.filter(Q(startdate__lt=avf) & (Q(enddate__gt=avf) | Q(enddate__isnull=True)))
        if avu:
            if includeBeforeAVU:
                queryset = queryset.filter(startdate__lt=avu)
            else:
                queryset = queryset.filter(Q(startdate__lt=avu) & (Q(enddate__gt=avu) | Q(enddate__isnull=True)))

        return queryset


class ItemLocationFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user_location = request.query_params.get('userLocation')
        distances_radius = request.query_params.getlist('distancesRadius[]')
        if user_location is not None:
            user_location = json.loads(user_location)
            user_location = Point(user_location['longitude'], user_location['latitude'], srid=4326)
            queryset = queryset.annotate(distance=Distance("location", user_location))

            if len(distances_radius) == 2:
                distances_radius = [int(distance) for distance in distances_radius]
                min_distance = min(distances_radius) * 1000
                max_distance = max(distances_radius) * 1000
                queryset = queryset.filter(Q(distance__gte=min_distance, distance__lte=max_distance) | Q(distance__isnull=True))

            ordering = request.query_params.get('ordering')
            if ordering == 'distance':
                queryset = queryset.order_by(F('distance').asc(nulls_last=True))
            if ordering == '-distance':
                queryset = queryset.order_by(F('distance').desc(nulls_last=True))
        return queryset


class ItemMinCreationdateFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_creationdate = request.query_params.get('minCreationdate')
        if min_creationdate:
            return queryset.filter(creationdate__gte=min_creationdate)
        return queryset


class ItemMapBoundsFilterBackend(filters.BaseFilterBackend):
    bbox_margins_ratio = 0.2

    def filter_queryset(self, request, queryset, view):
        bounds = request.query_params.getlist('bounds[]')
        if len(bounds) > 0:
            NW = GEOSGeometry(bounds[0])
            SE = GEOSGeometry(bounds[1])

            longitude_min=NW.coords[0]
            longitude_max=SE.coords[0]
            latitude_min=SE.coords[1]
            latitude_max=NW.coords[1]

            diff_longitude = abs(longitude_max - longitude_min)
            diff_latitude = abs(latitude_max - latitude_min)
            longitude_margin = diff_longitude * self.bbox_margins_ratio
            latitude_margin = diff_latitude * self.bbox_margins_ratio

            bbox = Polygon.from_bbox([
                longitude_min - longitude_margin,
                latitude_min - latitude_margin,
                longitude_max + longitude_margin,
                latitude_max + latitude_margin
            ])

            return queryset.filter(location__coveredby=bbox)
        return queryset


class ConversationContentFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('search')
        if search is not None and search != "":
            return queryset.filter(
                Q(item__name__icontains=search) | Q(item__description__icontains=search)
            )
        return queryset


class ConversationSelectedCategoryFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        selectedCategory = request.query_params.get('selectedCategory')
        if selectedCategory is not None:
            if selectedCategory == 'asked':
                return queryset.filter(starter=request.user)
            elif selectedCategory == 'yours':
                return queryset.filter(item__user=request.user)
        return queryset


class UserItemFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.query_params.get('id')
        if user is not None and user != "":
            return queryset.filter(user_id=int(user))
        return queryset.filter(user=request.user)
