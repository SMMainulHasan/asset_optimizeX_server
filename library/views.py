from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, views, status
from account.models import User
from organization.models import *
from account.renders import UserRenderer
from .models import Library
from .serializers import CreateLibrarySerializer
from uploadAsset.models import uploadAsset

class CreateLibraryAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def post(self, request):
        serializer = CreateLibrarySerializer(data=request.data, context = {'user':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
###### Library Update View #######
class LibraryUpdateView(UpdateAPIView):
    queryset = Library.objects.all()
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]
    
##### Library Delete View ######
class LibraryDeleteView(DestroyAPIView):
    queryset = Library.objects.all()
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]

class ListLibraryAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, org_id):   
        lib = Library.objects.filter(organization__id=org_id)
        list_lib = []
        for i in lib:
            lib_r = {}
            lib_r['id'] = i.id
            lib_r['library_name'] =i.library_name
            lib_r['description'] = i.description
            org = Organization.objects.get(organization_name=i.organization)
            lib_r['org_id'] = org.id
            lib_r['org_name'] = org.organization_name
            list_lib.append(lib_r)
       
            
        return response.Response(list_lib)


######## Organization All Asset Showing  ############
class assetAllImageView(views.APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    def get(self, request, org_id): 
        org_owner = Organization.objects.filter(owner=request.user)
        org_member = Organization.objects.filter(member=request.user)
        temp = [] 
       
        if org_owner.exists():
            print(org_owner)
            for i in org_owner:
                if i.id == org_id:
                    lib = Library.objects.filter(organization__id = org_id)      
                    for k in lib:
                        asset = uploadAsset.objects.filter(library = k.id)          
                        for j in asset:
                            tem = {}
                            tem['id'] = j.id
                            tem['title'] = j.title
                            tem['asset'] = j.asset.url
                            temp.append(tem)
        
        if  org_member.exists():   
       
            for i in org_member:
                if i.id == org_id:
                    lib = Library.objects.filter(organization__id = org_id)    
                    for k in lib:
                        asset = uploadAsset.objects.filter(library = k.id)          
                        for j in asset:
                            tem = {}
                            tem['id'] = j.id
                            tem['title'] = j.title
                            tem['asset'] = j.asset.url
                            temp.append(tem)
        
        total_img = {}  
        total_img['total_img'] = len(temp)
        lstt = []
        lstt.append(total_img)
        print(temp)           
        print(temp)
        return response.Response({'len':lstt, 
                                  'asset': temp}, status=status.HTTP_200_OK)
        
        
