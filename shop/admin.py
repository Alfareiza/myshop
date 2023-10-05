from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    # Any attr which is in the list_editable, have to be in list_display
    # These fielfs will be in the admin
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']

    # Allow to filter the products by
    list_filter = ['available', 'created', 'updated']

    # Allow to edit those attributes in multiple lines at the time
    list_editable = ['price', 'available']

    # Pre fill these fields
    prepopulated_fields = {'slug': ('name',)}
