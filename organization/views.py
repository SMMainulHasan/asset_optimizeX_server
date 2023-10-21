from django.shortcuts import render
from organization.serializers import *
from account.renders import UserRenderer
from account.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator
from account.utils import Util
from organization.models import *
from rest_framework import status, generics, views, viewsets, permissions, response

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from organization.ssl import sslcommerz_payment_gateway
import random

######### payment Gateway method ###########
@method_decorator(csrf_exempt, name='dispatch')
class successView(views.APIView):
  # permission_classes = [permissions.IsAuthenticated]
  def post(self, request):
    # user_id = request.user
    data = request.data
    user_id = int(data['value_b'])
    org_id = int(data['value_c'])
    amount = int(data['value_d'])
    user = User.objects.get(pk=user_id)
    org = Organization.objects.get(pk = org_id)
    
    payment = Payment(
        user = user,
        organization=org,
        payment_id =data['tran_id'],
        payment_method = data['card_issuer'],
        amount_paid= amount,
        status =data['status'],
    )
    payment.save()
    
    order = Order.objects.get(user=user, is_ordered=False, order_number=int(data['value_a']))
    
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    org = Organization.objects.get(id= org_id)
    user = User.objects.get(id = user_id)
    premium = premiumOrder()
    premium.organization = org
    premium.payment = payment
    premium.user = user 
    premium.ordered = True
    premium.save()
    org.premiumUser = True
    org.save()
    lst = []
    lst.append(payment.user)
    lst.append(payment.organization)
    lst.append(payment.payment_id)
    lst.append(payment.payment_method)
    lst.append(payment.amount_paid)
    lst.append(payment.status)
    return response.Response(status=status.HTTP_200_OK)


########## Permium button Click #########
class PlaceOrderPremiumView(views.APIView):
  permission_classes = [permissions.IsAuthenticated]
  
  def post(self, request, pk):
    user = request.user
    try:
      org = Organization.objects.get(pk=pk)
      if org.premiumUser == True:
        return response.Response("Alread You are Premium User")
      order = Order.objects.create(user=request.user, organization=org, is_ordered= False)

      order.order_number = order.id
      # sslcommerz_payment_gateway(request,order.id, pk, request.user.id)
      lst = {}
      lst['order_id'] = order.id 
      lst['org_id'] = pk
      lst['user_id'] = request.user.id
      lst['amount'] = 1000
      order.save()
      payment_url = sslcommerz_payment_gateway(request, order.id, pk, request.user.id, 1000)
      return response.Response(payment_url)
    except Organization.DoesNotExist:
      return response.Response('Organization Error')      
        

