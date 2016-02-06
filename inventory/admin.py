from django.contrib import admin
from .models import Host, Group, HostVar, GroupVar
# Register your models here.


class HostVarInline(admin.TabularInline):
    model = HostVar
    extra = 1


class HostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['ansible_alias']}),
    ]
    inlines = [HostVarInline]


class GroupVarInline(admin.TabularInline):
    model = GroupVar
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['ansible_group']}),
        ('ansible_hosts',  {'fields': ['ansible_hosts'], 'classes': ['collapse']}),
        ('ansible_children',  {'fields': ['ansible_children'], 'classes': ['collapse']}),
    ]
    inlines = [GroupVarInline]
    filter_horizontal = ('ansible_hosts', 'ansible_children')


admin.site.register(Host, HostAdmin)
admin.site.register(Group, GroupAdmin)
