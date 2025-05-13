
from .import views
from django.urls import path

urlpatterns = [
    path('add_event/', views.add_event, name="add_event"),
    path('update_events',views.update_events,name="update_events"),
    path('update_event_page',views.update_event_page,name="update_event_page"),
    path('events_home/', views.events_home, name="events_home"),
    path('rsvp_event/',views.rsvp_event,name='rsvp_event'),
    path('event_details',views.event_details,name='event_details'),
    path('image/<int:id>/', views.serve_image, name='serve_image'), #serve image url
    path('events/<int:event_id>/download-report/<str:format>/', views.download_event_report, name='download_event_report'), #generate pdf report url
    path('delete_event',views.delete_event, name='delete_event')
]
