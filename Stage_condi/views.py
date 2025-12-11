from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import OffreStage, Candidature, Evaluation
from .forms import OffreStageForm, CandidatureForm, EvaluationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse         # pour générer les liens
from Comm_notif.services import notify_code

def is_chef(user):
    return user.is_authenticated and user.role == "chef"

def is_student(user):
    return user.is_authenticated and user.role == "student"

def is_doctor(user):
    return user.is_authenticated and user.role == "doctor"

@user_passes_test(is_chef)
def creer_offre(request):
    if request.method == "POST":
        form = OffreStageForm(request.POST, user=request.user)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.superviseur = request.user   # le chef qui crée l'offre
            offre.save()
            messages.success(request, "Offre de stage créée avec succès.")
            return redirect("Stage_condi:liste_offre")
    else:
        form = OffreStageForm(user=request.user)

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
        form = OffreStageForm(request.POST, instance=offre, user=request.user)
        if form.is_valid():
            form.save()  # superviseur ne change pas ici
            return redirect("Stage_condi:liste_offre")
    else:
        
        form = OffreStageForm(instance=offre, user=request.user)

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

            # 🔔 NOTIFICATIONS ICI
            etudiant = candidature.etudiant
            chef = offre.superviseur  # le chef qui a créé l'offre

            # Notif pour l'étudiant
            notify_code(
                etudiant,
                code="STUDENT_CANDIDATURE_SUBMITTED",
                context={"stage": offre.titre},
                url=reverse("Stage_condi:detail_offre", args=[offre.id]),
                category="candidature",
                level="info",
            )

            # Notif pour le chef / hôpital
            if chef:
                notify_code(
                    chef,
                    code="HOSPITAL_NEW_CANDIDATURE",
                    context={"stage": offre.titre, "etudiant": etudiant.username},
                    url=reverse("Stage_condi:liste_candidatures_chef"),
                    category="candidature",
                    level="info",
                )

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

    # 🔔 Notification pour l'étudiant
    notify_code(
        candidature.etudiant,
        code="STUDENT_CANDIDATURE_ACCEPTED",
        context={"stage": candidature.offre.titre},
        category="candidature",
        level="success",
    )

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

    # 🔔 Notification pour l'étudiant
    notify_code(
        candidature.etudiant,
        code="STUDENT_CANDIDATURE_REFUSED",
        context={"stage": candidature.offre.titre},
        category="candidature",
        level="warning",
    )

    messages.info(request, "La candidature a été refusée.")
    return redirect("Stage_condi:liste_candidatures_chef")


@user_passes_test(is_doctor)
def liste_candidatures_medecin(request):
    candidatures = Candidature.objects.filter(
        offre__medecin_responsable=request.user
    ).order_by("-date_postulation")

    return render(
        request,
        "Stage_condi/liste_candidatures.html",
        {"candidatures": candidatures}
    )

@user_passes_test(is_doctor)
def evaluer_candidature(request, id):
    candidature = get_object_or_404(Candidature, id=id)

    # sécurité : le médecin ne peut évaluer que les candidatures de SES stages
    if candidature.offre.medecin_responsable != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à évaluer cette candidature.")

    evaluation = getattr(candidature, "evaluation", None)  # existe déjà ou non

    if request.method == "POST":
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.candidature = candidature
            evaluation.medecin = request.user
            evaluation.save()
            messages.success(request, "Évaluation enregistrée.")
            return redirect("Stage_condi:liste_candidatures_medecin")
    else:
        form = EvaluationForm(instance=evaluation)

    return render(request, "Stage_condi/evaluer_candidature.html", {
        "form": form,
        "candidature": candidature,
    })

@login_required
def historique_etudiant(request):
    evaluations = Evaluation.objects.filter(
        candidature__etudiant=request.user
    ).order_by("-created_at")

    return render(request, "Stage_condi/historique_etudiant.html", {
        "evaluations": evaluations
    })


