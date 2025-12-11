# accounts/urls.py
from django.urls import path
from . import views 
from django.views.generic import RedirectView
from .views import (
    RegisterView, LoginView, LogoutView,
    ProfileView, ProfileEditView,
    StudentDashboard, DoctorDashboard, ChefDashboard, ResponsableDashboard,AdminUserListView,
    AdminUserUpdateView,
    AdminUserCreateView,
    AdminUserDeleteView,
    
)

app_name = 'accounts'

urlpatterns = [
    # Page d'accueil redirige vers login
    path('', RedirectView.as_view(pattern_name='accounts:login'), name='home'),
    
    # Authentification
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    # Profil (accessible seulement après login)

    path("profile/", ProfileView.as_view(), name="profile"),


    # Dashboards (protégés par authentification)
    path("dashboard/student/", StudentDashboard.as_view(), name="student_dashboard"),
    path("dashboard/doctor/", DoctorDashboard.as_view(), name="doctor_dashboard"),
    path("dashboard/chef/", ChefDashboard.as_view(), name="chef_dashboard"),
    path("dashboard/responsable/", ResponsableDashboard.as_view(), name="responsable_dashboard"),


    
 #Statistiques
    path("dashboard/chef/statistiques/", views.ChefStatistiquesView.as_view(), name="ChefStatistiquesView"),
    path("dashboard/responsable/statistiques/",views.ResponsableStatistiquesView.as_view(),name="ResponsableStatistiquesView"),
    path("dashboard/admin/", views.AdminDashboard.as_view(), name="admin_dashboard"),

    path("admin/utilisateurs/", AdminUserListView.as_view(), name="admin_users"),
    path("admin/utilisateurs/nouveau/", AdminUserCreateView.as_view(), name="admin_user_create"),
    path("admin/utilisateurs/<int:pk>/", AdminUserUpdateView.as_view(), name="admin_user_edit"),
    path("admin/utilisateurs/<int:pk>/supprimer/", AdminUserDeleteView.as_view(), name="admin_user_delete"),

]