
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm, LoginForm, StudentProfileForm, DoctorProfileForm, ChefServiceProfileForm, ResponsableHopitalProfileForm
from .models import User, StudentProfile, DoctorProfile, ChefServiceProfile, ResponsableHopitalProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login   # <— important
from django.db.models import Count, Q
from Stage_condi.models import OffreStage, Candidature  
from Comm_notif.services import notify_code



def get_dashboard_url_name(user):
    role = getattr(user, "role", None)

    if role == "student":
        return "accounts:student_dashboard"
    elif role == "doctor":
        return "accounts:doctor_dashboard"
    elif role == "chef":
        return "accounts:chef_dashboard"
    elif role == "responsable":
        return "accounts:responsable_dashboard"
    elif user.role == "admin":
        return "accounts:admin_dashboard"

    # ⚠️ S'il a un rôle inconnu, on NE LE RENVOIE PAS vers student_dashboard,
    # sinon ça crée une boucle. On le renvoie vers la page de login.
    return "accounts:login"


@login_required(login_url="accounts:login")
def home_redirect(request):
    return redirect(get_dashboard_url_name(request.user))

# Fonctions de vérification des rôles

def is_student(user):
    return user.is_authenticated and getattr(user, "role", None) == "student"

def is_doctor(user):
    return user.is_authenticated and getattr(user, "role", None) == "doctor"

def is_chef(user):
    return user.is_authenticated and getattr(user, "role", None) == "chef"

def is_responsable(user):
    return user.is_authenticated and getattr(user, "role", None) == "responsable"
def is_admin(user):
    return user.is_authenticated and getattr(user, "role", None) == "admin"

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect(get_dashboard_url_name(user))

        return render(request, "accounts/register.html", {"form": form})

class LoginView(View):
    def get(self, request):
        # ⚠️ Si l'utilisateur est déjà connecté, on l'envoie direct sur SON dashboard
        if request.user.is_authenticated:
            return redirect(get_dashboard_url_name(request.user))

        form = AuthenticationForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 🔔 Notifications après login, selon le rôle
            if user.role == "student":
                notify_code(
                    user,
                    code="STUDENT_LOGIN_SUCCESS",
                    context={},
                    category="auth",
                    level="success",
                )
            elif user.role in ["chef", "doctor", "responsable"]:
                notify_code(
                    user,
                    code="HOSPITAL_LOGIN_SUCCESS",
                    context={},
                    category="auth",
                    level="success",
                )
            elif user.role == "admin":
                notify_code(
                    user,
                    code="ADMIN_LOGIN_SUCCESS",
                    context={},
                    category="auth",
                    level="success",
                )

            # ⚠️ ON IGNORE COMPLETEMENT "next" POUR CASSER LA BOUCLE
            return redirect(get_dashboard_url_name(user))

        # Si le login échoue, on réaffiche la page
        return render(request, "accounts/login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounts:login")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        profile = None
        if user.role == "student":
            profile = get_object_or_404(StudentProfile, user=user)
        elif user.role == "doctor":
               dp = user.doctorprofile
               dp.service = request.POST.get("service", dp.speciality)
               dp.save()

        elif user.role == "chef":
            profile = get_object_or_404(ChefServiceProfile, user=user)
        elif user.role == "responsable":
            profile = get_object_or_404(ResponsableHopitalProfile, user=user)
        return render(request, "accounts/profile.html", {"user": user, "profile": profile})

@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
    def get(self, request):
        user = request.user
        form = None
        if user.role == "student":
            profile = get_object_or_404(StudentProfile, user=user)
            form = StudentProfileForm(instance=profile)
        elif user.role == "doctor":
            profile = get_object_or_404(DoctorProfile, user=user)
            form = DoctorProfileForm(instance=profile)
        elif user.role == "chef":
            profile = get_object_or_404(ChefServiceProfile, user=user)
            form = ChefServiceProfileForm(instance=profile)
        elif user.role == "responsable":
            profile = get_object_or_404(ResponsableHopitalProfile, user=user)
            form = ResponsableHopitalProfileForm(instance=profile)
        return render(request, "accounts/profile_edit.html", {"form": form})

    def post(self, request):
        user = request.user
        form = None
        if user.role == "student":
            profile = get_object_or_404(StudentProfile, user=user)
            form = StudentProfileForm(request.POST, instance=profile)
        elif user.role == "doctor":
            profile = get_object_or_404(DoctorProfile, user=user)
            form = DoctorProfileForm(request.POST, instance=profile)
        elif user.role == "chef":
            profile = get_object_or_404(ChefServiceProfile, user=user)
            form = ChefServiceProfileForm(request.POST, instance=profile)
        elif user.role == "responsable":
            profile = get_object_or_404(ResponsableHopitalProfile, user=user)
            form = ResponsableHopitalProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
        return render(request, "accounts/profile_edit.html", {"form": form})

