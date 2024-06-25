from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters
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
