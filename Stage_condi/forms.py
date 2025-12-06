from django import forms
from .models import OffreStage

class OffreStageForm(forms.ModelForm):
    class Meta:
        model = OffreStage
        fields = '__all__'
        exclude = ['archive', 'created_at']
