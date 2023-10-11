from rest_framework import serializers

from library.models import Library
from organization.models import Organization
from xml.dom import ValidationErr

from rest_framework.response import Response
class CreateLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['library_name', 'description', 'organization']
    
    def validate(self, attrs):
        library_name = attrs.get('library_name')
        description = attrs.get('description')
        organization = attrs.get('organization')
        try:
            dup = Library.objects.get(organization=organization)          
            if library_name == dup.library_name:
                raise serializers.ValidationError("This library name already create")
            return attrs
        except Library.DoesNotExist:
            return attrs
        
        
    