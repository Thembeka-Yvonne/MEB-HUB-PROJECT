from tkinter.font import names

from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.admin_home,name="admin_home"),

    path('events_menu',views.events_menu, name="events_menu"),
    
    #url patterns for the bus
    
    path('bus_menu',views.bus_menu, name="bus_menu"),
    path('add_all_campus_view',views.add_all_campuses_view,name="add_all_campus_view"),
    path('add_bus_schedule/<int:code>/',views.add_bus_schedule,name="add_bus_schedule"),
    path('bus_stats', views.bus_schedule_stats, name='bus_schedule_stats'),
    #path('bus_dashboard',views.bus_dashboard,name="bus_dashboard"),
    
    #url pattern for the admin home
    path("view_all_actions",views.view_all_actions,name="view_all_actions"),

    #url patterns for the bus
    path("add_bus",views.add_bus,name="add_bus"),
    path("remove_bus",views.remove_bus,name="remove_bus"),

     #dashboard pages
    path("user_management",views.user_management,name="user_management"),
    path("analytics",views.analytics,name="analytics")
]
