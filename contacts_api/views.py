import csv
from django.http import HttpResponse
import io
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters

from categories_api.models import Category
from .models import Contact
from .serializers import ContactSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import ContactPagination

class ContactFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    email = filters.CharFilter(field_name="email", lookup_expr='icontains')
    category = filters.CharFilter(field_name="category__name", lookup_expr='icontains')

    class Meta:
        model = Contact
        fields = ['name', 'email', 'category']

class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = ContactPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ContactFilter
    search_fields = ['name', 'email']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        if Contact.objects.filter(email=serializer.validated_data['email']).exists():
            return Response({'error': 'A contact with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        if 'email' in serializer.validated_data:
            if Contact.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'error': 'A contact with this email already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Contact deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

def export_contacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Category', 'Created At'])

    contacts = Contact.objects.all()
    for contact in contacts:
        writer.writerow([
            contact.id,
            contact.name,
            contact.email,
            contact.phone,
            contact.category.label,  # Accessing category name
            contact.created_at
        ])

    return response


class ImportContactsView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.csv'):
            return Response({'error': 'Invalid file type. Only CSV files are allowed.'},
                            status=status.HTTP_400_BAD_REQUEST)

        file_data = file.read().decode('utf-8')
        io_string = io.StringIO(file_data)
        reader = csv.reader(io_string)

        headers = next(reader, None)
        expected_headers = ['name', 'email', 'phone', 'category']
        if headers != expected_headers:
            return Response({'error': f'Invalid CSV format. Expected headers: {expected_headers}'},
                            status=status.HTTP_400_BAD_REQUEST)

        errors = []
        contacts = []
        for row in reader:
            name, email, phone, category_name = row
            if Contact.objects.filter(email=email).exists():
                errors.append(f'Email {email} already exists.')
                continue

            try:
                category = Category.objects.get(label=category_name)
            except Category.DoesNotExist:
                errors.append(f'Category {category_name} does not exist.')
                continue

            contact = Contact(name=name, email=email, phone=phone, category=category)
            contacts.append(contact)

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        Contact.objects.bulk_create(contacts)
        return Response({'message': 'Contacts imported successfully'}, status=status.HTTP_201_CREATED)
