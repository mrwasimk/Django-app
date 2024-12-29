from django.contrib import admin
from .models import Issue
from .models import Module

admin.site.register(Issue)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credit', 'category')  # Columns to display in the admin
    search_fields = ('name', 'code')
# Register your models here.
