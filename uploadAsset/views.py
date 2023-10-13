from django.db.models import Q
from rest_framework import filters, generics, status, views, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.renders import UserRenderer
from library.models import Library

from .models import AssetVersion, uploadAsset
from .serializers import (AssetVersionSerializer, CurrentAssetSerializer,
                          PreviousVersionSerializer, uploadAssetSerializer)


class AssetListsCreateView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        flag = 1
        arr = []
        form_data = {}
        title = request.data.get('title')
        library = request.data.get('library')
        location = request.data.get('location')
        form_data['title'] = title
        form_data['library'] = library
        form_data['location'] = location
        
        for img in request.FILES.getlist('asset'):
            print(img)
            form_data['asset'] = img
           
            serializer = uploadAssetSerializer(data=form_data)
            if serializer.is_valid():
                serializer.save()
                arr.append(serializer.data)
            else:
                flag = 0
        if flag == 1:
            return Response({
                'Data':arr
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message' : 'Error!',
        }, status=status.HTTP_400_BAD_REQUEST)   
        

# class AssetListCreateView(generics.ListCreateAPIView):
#     serializer_class = uploadAssetSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['title', 'description', 'tags__tag_name']  # Include tags in search_fields

#     def get_queryset(self):
#         # Get the library_id from the URL parameter
#         library_id = self.kwargs.get('library_id')
#         search_query = self.request.query_params.get('search', '')

#         if library_id is None:
#             # Return a response with an error message if library_id is missing
#             return Response({'error': 'Library ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         queryset = uploadAsset.objects.filter(library_id=library_id)
        
#         if search_query:
#             # Use Q objects to perform case-insensitive search on multiple fields
#             queryset = queryset.filter(
#                 Q(title__icontains=search_query) |
#                 Q(description__icontains=search_query) |
#                 Q(tags__tag_name__icontains=search_query)
#             )
            
#         return queryset

class AssetListCreateView(generics.ListCreateAPIView):
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags__tag_name']  # Include tags in search_fields

    def get_queryset(self):
        # Get the library_id from the URL parameter
        library_id = self.kwargs.get('library_id')
        search_query = self.request.query_params.get('search', '')
        
        if library_id is None:
            # Return a response with an error message if library_id is missing
            return Response({'error': 'Library ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # if search_query:
        #     # Use Q objects to perform case-insensitive search on multiple fields
        #     queryset = queryset.filter(
        #         Q(title__icontains=search_query) |
        #         Q(description__icontains=search_query) |
        #         Q(tags__tag_name__icontains=search_query)
        #     )
        
        user = self.request.user
        org = Library.objects.filter(organization__owner = user)
        
        for i in org:
            if i.id == library_id:     
                queryset = uploadAsset.objects.filter(library_id=library_id)
                return queryset
        org_m = Library.objects.filter(organization__member = user)
        for i in org_m:
            if i.id == library_id:
                queryset = uploadAsset.objects.filter(library_id=library_id)
                print(queryset)
                return queryset

class AssetRetrieveView(generics.RetrieveAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]
    
        

class AssetUpdateView(generics.UpdateAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]

class AssetDeleteView(generics.DestroyAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]


#asset version control views.....

class PreviousAssetVersionsView(generics.ListAPIView):
    serializer_class = PreviousVersionSerializer

    def get_queryset(self):
        # Get the asset_id from the URL parameter
        asset_id = self.kwargs['asset_id']

        # Retrieve the asset instance
        try:
            asset_instance = uploadAsset.objects.get(id=asset_id)
        except uploadAsset.DoesNotExist:
            asset_instance = None

        # If the asset instance is found, return its previous versions
        if asset_instance:
            return asset_instance.versions.all()
        else:
            return AssetVersion.objects.none()
    
    # def get_queryset(self):
    #     asset_id = self.kwargs.get('asset_id')

    #     if asset_id is None:
    #         # Return a response with an error message if library_id is missing
    #         return Response({'error': 'assert_id ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     queryset = AssetVersion.objects.filter(id=asset_id)
    #     return queryset

class CurrentAssetView(generics.RetrieveAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = CurrentAssetSerializer        

class AssetVersionListView(generics.ListAPIView):
    queryset = AssetVersion.objects.all()
    serializer_class = AssetVersionSerializer