############## Register Organization #################
class OrganizationRegisterView(viewsets.ModelViewSet):
  permission_classes = [permissions.IsAuthenticated]
  renderer_classes = [UserRenderer]
  queryset = Organization.objects.all()
  serializer_class = organigationRegisterSerializer
  
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data = request.data)
    if serializer.is_valid():
      serializer.save(owner = self.request.user)
      user = self.request.user
      uid = urlsafe_base64_encode(force_bytes(user.id))
      token = default_token_generator.make_token(user)
      organization_name =  serializer.data.get('organization_name')    
      organization_name = urlsafe_base64_encode(force_bytes(organization_name))   
            
      link = "http://localhost:5173/api/organization/register/"
      print("uid", uid, " Token", token, " link", link, 'organizationName', organization_name)
      body = 'Click Following link to Active Your Account ' + link +  uid + '/'+ token + '/' + organization_name
      data = {
        'subject':'Active Your Account',
        'body':body,
        'to_email':user.email,
      }
      Util.send_email(data)

      return response.Response({'message':'Check mail Active Your Organization'}, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
############## Active Organization ##################
class registerOrganizationVerify(views.APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token,organization_name, format = None):
    serializer = registerOrganizationVerifySerializer(data=request.data, context = {'uid':uid, 'token':token, 'organization_name':organization_name})
    if serializer.is_valid(raise_exception=True):

      return response.Response({
        'message':'Organization Account Active Successfully'
      })
    return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
          
############## Organization Update  View ###############
class organizationUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Organization.objects.all()
    serializer_class = organizationUpdateSerializer
 
############## Organization Delete  View ###############
class organizationDeleteView(generics.DestroyAPIView):
  permission_classes = [permissions.IsAuthenticated]
  queryset = Organization.objects.all()
  serializer_class = organigationRegisterSerializer


############ Organization Get ##########
class OrganizationTotal(views.APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):   
      owner_organization = Organization.objects.filter(owner=request.user)
      owner_organization_data = []
      for i in owner_organization:
        if i.is_company == True:
          dic = {}
          dic['id'] = i.id
          dic['organization_name'] = i.organization_name
          owner_organization_data.append(dic)
          
      member_organization_data = []     
      member_organizations = addMember.objects.filter(user =request.user)
      print(member_organizations)
      for i in member_organizations:
        org = Organization.objects.filter(id = i.organization_id)
        dic = {}
        if i.is_company == True:
          dic['role'] = i.role
          for j in org:
            dic['id'] = j.id
            dic['organization_name'] = j.organization_name
          member_organization_data.append(dic)
      
    
      return response.Response({
          'owner_organizations': owner_organization_data,
          'member_organizations': member_organization_data,
          })  

########### Organization MemberAll ########
class OrganizationMember(views.APIView):
  permission_classes = [permissions.IsAuthenticated]
  
  def get(self, request, org_id):
    try:
      org = Organization.objects.get(id = org_id)
      
      lst = []
      k = 0
      dic = {}
      for i in org.member.all():
        k = i.id        
        lst.append(i.email)
        # print(i.rol
      member = addMember.objects.filter(organization__member = k)
     
      j = 0
      for i in member: 
        ls = []
        ls.append(i.role)
        ls.append(i.is_company)
        dic[lst[j]] = ls
        j+=1
      print(dic)
      return response.Response(dic,status=status.HTTP_200_OK)
    except Organization.DoesNotExist:
      return response.Response("Orgnization information not valid")
  
########### Organization Member Remove ###### 
class MemberRemoveView(generics.DestroyAPIView):
    queryset = addMember.objects.all()
    serializer_class = addMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')    
        print(pk)
        try:   
            member_id = addMember.objects.get(pk = pk)
            print(member_id.email)
          
            member_id.delete()
            return response.Response({'message':'Delete Successfully'})
        except addMember.DoesNotExist:
            return response.Response({
                'message':'Not valid asset'
            })

          
########### Organization Member Request View #######
class addMemberView(views.APIView):
  permission_classes= [permissions.IsAuthenticated]
  renderer_classes = [UserRenderer]
  def post(self, request):
    serializer = addMemberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    role = serializer.data.get('role')
    organization_name = serializer.data.get('organization')
    
    
    org_m = addMember.objects.filter(organization__organization_name = organization_name)
    for i in org_m:
      if i.user == request.user:
        if i.role == 'Contributor' or i.role == 'Consumer':
          print(i.role)
          return response.Response({"msg": "Your are not access this organization add user option"})
    try:
      user = User.objects.get(email=email)
      if request.user == user:
        return response.Response("Not Valid Email")
      try:
        organization = Organization.objects.get(organization_name=organization_name)
        if organization.owner == user:
          return response.Response({
            "msg":"This user Organization Owner you are not invited request"
          })
        th = organization.member.all()
        for i in th:
          if i.email == email:
            return response.Response("This user Already added")       
        member = addMember.objects.create(user=user, organization=organization, email=email, role=role, is_company=False)
        member.save()
        organization.save()
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        org_name = urlsafe_base64_encode(force_bytes(organization_name))
        link = "http://localhost:5173/api/organization/add-user/"
        print("uid", uid, " Token", token, " link", link)
        body = 'Click Following link to confirm invited accepted ' + link +  uid + '/'+ token + '/' + org_name
        data = {
          'subject':'Invited Request',
          'body':body,
          'to_email':email,
        }
        Util.send_email(data)
        
        return response.Response({'message':"Invited Link send."})
        
      except Organization.DoesNotExist:
        return response.Response({'msg':"Organization not register"})
    except User.DoesNotExist:
      return response.Response({"msg":"user not register"})
         
#  ############## Active Organization ##################
class invitedActive(views.APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token,org_name, format = None):
    serializer = memberInvitedAcceptSerializer(data=request.data, context = {'uid':uid, 'token':token, 'org_name':org_name})
    if serializer.is_valid(raise_exception=True):
      
      return response.Response({
        'massage':'Invited request Confirm Successfully'
      })
    return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    
      