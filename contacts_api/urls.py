from django.urls import path
from .views import ContactListCreateView, ContactDetailView, export_contacts, ImportContactsView
urlpatterns = [
    path('contact/', ContactListCreateView.as_view()),
    path('contact/<int:pk>/', ContactDetailView.as_view()),
    path('export/', export_contacts),
    path('import/', ImportContactsView.as_view()),
]