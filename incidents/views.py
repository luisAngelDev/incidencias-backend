from django.shortcuts import render
from rest_framework import viewsets
from .serializer import IncidentSerializer
from .models import Incident

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class IncidentView(viewsets.ModelViewSet):
    serializer_class = IncidentSerializer
    queryset = Incident.objects.all()

     # Configurar autenticación y permisos solo para este viewset
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]