
from .import views
from django.urls import path

urlpatterns = [
    path('add_event/', views.add_event, name="add_event"),
    path('success', views.success, name="success"),
    path('update_events',views.update_events,name="update_events"),
    path('update_event_page',views.update_event_page,name="update_event_page"),
    path('delete_events',views.delete_events,name="delete_events"),
    path('delete_event_page/',views.delete_event_page,name="delete_event_page"),
    path('events_home/', views.events_home, name="events_home")

]
