from django.urls import path
from . import views

app_name = "Stage_condi"

urlpatterns = [
    path("offres/", views.liste_offre, name="liste_offre"),
    path("offres/nouvelle/", views.creer_offre, name="creer_offre"),
    path("offres/<int:id>/", views.detail_offre, name="detail_offre"),
    path("<int:id>/modifier/", views.modifier_offre, name="modifier_offre"),
    path("<int:id>/supprimer/", views.supprimer_offre, name="supprimer_offre"),
]
