import json
from datetime import datetime, timezone

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Q, F
from rest_framework import filters


class ItemTypeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        types = request.query_params.getlist('types[]')
        if len(types) > 0:
            return queryset.filter(type__in=types)
        return queryset


class ItemViewFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        only_new = request.query_params.get('onlyNew') == "true"
        if only_new:
            return queryset.exclude(item_views__user=request.user)
        return queryset


class ItemAvailabilityFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        available_from = request.query_params.get('availableFrom')
        available_until = request.query_params.get('availableUntil')

        if available_from:
            if available_until:
                queryset = queryset.filter((Q(startdate__gte=available_from) & Q(startdate__lte=available_until)) | (Q(startdate__lt=available_from) & Q(enddate__isnull=True)))
                queryset = queryset.filter((Q(enddate__gte=available_from) & Q(enddate__lte=available_until)) | Q(enddate__isnull=True))
            else:
                queryset = queryset.filter(Q(enddate__gte=available_from) | (Q(startdate__lt=available_from) & Q(enddate__isnull=True)))
        elif available_until:
            queryset = queryset.filter(Q(enddate__lte=available_until) | (Q(startdate__gte=datetime.now(timezone.utc)) & Q(enddate__isnull=True)))
        return queryset


class ItemLocationFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user_location = request.query_params.get('userLocation')
        distances_radius = request.query_params.getlist('distancesRadius[]')
        if user_location is not None:
            user_location = json.loads(user_location)
            user_location = Point(user_location['longitude'], user_location['latitude'], srid=4326)
            queryset = queryset.annotate(distance=Distance("location", user_location))

            if len(distances_radius) > 0:
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


class ItemCategoryFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        categories = request.query_params.getlist('categories[]')
        if len(categories) > 0:
            return queryset.filter(
                Q(category1__in=categories) | Q(category2__in=categories) | Q(category3__in=categories)
            )
        return queryset


class ActiveItemFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(enddate__isnull=True) | Q(enddate__gte=datetime.now()))


class UserItemFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.query_params.get('id')
        if user is not None and user != "":
            return queryset.filter(user_id=int(user))
        return queryset.filter(user=request.user)
