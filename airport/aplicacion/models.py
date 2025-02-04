from django.db import models

# Create your models here.
class Terminal(models.Model):
    numero = models.IntegerField(unique=True)  # Número de terminal
    nombre = models.CharField(max_length=100, unique=True)  # Nombre de la terminal

    def __str__(self):
        return f"Terminal {self.numero} - {self.nombre}"
    
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

    def __str__(self):
        return f"Vuelo {self.id} - {self.tipo_vuelo} a {self.ciudad_destino}"


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
    CLASE_ASIENTO_CHOICES = [
        ('PRIMERA', 'Primera Clase'),
        ('SEGUNDA', 'Segunda Clase'),
        ('TERCERA', 'Tercera Clase'),
    ]

    vuelo = models.ForeignKey('Vuelo', on_delete=models.CASCADE)  # Relación con el vuelo
    pasajero = models.ForeignKey('Pasajero', on_delete=models.CASCADE)  # Relación con el pasajero
    numero_asiento = models.IntegerField()
    clase_asiento = models.CharField(
        max_length=10,
        choices=CLASE_ASIENTO_CHOICES,
        default='TERCERA'
    )
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=4)  # Precio final del boleto

    def __str__(self):
        return f"Boleto {self.id} - {self.pasajero} - Vuelo {self.vuelo.id} - Asiento {self.numero_asiento}"
