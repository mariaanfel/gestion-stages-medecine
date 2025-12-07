from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()

class OffreStage(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    specialite = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    superviseur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    archive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
    
class Candidature(models.Model):

    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("acceptee", "Acceptée"),
        ("refusee", "Refusée"),
        ("archivee", "Archivée"),
    ]

    etudiant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidatures"
    )

    offre = models.ForeignKey(
        OffreStage,
        on_delete=models.CASCADE,
        related_name="candidatures"
    )

    cv = models.FileField(upload_to="cvs/")
    lettre_motivation = models.TextField(blank=True, null=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="en_attente"
    )

    date_postulation = models.DateTimeField(auto_now_add=True)
    date_decision = models.DateTimeField(null=True, blank=True)

    commentaire_medecin = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Candidature de {self.etudiant.username} pour {self.offre.titre}"