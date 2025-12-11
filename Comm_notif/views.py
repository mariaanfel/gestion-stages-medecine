from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Notification


@method_decorator(login_required, name="dispatch")
class NotificationListView(ListView):
    model = Notification
    template_name = "Comm_notif/notifications.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
@method_decorator(login_required, name="dispatch")
class NotificationListView(ListView):
    model = Notification
    template_name = "Comm_notif/notifications.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        # On affiche uniquement les notifications de l'utilisateur connecté
        return Notification.objects.filter(recipient=self.request.user)
