from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import OffreStage, Candidature
from .forms import OffreStageForm, CandidatureForm
from django.contrib.auth.decorators import login_required, user_passes_test

def is_chef(user):
    return user.is_authenticated and user.role == "chef"

def is_student(user):
    return user.is_authenticated and user.role == "student"

@user_passes_test(is_chef)
def creer_offre(request):
    if request.method == "POST":
        form = OffreStageForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.superviseur = request.user   
            offre.save()
            return redirect('Stage_condi:liste_offre')
    else:
        form = OffreStageForm()
    return render(request, "Stage_condi/creer_offre.html", {"form": form})


def liste_offre(request):
    offres = OffreStage.objects.filter(archive=False)
    return render(request, "Stage_condi/liste_offre.html", {"offres": offres})

def detail_offre(request, id):
    offre = get_object_or_404(OffreStage, id=id)
    return render(request, "Stage_condi/detail_offre.html", {"offre": offre})

@user_passes_test(is_chef)
def modifier_offre(request, id):
    offre = get_object_or_404(OffreStage, id=id)

    if request.method == "POST":
        form = OffreStageForm(request.POST, request.FILES, instance=offre)
        if form.is_valid():
            form.save()
            return redirect("Stage_condi:liste_offre")
    else:
        form = OffreStageForm(instance=offre)

    return render(request, "Stage_condi/edit.html", {"form": form, "offre": offre})


@user_passes_test(is_chef)
def supprimer_offre(request, id):
    offre = get_object_or_404(OffreStage, id=id)

    if request.method == "POST":
        offre.delete()
        return redirect("Stage_condi:liste_offre")

    return render(request, "Stage_condi/delete_confirm.html", {"offre": offre})

@user_passes_test(is_student)
def postuler(request, id):
    offre = get_object_or_404(OffreStage, id=id)

    # Empêcher un étudiant de postuler 2 fois à la même offre
    if Candidature.objects.filter(etudiant=request.user, offre=offre).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
        return redirect("Stage_condi:detail_offre", id=offre.id)

    if request.method == "POST":
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.etudiant = request.user
            candidature.offre = offre
            candidature.save()

            messages.success(request, "Votre candidature a été envoyée avec succès.")
            return redirect("Stage_condi:detail_offre", id=offre.id)
    else:
        form = CandidatureForm()

    return render(request, "Stage_condi/postuler.html", {
        "offre": offre,
        "form": form
    })


@login_required
def liste_candidatures_etudiant(request):
    candidatures = Candidature.objects.filter(
        etudiant=request.user
    ).order_by('-date_postulation')
    return render(request, 'Stage_condi/liste_candidatures.html', {'candidatures': candidatures})


@user_passes_test(is_chef)
def liste_candidatures_chef(request):
    candidatures = Candidature.objects.filter(
        offre__superviseur=request.user
    ).order_by('-date_postulation')
    return render(request, 'Stage_condi/liste_candidatures.html', {'candidatures': candidatures})


@user_passes_test(is_chef)
def accepter_candidature(request, id):
    candidature = get_object_or_404(Candidature, id=id)

    # Sécurité : le chef ne peut agir que sur SES offres
    if candidature.offre.superviseur != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cette candidature.")

    candidature.statut = "acceptee"
    candidature.date_decision = timezone.now()
    candidature.commentaire_medecin = request.POST.get(
        "commentaire_medecin",
        candidature.commentaire_medecin
    )
    candidature.save()

    messages.success(request, "La candidature a été acceptée.")
    return redirect("Stage_condi:liste_candidatures_chef")


@user_passes_test(is_chef)
def refuser_candidature(request, id):
    candidature = get_object_or_404(Candidature, id=id)

    if candidature.offre.superviseur != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cette candidature.")

    candidature.statut = "refusee"
    candidature.date_decision = timezone.now()
    candidature.commentaire_medecin = request.POST.get(
        "commentaire_medecin",
        candidature.commentaire_medecin
    )
    candidature.save()

    messages.info(request, "La candidature a été refusée.")
    return redirect("Stage_condi:liste_candidatures_chef")