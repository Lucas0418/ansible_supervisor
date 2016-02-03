from django.contrib import admin
from .models import Host, Group, Var
# Register your models here.

class VarInline(admin.TabularInline):
    model = Var
    extra = 1

class HostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['ansible_alias']}),
        ('Data information',  {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [VarInline]

admin.site.register(Host, HostAdmin)
admin.site.register(Group)
#admin.site.register(Var)
