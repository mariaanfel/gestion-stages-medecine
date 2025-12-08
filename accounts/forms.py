from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, DoctorProfile, ChefServiceProfile, ResponsableHopitalProfile

class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Rôle")
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    class Meta:
        model = User
       
        fields = [
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        # on récupère l'objet User sans l’enregistrer tout de suite
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        # role est déjà pris en charge par le ModelForm, mais on peut forcer si tu veux :
        # user.role = self.cleaned_data["role"]

        if commit:
            user.save()
        return user

    


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field','placeholder': 'Nom d\'utilisateur'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field','placeholder': 'Mot de passe' })
    )
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["matricule", "cycle"]

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ["service"]

class ChefServiceProfileForm(forms.ModelForm):
    class Meta:
        model = ChefServiceProfile
        fields = ["service"]

class ResponsableHopitalProfileForm(forms.ModelForm):
    class Meta:
        model = ResponsableHopitalProfile
        fields = ["hopital"]