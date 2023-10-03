from django.db import models

from category.models import Category
from library.models import Library
from organization.models import Organization


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class uploadAsset(models.Model):
  library = models.ForeignKey(Library, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=500)
  file_type = models.FileField(upload_to='images/company/asset/')# <<--------
  created_at = models.DateTimeField(auto_now_add= True)
  updated_at = models.DateTimeField(auto_now_add= True)
  tags = models.ManyToManyField(Tag, blank=True) #Need to work
  location = models.CharField(max_length=200)
  comment = models.CharField(max_length=300)
  
  def __str__(self):
      return self.title
  
  
  

