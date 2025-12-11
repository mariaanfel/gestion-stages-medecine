from django.urls import path
from . import views

app_name = "Stage_condi"

urlpatterns = [
    path("offres/", views.liste_offre, name="liste_offre"),
    path("offres/nouvelle/", views.creer_offre, name="creer_offre"),
    path("offres/<int:id>/", views.detail_offre, name="detail_offre"),
    path("offres/<int:id>/modifier/", views.modifier_offre, name="modifier_offre"),
    path("offres/<int:id>/supprimer/", views.supprimer_offre, name="supprimer_offre"),
    path("offres/<int:id>/postuler/", views.postuler, name="postuler"),
    path("candidatures/", views.liste_candidatures_etudiant, name="liste_candidatures_etudiant"),
    path("candidatures/recues/", views.liste_candidatures_chef, name="liste_candidatures_chef"),
    path("candidatures/<int:id>/accepter/", views.accepter_candidature, name="accepter_candidature"),
    path("candidatures/<int:id>/refuser/", views.refuser_candidature, name="refuser_candidature"),
    path("candidature/<int:id>/", views.detail_candidature, name="detail_candidature"),
    path("candidatures/medecin/", views.liste_candidatures_medecin, name="liste_candidatures_medecin"),
    path("candidatures/<int:id>/evaluer/", views.evaluer_candidature, name="evaluer_candidature"),
    path("evaluations/miennes/", views.historique_etudiant, name="historique_etudiant"),


]
