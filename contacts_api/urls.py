from django.urls import path
from .views import ContactListCreateView, ContactDetailView
urlpatterns = [
    path('contact/', ContactListCreateView.as_view()),
    path('contact/<int:pk>/', ContactDetailView.as_view()),
]