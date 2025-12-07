

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
 
 
# Profil Etudiant
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20)
    cycle = models.CharField(max_length=100)

# Profil Médecin
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)

# Profil Chef de service
class ChefServiceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=100)

# Profil Responsable hôpital
class ResponsableHopitalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hopital = models.CharField(max_length=150)


def __str__(self):
        return f"{self.username} ({self.role})"