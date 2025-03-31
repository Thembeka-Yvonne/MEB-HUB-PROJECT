from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_home,name="admin_home"),
    path('campus-menu',views.campus_menu,name="campus_menu"),
    path('add_campus',views.add_campus,name="add_campus"),
    path('list_all_campus',views.list_all_campus,name="list_all_campus"),
    path('remove_campus/<int:id>',views.remove_campus,name="remove_campu"),
    path('modify_list_campus',views.modify_list_campus,name="modify_list_campus"),
    path('modify_campus/<int:id>',views.modify_campus,name="modify_campus"),
    path('view_all_campuses',views.view_all_campuses,name="view_all_campuses"),
    path('events_menu',views.events_menu, name="events_menu")
]
