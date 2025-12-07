from django import forms
from .models import OffreStage
from .models import Candidature

class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ["cv", "lettre_motivation"]

        widgets = {
            "lettre_motivation": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Expliquez pourquoi vous postulez…"
            })
        }

class OffreStageForm(forms.ModelForm):
    class Meta:
        model = OffreStage
        
        exclude = ['archive', 'created_at', 'superviseur']

