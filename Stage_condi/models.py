from django.db import models
from django.contrib.auth import get_user_model

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
