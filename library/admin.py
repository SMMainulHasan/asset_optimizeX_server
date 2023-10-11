from django.contrib import admin
from .models import Library

# Register your models here.

class LibraryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('library_name',)}
  list_display = ['library_name', 'created_date', 'id']
admin.site.register(Library, LibraryAdmin)