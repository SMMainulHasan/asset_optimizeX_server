from django.contrib import admin
from organization.models import *

# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('organization_name',)}
  list_display = ['organization_name', 'created_date', 'id']
 
class Member(admin.ModelAdmin):
  list_display = ['user']
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(addMember, Member)

