

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Étudiant"),
        ("doctor", "Médecin"),
        ("chef", "Chef de service"),
        ("responsable", "Responsable hôpital"),
        ("admin", "Administrateur"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    def __str__(self):
        # get_role_display() affiche le label "Étudiant", "Médecin", etc.
        return f"{self.username} ({self.get_role_display()})"
 
 
# Profil Etudiant
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20)
    cycle = models.CharField(max_length=100)
    def __str__(self):
        return f"Profil étudiant de {self.user.username}"

# Profil Médecin
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.CharField("Service", max_length=100, blank=True, null=True)
    def __str__(self):
        return f"Profil médecin de {self.user.username}"

# Profil Chef de service
class ChefServiceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=100)
    def __str__(self):
        return f"Profil chef de service de {self.user.username}"

# Profil Responsable hôpital
class ResponsableHopitalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hopital = models.CharField(max_length=150)
    def __str__(self):
        return f"Profil responsable hôpital de {self.user.username}"


