from django.contrib import admin
from .models import Category, Hierarchy
# from tinymce.widgets import TinyMCE
from django.db import models

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Category/Parent", {"fields": ["category_name", "category_parent"]}),
        ("Date/Author", {"fields": ["created_by", "create_date"]}),
        ("Description", {"fields": ["hierarchy", "description"]}),
        ("Image", {"fields": ["image_description", "image_address"]}),
    ]

    # formfield_overrides = {
    #     models.TextField: {'widget': TinyMCE()},
    # }   


admin.site.register(Category, CategoryAdmin)
admin.site.register(Hierarchy)