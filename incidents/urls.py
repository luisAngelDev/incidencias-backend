from django.urls import path, include
from rest_framework import routers
from incidents import views

router = routers.DefaultRouter()
router.register(r'incidents', views.IncidentView, 'incidents')

urlpatterns = [
    path("api/", include(router.urls))
]