from organization.models import *
from rest_framework import serializers
from account.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator


########### addMember Serializer ######
class addMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = addMember
        fields = '__all__'

############ Organization Register Serializer ##################
class organigationRegisterSerializer(serializers.ModelSerializer):
    member = addMemberSerializer(many=True, read_only=True)
    class Meta:
        model = Organization
        fields = '__all__'
   
############# Active Register Organization ###############     
class registerOrganizationVerifySerializer(serializers.Serializer):
    def validate(self, attrs):
        uid = self.context.get('uid')
        token = self.context.get('token')
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id = id)
        organization_name = self.context.get('organization_name')
        org_name = smart_str(urlsafe_base64_decode(organization_name))
        
        organization = Organization.objects.get(organization_name=org_name)
        if organization is None:
          raise ValidationError('You are not a Register Organization')
        if user is not None:
            organization.is_company = True
            organization.save()
            user.save()
            return attrs
        else:
            raise ValidationError('Token is not Valid or Expired')
        

####### Member Active Serializer #######
class memberInvitedAcceptSerializer(serializers.Serializer):
  def validate(self, attrs):
    uid = self.context.get('uid')
    token = self.context.get('token')
    org_idd = self.context.get('org_id')
   
    id = smart_str(urlsafe_base64_decode(uid))
    org_id = smart_str(urlsafe_base64_decode(org_idd))
    user = User.objects.get(id = id)
    org = Organization.objects.get(id= org_id)  
    token = default_token_generator.check_token(user, token)
    add = addMember.objects.get(organization =org)
    
    if user is not None:
      add.is_company = True
      user.save()
      add.save()
      return attrs
    else:
      raise ValidationError('Token is not Valid or Expired')
