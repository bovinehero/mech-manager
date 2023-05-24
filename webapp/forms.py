from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
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