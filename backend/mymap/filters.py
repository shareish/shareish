from datetime import datetime

from django.db.models import Q
from django.contrib.postgres import search
from rest_framework import filters


class ItemTypeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        type = request.query_params.get('type')
        if type is not None and type != "":
            return queryset.filter(type=type)
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
        category = request.query_params.get('category')
        if category is not None and category != "":
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
        if user is not None and user != "":
            return queryset.filter(user_id=int(user))
        else:
            return queryset.filter(user=request.user)
