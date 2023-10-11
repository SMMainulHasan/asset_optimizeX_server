from rest_framework import serializers
from .models import uploadAsset,AssetVersion, AssetFile

class assetFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetFile
        fields = ['id', 'uploadasset', 'asset']
        
        
class uploadAssetSerializer(serializers.ModelSerializer):
    asset = assetFileSerializer(many=True, read_only=True)
    upload_asset = serializers.ListField(
        child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True)
    class Meta:
        model = uploadAsset
        fields = ['id', 'organization', 'title', 'library', 'description', 'asset', 'upload_asset', 'location']
        
    def create(self, validated_data):
        uploaded_data = validated_data.pop('upload_asset')
        upload_asset = uploadAsset.objects.create(**validated_data)
        for upload_item in uploaded_data:
            new_asset = AssetFile.objects.create(uploadasset=upload_asset, asset=upload_item)
        return upload_asset
            

class PreviousVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetVersion
        fields = ('id','asset', 'created_at')  # Define the fields you want to include in the response

class CurrentAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = uploadAsset
        fields = ('id', 'asset', 'created_at') 
     
#all asset        
class AssetVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetVersion
        fields = ('id', 'title', 'asset', 'created_at')         