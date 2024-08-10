from django.urls import path, include
from  . import views

app_name = "events"

urlpatterns = [
    path('', views.event_list, name="event_list"),
    path('event/<int:pk>', views.event_detail, name="event_detail"),
    path('event/new/', views.event_create, name="event_create"),
    path('event/<int:pk>/edit/', views.event_update, name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('logout/', views.user_logout, name='logout'),
]