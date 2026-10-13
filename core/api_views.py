
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Registro
from .serializers import RegistroSerializer
from .views import es_admin, es_normal, es_viewer


class RegistroPermission(BasePermission):
    """
    Permisos diferenciados por rol.

    viewer: consultar
    normal: consultar y crear
    admin: consultar, crear, editar y eliminar
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if es_admin(user):
            return True

        if request.method in ("GET", "HEAD", "OPTIONS"):
            return es_normal(user) or es_viewer(user)

        if request.method == "POST":
            return es_normal(user)

        return False


class RegistroViewSet(viewsets.ModelViewSet):
    """
    API REST para gestionar registros de prácticas.
    """

    serializer_class = RegistroSerializer
    permission_classes = [RegistroPermission]

    def get_queryset(self):
        return Registro.objects.filter(eliminado=False)

    def perform_destroy(self, instance):
        instance.soft_delete()
