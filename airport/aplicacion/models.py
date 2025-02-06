from django.db import models

# Create your models here.
class Terminal(models.Model):
    numero = models.IntegerField(unique=True)  # Número de terminal
    nombre = models.CharField(max_length=100, unique=True)  # Nombre de la terminal

    def __str__(self):
        return f"Terminal {self.numero} - {self.nombre}"
    
from django.db import models

class Vuelo(models.Model):
    TIPO_VUELO_CHOICES = [
        ('NACIONAL', 'Nacional'),
        ('INTERNACIONAL', 'Internacional'),
    ]

    terminal = models.ForeignKey('Terminal', on_delete=models.CASCADE)
    avion = models.ForeignKey('Avion', on_delete=models.CASCADE)
    pais_destino = models.CharField(max_length=100)
    ciudad_destino = models.CharField(max_length=100)
    fecha_salida = models.DateTimeField()
    fecha_arribo = models.DateTimeField()
    tipo_vuelo = models.CharField(
        max_length=13, 
        choices=TIPO_VUELO_CHOICES, 
        default='NACIONAL'
    )

    def obtener_rangos_asientos(self):
        """
        Calcula los rangos de asientos disponibles según la distribución de clases:
        - 15% Primera Clase (asientos más bajos primero)
        - 25% Segunda Clase
        - 60% Tercera Clase
        """
        total_asientos = self.avion.cantidad_asientos
        primera_fin = int(total_asientos * 0.15)  # 15% para primera clase
        segunda_fin = primera_fin + int(total_asientos * 0.25)  # 25% para segunda clase
        tercera_fin = total_asientos  # 60% restante para tercera clase

        return {
            'PRIMERA': range(1, primera_fin + 1),
            'SEGUNDA': range(primera_fin + 1, segunda_fin + 1),
            'TERCERA': range(segunda_fin + 1, tercera_fin + 1),
        }

    def __str__(self):
        return f"Vuelo {self.id} - {self.tipo_vuelo} a {self.ciudad_destino} ({self.pais_destino})"


class Avion(models.Model):
    matricula = models.CharField(max_length=20, unique=True)  # Identificación única del avión
    modelo = models.CharField(max_length=50)
    fabricante = models.CharField(max_length=50)
    pais_fabricante = models.CharField(max_length=50)
    cantidad_asientos = models.IntegerField()
    
    def __str__(self):
        return f"{self.modelo} - {self.matricula}"

class Pasajero(models.Model):
    id = models.AutoField(primary_key=True)  # ID autoincrementable
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Boleto(models.Model):
    vuelo = models.ForeignKey('Vuelo', on_delete=models.CASCADE)
    pasajero = models.ForeignKey('Pasajero', on_delete=models.CASCADE)
    clase_asiento = models.CharField(
        max_length=10,
        choices=[('PRIMERA', 'Primera Clase'), ('SEGUNDA', 'Segunda Clase'), ('TERCERA', 'Tercera Clase')],
        default='TERCERA'
    )
    numero_asiento = models.IntegerField()  # Número de asiento asignado automáticamente

    precio_pagado = models.DecimalField(max_digits=10, decimal_places=4)  # Precio final del boleto

    def __str__(self):
        return f"Boleto {self.id} - {self.pasajero} - Vuelo {self.vuelo.id} - Asiento {self.numero_asiento}"
