from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Proof")


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
            fecha_obj = datetime.strptime(
                fecha_str, "%Y-%m-%d"
            ).date()  # Convertir string a date
            vuelos = Vuelo.objects.filter(
                terminal_id=terminal_id,
                fecha_salida__date=fecha_obj,  # Ignorar la hora en la comparación
            )
        except ValueError:
            vuelos = []  # Si la fecha es inválida, retorna lista vacía

    return render(
        request,
        "aplicacion/usuario_dashboard.html",
        {"terminales": terminales, "vuelos": vuelos},
    )


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
        vuelo.asientos_disponibles = (
            vuelo.avion.cantidad_asientos - boletos_vendidos
        )  # Nueva propiedad dinámica

    return render(request, "aplicacion/moderador_dashboard.html", {"vuelos": vuelos})


def es_administrador(user):
    return user.groups.filter(name="Administrador").exists()


"""
@login_required
@user_passes_test(es_administrador)
"""


def vista_admin(request):
    return render(request, "aplicacion/admin_dashboard.html")


from django import forms

from django import forms
from .models import Boleto


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Vuelo, Boleto, Pasajero
from .forms import VentaBoletoForm

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Vuelo, Boleto

def obtener_asientos_disponibles(request):
    vuelo_id = request.GET.get("vuelo_id")
    clase = request.GET.get("clase")

    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asientos_ocupados = set(Boleto.objects.filter(vuelo=vuelo).values_list("numero_asiento", flat=True))

    # Obtener rangos de asientos según la clase
    rangos = vuelo.obtener_rangos_asientos()
    
    # Filtrar solo los asientos disponibles en la clase seleccionada
    asientos_disponibles = [asiento for asiento in rangos[clase] if asiento not in asientos_ocupados]
    print("TESTING______________",asientos_disponibles)
    return JsonResponse({"asientos": asientos_disponibles})

def obtener_asientos_disponibles_directo(vuelo, clase):
    """ Función auxiliar para obtener asientos disponibles directamente sin JSON """
    if clase is None:
        return None
    asientos_ocupados = set(Boleto.objects.filter(vuelo=vuelo).values_list("numero_asiento", flat=True))
    rangos = vuelo.obtener_rangos_asientos()
    return [asiento for asiento in rangos[clase] if asiento not in asientos_ocupados]

from django.shortcuts import render, get_object_or_404, redirect
from .models import Vuelo, Boleto, Pasajero
from .forms import VentaBoletoForm

def vender_boleto(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    
    if request.method == "POST":
        form = VentaBoletoForm(request.POST)
        if form.is_valid():
            clase_asiento = form.cleaned_data["clase_asiento"]
            numero_asiento = int(form.cleaned_data["numero_asiento"])

            # Validar que el asiento seleccionado está disponible
            asientos_disponibles = obtener_asientos_disponibles_directo(vuelo, clase_asiento)

            if numero_asiento not in vuelo.obtener_rangos_asientos()[clase_asiento]:
                return render(request, "aplicacion/vender_boleto.html", {
                    "form": form, 
                    "vuelo": vuelo, 
                    "error": ("Asiento no válido. Por favor intruduzca un número válido")
                })
            if numero_asiento not in asientos_disponibles:
                return render(request, "aplicacion/vender_boleto.html", {
                    "form": form, 
                    "vuelo": vuelo, 
                    "error": "El asiento seleccionado ya está ocupado. Intente con otro."
                })
    
            # Crear o buscar el pasajero
            pasajero, _ = Pasajero.objects.get_or_create(
                nombre=form.cleaned_data["nombre"],
                apellidos=form.cleaned_data["apellidos"]
            )

            # Crear el boleto
            Boleto.objects.create(
                vuelo=vuelo,
                pasajero=pasajero,  
                clase_asiento=clase_asiento,
                numero_asiento=numero_asiento,
                precio_pagado = 0
            )

            return redirect("vista_moderador")

    else:
        form = VentaBoletoForm()
    clase_asiento = request.GET.get("clase_asiento")
    clase_asiento = "SEGUNDA"
    print(clase_asiento)
    asientos_disponibles = obtener_asientos_disponibles_directo(vuelo, clase_asiento)
    return render(request, "aplicacion/vender_boleto.html", {
        "form": form, 
        "vuelo": vuelo,
        "asientos":asientos_disponibles
    })


def confirmacion_venta(request):
    return render(request, 'confirmacion_venta.html')

def detalles_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    boletos_vendidos = Boleto.objects.filter(vuelo=vuelo).count()
    asientos_disponibles = vuelo.avion.cantidad_asientos - boletos_vendidos

    data = {
        "id": vuelo.id,
        "terminal": vuelo.terminal.nombre,
        "pais_destino": vuelo.pais_destino,
        "ciudad_destino": vuelo.ciudad_destino,
        "fecha_salida": vuelo.fecha_salida.strftime("%Y-%m-%d %H:%M"),
        "fecha_arribo": vuelo.fecha_arribo.strftime("%Y-%m-%d %H:%M"),
        "tipo_vuelo": vuelo.get_tipo_vuelo_display(),
        "asientos_disponibles": asientos_disponibles,
        "boletos_vendidos": boletos_vendidos,
    }

    return JsonResponse(data)


def detalles_vuelo_pagina(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    boletos_vendidos = Boleto.objects.filter(vuelo=vuelo).count()
    asientos_disponibles = vuelo.avion.cantidad_asientos - boletos_vendidos

    return render(
        request,
        "aplicacion/detalles_vuelo.html",
        {
            "vuelo": vuelo,
            "boletos_vendidos": boletos_vendidos,
            "asientos_disponibles": asientos_disponibles,
        },
    )

