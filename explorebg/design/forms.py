from django import forms

from explorebg.design.models import Design


class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['name', 'design_image']


class EditDesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'size': '30',
                    'style': 'border: solid; border-color:green; border-radius: 10px; font-size: 100%;' 'font: bold;',
                }
            ),
        }
