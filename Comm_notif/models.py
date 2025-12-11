from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class NotificationTemplate(models.Model):
    """
    Modèle pour les types de notifications :
    ex: STUDENT_CANDIDATURE_ACCEPTED, HOSPITAL_NEW_CANDIDATURE, etc.
    """

    ROLE_CHOICES = [
        ("student", "Étudiant"),
        ("doctor", "Médecin"),
        ("chef", "Chef de service"),
        ("responsable", "Responsable d’hôpital"),
        ("admin", "Administrateur"),
        ("all", "Tous"),
    ]

    code = models.CharField(
        max_length=100,
        unique=True,
        help_text="Code interne, ex: STUDENT_CANDIDATURE_ACCEPTED",
    )
    title_template = models.CharField(
        max_length=200,
        help_text="Titre avec variables, ex: 'Candidature pour {stage}'",
    )
    body_template = models.TextField(
        help_text="Message avec variables, ex: 'Votre candidature pour {stage} a été acceptée.'",
    )
    target_role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="all",
    )

    def __str__(self):
        return f"{self.code} ({self.target_role})"


class Notification(models.Model):
    """
    Notification envoyée à un utilisateur.
    """

    LEVEL_CHOICES = [
        ("info", "Information"),
        ("success", "Succès"),
        ("warning", "Avertissement"),
        ("error", "Erreur"),
    ]

    CATEGORY_CHOICES = [
        ("auth", "Authentification"),
        ("offre", "Offre de stage"),
        ("candidature", "Candidature"),
        ("stage", "Stage"),
        ("evaluation", "Évaluation"),
        ("message", "Message"),
        ("system", "Système"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)
    message = models.TextField()

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="info")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="system")

    url = models.CharField(
        max_length=300,
        blank=True,
        help_text="Lien vers la page concernée (optionnel)",
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient} - {self.title[:30]}"