# ============================================================================
# DASHBOARDS AVEC CONTEXTE DYNAMIQUE
# ============================================================================
@method_decorator([login_required, user_passes_test(is_student, login_url=None)], name='dispatch')
class StudentDashboard(View):
    def get(self, request):
        # Récupérer le profil étudiant
        try:
            profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            profile = None
        
        # Statistiques pour l'étudiant
        stats = {
            'stages_en_cours': 3,
            'documents_en_attente': 2,
            'evaluations_pending': 1,
            'moyenne_generale': 15.5,
        }
        
        context = {
            'profile': profile,
            'user': request.user,
            'stats': stats,
            'page_title': 'Dashboard Étudiant',
        }
        return render(request, "accounts/dashboard_student.html", context)

@method_decorator([login_required, user_passes_test(is_doctor)], name='dispatch')
class DoctorDashboard(View):
    def get(self, request):
        # Récupérer le profil médecin
        try:
            profile = DoctorProfile.objects.get(user=request.user)
        except DoctorProfile.DoesNotExist:
            profile = None
        
        # Statistiques pour le médecin
        stats = {
            'etudiants_assignes': 5,
            'evaluations_en_attente': 3,
            'rapports_a_valider': 2,
            'reunions_cette_semaine': 1,
        }
        
        context = {
            'profile': profile,
            'user': request.user,
            'stats': stats,
            'page_title': 'Dashboard Médecin',
        }
        return render(request, "accounts/dashboard_doctor.html", context)
@method_decorator([login_required, user_passes_test(is_chef)], name='dispatch')
class ChefDashboard(View):
    def get(self, request):
        # Profil chef de service
        try:
            profile = ChefServiceProfile.objects.get(user=request.user)
            service_name = profile.service
        except ChefServiceProfile.DoesNotExist:
            profile = None
            service_name = None

        # 1) Récupérer tous les médecins de ce service
        doctor_users_ids = DoctorProfile.objects.filter(
            service=service_name
        ).values_list("user_id", flat=True)

        # 2) Offres supervisées par :
        #    - un médecin de ce service
        #    - OU le chef lui-même
        offres_qs = OffreStage.objects.filter(
            Q(superviseur_id__in=doctor_users_ids) |
            Q(superviseur=request.user)
        )

        # Séparer actives / archivées
        offres_actives = offres_qs.filter(archive=False)
        offres_archivees = offres_qs.filter(archive=True)

        # Candidatures sur ces offres
        candidatures_qs = Candidature.objects.filter(offre__in=offres_qs)

        total_candidatures = candidatures_qs.count()
        en_attente = candidatures_qs.filter(statut="en_attente").count()
        acceptees = candidatures_qs.filter(statut="acceptee").count()
        refusees = candidatures_qs.filter(statut="refusee").count()
        archivees = candidatures_qs.filter(statut="archivee").count()

        # Taux d'occupation = acceptées / (acceptées + en attente)
        denom = acceptees + en_attente
        taux_occupation = round(acceptees / denom * 100) if denom > 0 else 0

        stats = {
            "offres_actives": offres_actives.count(),
            "offres_archivees": offres_archivees.count(),
            "candidatures_recues": total_candidatures,
            "candidatures_en_attente": en_attente,
            "candidatures_acceptees": acceptees,
            "candidatures_refusees": refusees,
            "candidatures_archivees": archivees,
            "taux_occupation": taux_occupation,
            "reunions_cette_semaine": 0,
            "alertes_en_cours": en_attente,
        }

        context = {
            "profile": profile,
            "user": request.user,
            "stats": stats,
            "page_title": "Dashboard Chef de Service",
        }
        return render(request, "accounts/dashboard_chef.html", context)

@method_decorator([login_required, user_passes_test(is_responsable)], name='dispatch')
class ResponsableDashboard(View):
    def get(self, request):
        # Profil responsable
        try:
            profile = ResponsableHopitalProfile.objects.get(user=request.user)
        except ResponsableHopitalProfile.DoesNotExist:
            profile = None

        # Offres et candidatures sur tout l'hôpital (toutes spécialités)
        offres_actives = OffreStage.objects.filter(archive=False)
        offres_archivees = OffreStage.objects.filter(archive=True)

        candidatures_qs = Candidature.objects.filter(offre__archive=False)
        stages_actifs = candidatures_qs.filter(statut="acceptee").count()
        candidatures_en_attente = candidatures_qs.filter(statut="en_attente").count()

        services_geres = (
            offres_actives.values("specialite").distinct().count()
        )

        # Approximatif : nb de médecins + chefs
        personnel_total = User.objects.filter(
            role__in=["doctor", "chef"]
        ).count()

        stats = {
            "stages_actifs": stages_actifs,
            "services_geres": services_geres,
            "offres_disponibles": offres_actives.count(),
            "offres_archivees": offres_archivees.count(),
            "personnel_total": personnel_total,
            "alertes_en_cours": candidatures_en_attente,  # ex : candidatures encore en attente
        }

        context = {
            "profile": profile,
            "user": request.user,
            "stats": stats,
            "page_title": "Dashboard Responsable Hospitalier",
        }
        return render(request, "accounts/dashboard_responsable.html", context)

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/profile.html")

    def post(self, request):
        user = request.user

        # Champs généraux
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()

        # Gestion des rôles
        if user.role == "student":
            sp = user.studentprofile
            sp.matricule = request.POST.get("matricule")
            sp.cycle = request.POST.get("cycle")
            sp.save()

        elif user.role == "doctor":
            dp = user.doctorprofile
            dp.speciality = request.POST.get("speciality")
            dp.save()

        elif user.role == "chef":
            cp = user.chefserviceprofile
            cp.service = request.POST.get("service")
            cp.hopital = request.POST.get("hopital")
            cp.save()

        elif user.role == "responsable":
            rp = user.responsablehopitalprofile
            rp.hopital = request.POST.get("hopital")
            rp.save()

        messages.success(request, "Profil mis à jour avec succès !")
        return redirect("accounts:profile")
