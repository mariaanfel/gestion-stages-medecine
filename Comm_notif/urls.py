from django.urls import path
from .views import NotificationListView

app_name = "Comm_notif"

urlpatterns = [
    path("mes-notifications/", NotificationListView.as_view(), name="liste"),
    path("mes-notifications/", NotificationListView.as_view(), name="liste"),
]
