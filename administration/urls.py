from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_home,name="admin_home"),
    path('campus-menu',views.campus_menu,name="campus_menu"),
    path('add_campus',views.add_campus,name="add_campus"),
    path('events_menu',views.events_menu, name="events_menu"),
]
