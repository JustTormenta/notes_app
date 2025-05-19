from django.urls import path
from .views import hello_view, index, note_view
from . import views

urlpatterns = [
    path('', hello_view),
    path('', views.index, name='home'),
    path('hw39/', index),
    path('hw40/', note_view),
    path('note/create/', views.create_note, name='create_note'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('note/<int:pk>/edit/', views.edit_note, name='edit_note'),
    path('note/<int:pk>/delete/', views.delete_note, name='delete_note'),
]