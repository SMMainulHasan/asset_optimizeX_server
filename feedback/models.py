from django.db import models
from account.models import User
# Create your models here.

class Feedbackmodel(models.Model):
  RATING = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  message = models.TextField(max_length=500)
  rating = models.CharField(max_length=50, choices=RATING)
  
  def __str__(self):
      return self.user.name
  