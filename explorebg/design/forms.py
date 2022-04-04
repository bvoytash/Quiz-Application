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