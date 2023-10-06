from rest_framework import filters
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from .models import Library
from .serializers import CreateLibrarySerializer


class CreateLibraryAPIView(CreateAPIView):
    queryset = Library.objects.all()
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['library_name', 'description']

class LibraryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Library.objects.all()
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['library_name', 'description']

class ListLibraryAPIView(ListAPIView):
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['library_name', 'description']

    def get_queryset(self):
        org_id = self.kwargs.get('org_id')
        return Library.objects.filter(organization__id=org_id)
