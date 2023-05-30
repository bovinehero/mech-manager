""" Contains the admin registration for the app """
# django imports occur at runtime, so fail linter
# pylint:disable=import-error
from django.contrib import admin
# pylint:enable=import-error
from .models import Mech


@admin.register(Mech)
class MechAdmin(admin.ModelAdmin):
    """
    Enables Mech model to be displayed in the admin app
    """
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

    # request var is pushed from website
    # pylint:disable=unused-argument
    def approve_mech(self, request, queryset):
        """
        Enables approve mech action in Mechs
        """
        queryset.update(status=True)

    def revoke_mech(self, request, queryset):
        """
        Enables revoke mech action in Mechs
        """
        queryset.update(status=False)
    # pylint:disable=unused-argument
