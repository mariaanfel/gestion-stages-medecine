from django.shortcuts import render, redirect, get_object_or_404
from .models import OffreStage
from .forms import OffreStageForm
from django.contrib.auth.decorators import user_passes_test

def is_chef(user):
    return user.is_authenticated and user.role == "chef"

@user_passes_test(is_chef)
def creer_offre(request):
    if request.method == "POST":
        form = OffreStageForm(request.POST)
        if form.is_valid():
            form.save()
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
