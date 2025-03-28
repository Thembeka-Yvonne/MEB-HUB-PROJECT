
from .import views
from django.urls import path

urlpatterns = [
    path('add_event',views.add_event,name="add_event"),
    path('update_events',views.update_events,name="update_events"),
    path('update_event_page',views.update_event_page,name="update_event_page"),
    path('delete_event',views.delete_event,name="delete_event")
]
