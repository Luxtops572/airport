from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Proof");

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Vuelo, Terminal

from datetime import datetime

def vista_usuario(request):
    terminales = Terminal.objects.all()
    vuelos = None  

    terminal_id = request.GET.get("terminal")
    fecha_str = request.GET.get("fecha")  # La fecha viene como string

    if terminal_id and fecha_str:
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()  # Convertir string a date
            vuelos = Vuelo.objects.filter(
                terminal_id=terminal_id,
                fecha_salida__date=fecha_obj  # Ignorar la hora en la comparación
            )
        except ValueError:
            vuelos = []  # Si la fecha es inválida, retorna lista vacía

    return render(request, "aplicacion/usuario_dashboard.html", {"terminales": terminales, "vuelos": vuelos})

from django.contrib.auth.decorators import login_required, user_passes_test

def es_moderador(user):
    return user.groups.filter(name="Moderador").exists()
"""
@login_required
@user_passes_test(es_moderador)
"""
from django.shortcuts import render, get_object_or_404, redirect
from .models import Vuelo, Boleto

def vista_moderador(request):
    vuelos = Vuelo.objects.all()
    
    # Agregar información de asientos disponibles
    for vuelo in vuelos:
        boletos_vendidos = Boleto.objects.filter(vuelo=vuelo).count()
        vuelo.asientos_disponibles = vuelo.avion.cantidad_asientos - boletos_vendidos  # Nueva propiedad dinámica

    return render(request, "aplicacion/moderador_dashboard.html", {"vuelos": vuelos})

def es_administrador(user):
    return user.groups.filter(name="Administrador").exists()

@login_required
@user_passes_test(es_administrador)
def vista_admin(request):
    return render(request, "admin_dashboard.html")


from django import forms

class VentaBoletoForm(forms.Form):
    CLASE_ASIENTO_CHOICES = [
        ('PRIMERA', 'Primera Clase'),
        ('SEGUNDA', 'Segunda Clase'),
        ('TERCERA', 'Tercera Clase'),
    ]
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    clase_asiento = forms.ChoiceField(choices=CLASE_ASIENTO_CHOICES)

def vender_boleto(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    boletos_vendidos = Boleto.objects.filter(vuelo=vuelo).count()
    asientos_disponibles = vuelo.avion.cantidad_asientos - boletos_vendidos

    if asientos_disponibles <= 0:
        return redirect("vista_moderador")

    if request.method == "POST":
        form = VentaBoletoForm(request.POST)
        if form.is_valid():
            Boleto.objects.create(
                vuelo=vuelo,
                pasajero_nombre=form.cleaned_data["nombre"],
                pasajero_apellidos=form.cleaned_data["apellidos"],
                clase_asiento=form.cleaned_data["clase_asiento"]
            )
            return redirect("vista_moderador")
    else:
        form = VentaBoletoForm()

    return render(request, "aplicacion/vender_boleto.html", {"form": form, "vuelo": vuelo, "asientos_disponibles": asientos_disponibles})
