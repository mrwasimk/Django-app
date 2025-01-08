from django.contrib import admin
from .models import Issue
from .models import Module, Registration

admin.site.register(Issue)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credit', 'category') 
    search_fields = ('name', 'code')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'registerdate')
    search_fields = ('user__username', 'module__name')
    list_filter = ('registerdate', 'module')

# Register your models here.
