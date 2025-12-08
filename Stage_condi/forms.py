from django import forms
from .models import OffreStage
from .models import Candidature, Evaluation
from django.contrib.auth import get_user_model

User = get_user_model()

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
        # on n'affiche pas les champs gérés automatiquement
        exclude = ["archive", "created_at", "superviseur"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # optionnel : filtrer pour ne montrer que les médecins (role == "doctor")
        self.fields["medecin_responsable"].queryset = User.objects.filter(role="doctor")
        self.fields["medecin_responsable"].required = False

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["note", "commentaire"]
        widgets = {
            "note": forms.NumberInput(attrs={"min": 0, "max": 20}),  # adapte l'échelle
            "commentaire": forms.Textarea(attrs={"rows": 4}),
        }
