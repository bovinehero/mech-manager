""" Contains the form definitions for the webapp """
# django imports occur at runtime, so fail linter
# pylint:disable=import-error
from django import forms
# pylint:enable=import-error
from .models import Mech


class CreateMechForm(forms.ModelForm):
    """
    Defines the form used to create a new mech
    """
    class Meta:
        """
        Django defined Class used to define what the form can render
        """
        model = Mech
        fields = [
            'name',
            'category',
            'weight',
            'tech_level',
            'role',
            'description',
            'record_sheet',
            'battle_value',
            'status'
        ]


class UpdateMechForm(forms.ModelForm):
    """
    Defines the form used to edit an existing mech
    """
    class Meta:
        """
        Django defined Class used to define what the form can render
        """
        model = Mech
        fields = [
            'name',
            'category',
            'weight',
            'tech_level',
            'role',
            'description',
            'record_sheet',
            'battle_value',
            'status'
        ]
