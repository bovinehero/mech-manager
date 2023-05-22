from django import forms
from .models import Mech

class CreateMechForm(forms.ModelForm):
    
    class Meta:
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
    
    class Meta:
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