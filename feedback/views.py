from django.shortcuts import render
from rest_framework import views, response, permissions
from feedback.models import Feedbackmodel
from feedback.serializers import feedbackSerializers
from account.renders import UserRenderer

# Create your views here.
class FeedbackView(views.APIView):
  # permission_classes= [permissions.IsAuthenticated]
  # renderer_classes = [UserRenderer]
  def post(self, request):
      serializer = feedbackSerializers(data=request.data)
      
      serializer.is_valid(raise_exception=True)
      print(serializer)
      user = request.user
      message = serializer.data.get('message')
      rating = serializer.data.get('rating')
      if user == 'AnonymousUser':
        return response.Response({'message':"Authentication required"})
      
      feedback = Feedbackmodel.objects.create(user=user, message=message, rating=rating)
      feedback.save()
      serializer.save()
      
      print(user, message, rating)
      return response.Response({'message':"Thank you for providing your Feedback."})

