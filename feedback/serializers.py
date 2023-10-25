from rest_framework import serializers
from feedback.models import Feedbackmodel

class feedbackSerializers(serializers.Serializer):
  message = serializers.CharField(max_length=500)
  rating  = serializers.CharField(max_length = 50)
  class Meta:
    # model = Feedbackmodel
    fields = ['message', 'rating']

