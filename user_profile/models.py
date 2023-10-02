from django.db import models
from account.models import User
from django.utils.text import slugify

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.name

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    company_name = models.CharField(max_length=100)  
    slug = models.SlugField(max_length=150)
    description = models.TextField(max_length=1000) 
    created_at = models.DateField(auto_now_add=True)  
    headquarters = models.CharField(max_length=200)  
    website = models.URLField(blank=True)  
    company_logo = models.ImageField(upload_to = 'company-logo/', blank = True)
    
    def save(self, *args, **kwargs):
      self.slug = slugify(self.company_name)
      super(Company, self).save(*args, **kwargs)
      
      
    def __str__(self):
        return self.company_name
          
################ Add user Model ###########
class AddUserModel(models.Model):
  PERMISSION = (
    ('Read', 'Read'),
    ('Write', 'Write'),
    ('Admin', 'Admin'),
  )
  user = models.ForeignKey(User, on_delete= models.CASCADE)
  permission = models.CharField(max_length=50, choices=PERMISSION)
  
  def __str__(self):
      return self.user.email
  
  
  

  


