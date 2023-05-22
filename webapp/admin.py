from django.contrib import admin
from .models import Mech

@admin.register(Mech)
class MechAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'weight',
        'tech_level',
        'role',
        'record_sheet',
        'battle_value',
        'status',
        'image'
        ) 
    search_fields = ['type', 'tech_level']
    list_filter = ('tech_level', )
    actions = ['approve_mech', 'revoke_mech']
    prepopulated_fields = {'slug': ('name',)}

    def approve_mech(self, request, queryset):
        queryset.update(status=True)
    
    def revoke_mech(self, request, queryset):
        queryset.update(status=False)