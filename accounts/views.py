# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm, LoginForm, StudentProfileForm, DoctorProfileForm, ChefServiceProfileForm, ResponsableHopitalProfileForm
from .models import User, StudentProfile, DoctorProfile, ChefServiceProfile, ResponsableHopitalProfile

# Fonctions de vérification des rôles
def is_student(user): return user.role == "student"
def is_doctor(user): return user.role == "doctor"
def is_chef(user): return user.role == "chef"
def is_responsable(user): return user.role == "responsable"
def is_admin(user): return user.role == "admin"

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Création automatique du profil selon le rôle
            role = form.cleaned_data['role']

            if role == "student":
                StudentProfile.objects.create(user=user)
            elif role == "doctor":
                DoctorProfile.objects.create(user=user)
            elif role == "chef":
                ChefServiceProfile.objects.create(user=user)
            elif role == "responsable":
                ResponsableHopitalProfile.objects.create(user=user)

            return redirect("accounts:login")

        return render(request, "accounts/register.html", {"form": form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                if user.role == "student":
                    return redirect("accounts:student_dashboard")
                elif user.role == "doctor":
                    return redirect("accounts:doctor_dashboard")
                elif user.role == "chef":
                    return redirect("accounts:chef_dashboard")
                elif user.role == "responsable":
                    return redirect("accounts:responsable_dashboard")
                elif user.role == "admin":
                    return redirect("/admin/")
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
            profile = get_object_or_404(DoctorProfile, user=user)
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

@method_decorator([login_required, user_passes_test(is_student)], name='dispatch')
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
        # Récupérer le profil chef de service
        try:
            profile = ChefServiceProfile.objects.get(user=request.user)
        except ChefServiceProfile.DoesNotExist:
            profile = None
        
        # Statistiques pour le chef de service
        stats = {
            'etudiants_service': 8,
            'stages_proposes': 5,
            'lits_disponibles': 12,
            'taches_en_cours': 7,
        }
        
        context = {
            'profile': profile,
            'user': request.user,
            'stats': stats,
            'page_title': 'Dashboard Chef de Service',
        }
        return render(request, "accounts/dashboard_chef.html", context)

@method_decorator([login_required, user_passes_test(is_responsable)], name='dispatch')
class ResponsableDashboard(View):
    def get(self, request):
        # Récupérer le profil responsable
        try:
            profile = ResponsableHopitalProfile.objects.get(user=request.user)
        except ResponsableHopitalProfile.DoesNotExist:
            profile = None
        
        # Statistiques pour le responsable
        stats = {
            'stages_actifs': 15,
            'services_geres': 8,
            'personnel_total': 45,
            'alertes_en_cours': 3,
        }
        
        context = {
            'profile': profile,
            'user': request.user,
            'stats': stats,
            'page_title': 'Dashboard Responsable Hospitalier',
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
