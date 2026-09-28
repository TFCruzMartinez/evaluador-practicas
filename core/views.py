from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Registro
from .services import evaluar_postulacion


# --------------------------------------------------
# FUNCIONES DE PERMISOS
# --------------------------------------------------

def es_admin(user):
    return (
        user.is_superuser
        or user.groups.filter(name="admin").exists()
    )


def es_normal(user):
    return user.groups.filter(name="normal").exists()


def es_viewer(user):
    return user.groups.filter(name="viewer").exists()


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def vista_login(request):
    if request.user.is_authenticated:
        return redirect("lista")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("lista")

        messages.error(
            request,
            "Usuario o contraseña incorrectos."
        )

    return render(request, "login.html")


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@login_required(login_url="login")
def vista_logout(request):
    logout(request)
    return redirect("login")


# --------------------------------------------------
# READ
# admin + normal + viewer
# --------------------------------------------------

@login_required(login_url="login")
def lista(request):
    if not (
        es_admin(request.user)
        or es_normal(request.user)
        or es_viewer(request.user)
    ):
        raise PermissionDenied

    registros = Registro.objects.filter(eliminado=False)

    return render(
        request,
        "lista.html",
        {
            "registros": registros,
            "es_admin": es_admin(request.user),
            "es_normal": es_normal(request.user),
            "es_viewer": es_viewer(request.user),
        }
    )


# --------------------------------------------------
# CREATE
# admin + normal
# --------------------------------------------------

@login_required(login_url="login")
def crear(request):
    if not (
        es_admin(request.user)
        or es_normal(request.user)
    ):
        raise PermissionDenied

    error = None

    if request.method == "POST":
        try:
            semestre = int(
                request.POST.get("semestre", "")
            )
            horas_disponibles = int(
                request.POST.get(
                    "horas_disponibles",
                    ""
                )
            )

        except ValueError:
            error = (
                "Semestre y horas disponibles "
                "deben ser números enteros."
            )

        else:
            resultado = evaluar_postulacion(
                semestre,
                horas_disponibles
            )

            Registro.objects.create(
                semestre=semestre,
                horas_disponibles=horas_disponibles,
                resultado=resultado
            )

            return redirect("lista")

    return render(
        request,
        "form.html",
        {
            "accion": "Crear",
            "error": error
        }
    )


# --------------------------------------------------
# UPDATE
# solo admin
# --------------------------------------------------

@login_required(login_url="login")
def editar(request, pk):
    if not es_admin(request.user):
        raise PermissionDenied

    registro = get_object_or_404(
        Registro,
        pk=pk,
        eliminado=False
    )

    error = None

    if request.method == "POST":
        try:
            semestre = int(
                request.POST.get("semestre", "")
            )
            horas_disponibles = int(
                request.POST.get(
                    "horas_disponibles",
                    ""
                )
            )

        except ValueError:
            error = (
                "Semestre y horas disponibles "
                "deben ser números enteros."
            )

        else:
            registro.semestre = semestre
            registro.horas_disponibles = horas_disponibles

            # Reutiliza la lógica original
            registro.resultado = evaluar_postulacion(
                semestre,
                horas_disponibles
            )

            registro.save()

            return redirect("lista")

    return render(
        request,
        "form.html",
        {
            "accion": "Editar",
            "registro": registro,
            "error": error
        }
    )


# --------------------------------------------------
# DELETE LÓGICO
# solo admin
# --------------------------------------------------

@login_required(login_url="login")
def eliminar(request, pk):
    if not es_admin(request.user):
        raise PermissionDenied

    registro = get_object_or_404(
        Registro,
        pk=pk,
        eliminado=False
    )

    if request.method == "POST":
        registro.soft_delete()
        return redirect("lista")

    return render(
        request,
        "confirmar.html",
        {"registro": registro}
    )