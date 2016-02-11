from django.contrib import admin
from .models import SetupModule

# Register your models here.


class SetupModuleAdmin(admin.ModelAdmin):
    fieldsets = [
        ['command', {'fields': ['command']}],
        ['hosts', {'fields': ['hosts']}],
        ['groups', {'fields': ['groups']}],
    ]
    filter_horizontal = ['hosts', 'groups']


admin.site.register(SetupModule, SetupModuleAdmin)