@method_decorator([login_required, user_passes_test(is_chef)], name="dispatch")
class ChefStatistiquesView(View):
    def get(self, request):
        # Service du chef
        profile = ChefServiceProfile.objects.get(user=request.user)
        service_name = profile.service

        # Médecins du service
        doctor_users_ids = DoctorProfile.objects.filter(
            service=service_name
        ).values_list("user_id", flat=True)

        # Offres du service (médecins + chef)
        offres = OffreStage.objects.filter(
            Q(superviseur_id__in=doctor_users_ids) |
            Q(superviseur=request.user)
        )

        # Candidatures sur ces offres
        candidatures = Candidature.objects.filter(offre__in=offres)

        stats = {
            "offres_actives": offres.filter(archive=False).count(),
            "offres_archivees": offres.filter(archive=True).count(),
            "candidatures_totales": candidatures.count(),
            "en_attente": candidatures.filter(statut="en_attente").count(),
            "acceptees": candidatures.filter(statut="acceptee").count(),
            "refusees": candidatures.filter(statut="refusee").count(),
            "archivees": candidatures.filter(statut="archivee").count(),
        }

        stats_par_offre = (
            candidatures.values("offre__titre")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        context = {
            "stats": stats,
            "stats_par_offre": stats_par_offre,
            "service": service_name,
        }
        return render(request, "accounts/statistiques_chef.html", context)

@method_decorator([login_required, user_passes_test(is_responsable)], name="dispatch")
class ResponsableStatistiquesView(View):
    def get(self, request):

        offres = OffreStage.objects.filter(archive=False)
        candidatures = Candidature.objects.all()

        stats = {
            "offres_total": offres.count(),
            "candidatures_totales": candidatures.count(),
            "acceptees": candidatures.filter(statut="acceptee").count(),
            "en_attente": candidatures.filter(statut="en_attente").count(),
            "refusees": candidatures.filter(statut="refusee").count(),
        }

        # REGROUPER PAR SERVICE
        stats_par_service = (
            candidatures.values("offre__specialite")
            .annotate(total=Count("id"))
            .order_by("offre__specialite")
        )

        context = {
            "stats": stats,
            "stats_par_service": stats_par_service,
        }

        return render(request, "accounts/statistiques_responsable.html", context)

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class AdminDashboard(View):
    def get(self, request):
        # Comptes
        total_users = User.objects.count()
        total_students = User.objects.filter(role="student").count()
        total_doctors = User.objects.filter(role="doctor").count()
        total_chefs = User.objects.filter(role="chef").count()
        total_responsables = User.objects.filter(role="responsable").count()
        total_admins = User.objects.filter(role="admin").count()

        # Stages & candidatures
        offres_total = OffreStage.objects.count()
        offres_actives = OffreStage.objects.filter(archive=False).count()
        offres_archivees = OffreStage.objects.filter(archive=True).count()

        candidatures_total = Candidature.objects.count()
        candidatures_en_attente = Candidature.objects.filter(statut="en_attente").count()
        candidatures_acceptees = Candidature.objects.filter(statut="acceptee").count()
        candidatures_refusees = Candidature.objects.filter(statut="refusee").count()

        stats = {
            "total_users": total_users,
            "total_students": total_students,
            "total_doctors": total_doctors,
            "total_chefs": total_chefs,
            "total_responsables": total_responsables,
            "total_admins": total_admins,
            "offres_total": offres_total,
            "offres_actives": offres_actives,
            "offres_archivees": offres_archivees,
            "candidatures_total": candidatures_total,
            "candidatures_en_attente": candidatures_en_attente,
            "candidatures_acceptees": candidatures_acceptees,
            "candidatures_refusees": candidatures_refusees,
        }

        # Exemple de top 5 utilisateurs les plus récents
        derniers_utilisateurs = User.objects.order_by("-date_joined")[:5]

        context = {
            "stats": stats,
            "derniers_utilisateurs": derniers_utilisateurs,
            "page_title": "Dashboard Administrateur",
        }
        return render(request, "accounts/dashboard_admin.html", context)
    

    


