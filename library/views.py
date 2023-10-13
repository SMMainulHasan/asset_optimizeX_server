from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, views, status
from account.models import User

from account.renders import UserRenderer
from .models import Library
from .serializers import CreateLibrarySerializer
from uploadAsset.models import uploadAsset

class CreateLibraryAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def post(self, request):
        serializer = CreateLibrarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
    
# class CreateLibraryAPIView(CreateAPIView):
#     queryset = Library.objects.all()
#     serializer_class = CreateLibrarySerializer
#     permission_classes = [IsAuthenticated]
    

class LibraryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Library.objects.all()
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]

# class ListLibraryAPIView(ListAPIView):
    # serializer_class = CreateLibrarySerializer
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     org_id = self.kwargs.get('org_id')
    #     lib  = Library.objects.filter(organization__id=org_id)
    #     list_lib = []
    #     for i in lib:
    #         lib_r={}
    #         lib_r['id'] = i.id
    #         lib_r['library_name'] = i.library_name
    #         lib_r['description'] = i.description
    #         lib_r['organization'] = i.organization
    #         list_lib.append(lib_r)
    #         # print(i.id,"<<<<")
    #     # print(org_id, lib , "<<<<<<<<<")
    #     print(list_lib)
    #     return  list_lib




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
            lib_r['organization'] = i.description
            list_lib.append(lib_r)
            
        return response.Response(list_lib)

from organization.models import Organization
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
        
        photo = {}  
        photo['total_img'] = len(temp)
        temp.append(photo)
        print(temp)           
        return response.Response(temp, status=status.HTTP_200_OK)
        
        # lib = Library.objects.filter(organization__id = org_id)    
        # photo = []   
        # for i in lib:
        #     asset = uploadAsset.objects.filter(library = i.id)          
        #     for j in asset:
        #         tem = {}
        #         tem['id'] = j.id
        #         tem['title'] = j.title
        #         tem['asset'] = j.asset.url
        #         photo.append(tem)
        # tem = {}
        # tem['total_img'] = len(photo)
        # photo.insert(0, tem)
        # print(photo)                                               
        # return response.Response(photo, status=status.HTTP_200_OK)

        
        # return response.Response({"message": "You are not access this organization"}, status=status.HTTP_400_BAD_REQUEST)
