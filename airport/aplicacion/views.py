from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Proof");

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Vuelo, Terminal

def vista_usuario(request):
    terminales = Terminal.objects.all()
    vuelos = None

    if request.GET.get("terminal") and request.GET.get("fecha"):
        vuelos = Vuelo.objects.filter(
            terminal_id=request.GET["terminal"],
            fecha_salida=request.GET["fecha"]
        )

    return render(request, "aplicacion/usuario_dashboard.html", {"terminales": terminales, "vuelos": vuelos})

from django.contrib.auth.decorators import login_required, user_passes_test

def es_moderador(user):
    return user.groups.filter(name="Moderador").exists()

@login_required
@user_passes_test(es_moderador)
def vista_moderador(request):
    vuelos = Vuelo.objects.all()
    return render(request, "moderador_dashboard.html", {"vuelos": vuelos})

def es_administrador(user):
    return user.groups.filter(name="Administrador").exists()

@login_required
@user_passes_test(es_administrador)
def vista_admin(request):
    return render(request, "admin_dashboard.html")
