from django import forms
from .models import Boleto, Pasajero

class VentaBoletoForm(forms.Form):
    nombre = forms.CharField(max_length=50, label="Nombre del pasajero")
    apellidos = forms.CharField(max_length=50, label="Apellidos del pasajero")
    clase_asiento = forms.ChoiceField(
        choices=[('PRIMERA', 'Primera Clase'), ('SEGUNDA', 'Segunda Clase'), ('TERCERA', 'Tercera Clase')],
        label="Clase de asiento"
    )
    numero_asiento = forms.IntegerField(label="Número de asiento")
