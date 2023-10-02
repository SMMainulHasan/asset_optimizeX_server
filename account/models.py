from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')
      
      user = self.model(
          email=self.normalize_email(email),
          name=name,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, phone_number, password=None ):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
      )
      user.is_admin = True
      user.is_staff = True
      user.is_superuser = True
      user.save(using = self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  phone_number = models.CharField(max_length=50)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  tc = models.BooleanField(blank=False, null=False, default=False)
  image = models.ImageField(upload_to = 'images/account/', null=False, blank = False, default='profile_pics/profile.jpg')

  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_superadmin = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name','phone_number']
  
  objects = UserManager()
  
  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True


# from django.db import models
# from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# #  Custom User Manager
# class UserManager(BaseUserManager):
#   def create_user(self,name, email, phone_number,  tc, password=None, password2=None):
#       """
#       Creates and saves a User with the given email, name, tc and password.
#       """
#       if not email:
#           raise ValueError('User must have an email address')

#       user = self.model(
#           email=self.normalize_email(email),
#           name=name,
#           phone_number = phone_number,
#           tc=tc,
#       )

#       user.set_password(password)
#       user.save(using=self._db)
#       return user

#   def create_superuser(self,name, email, phone_number,  tc, password=None):
#       """
#       Creates and saves a superuser with the given email, name, tc and password.
#       """
#       user = self.create_user(
#           email,
#           password=password,
#           name=name,
#           tc=tc,
#           phone_number=phone_number,
#       )
#       user.is_admin = True
#       user.is_staff = True
#       user.is_superuser = True
#       user.is_active = True
#       user.save(using=self._db)
#       return user

# #  Custom User Model
# class User(AbstractBaseUser):
#   email = models.EmailField(
#       verbose_name='Email',
#       max_length=255,
#       unique=True,
#   )
#   name = models.CharField(max_length=200)
#   phone_number = models.CharField(max_length=11)
#   tc = models.BooleanField()
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)
#   image = models.ImageField(upload_to = 'images/account/', null=False, blank = False, default='images/account/profile.jpg')
  
#   is_admin = models.BooleanField(default=False)
#   is_staff = models.BooleanField(default=False)
#   is_active = models.BooleanField(default=True)
#   is_superadmin = models.BooleanField(default=False)

#   objects = UserManager()

#   USERNAME_FIELD = 'email'
#   REQUIRED_FIELDS = ['name', 'tc']

#   def __str__(self):
#       return self.email

#   def has_perm(self, perm, obj=None):
#       "Does the user have a specific permission?"
#       # Simplest possible answer: Yes, always
#       return self.is_admin

#   def has_module_perms(self, app_label):
#       "Does the user have permissions to view the app `app_label`?"
#       # Simplest possible answer: Yes, always
#       return True









