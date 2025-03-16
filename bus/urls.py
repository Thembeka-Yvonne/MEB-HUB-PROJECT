from . import views
from django.urls import path

urlpatterns = [
    path("home",views.home,name="home"),
    path("view_schedule/<int:schedule_code>",views.view_schedule,name="view_schedule")
]