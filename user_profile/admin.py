from django.contrib import admin
from user_profile.models import Company, UserProfile, AddUserModel
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('company_name',)}
  list_display = ['company_name', 'created_at']
  

admin.site.register(AddUserModel)


admin.site.register(UserProfile)
admin.site.register(Company, CompanyAdmin)

