from django.contrib import admin
from .models import Vuelo,Terminal,Boleto,Pasajero,Avion

# Register your models here.
admin.site.register(Vuelo)
admin.site.register(Terminal)
admin.site.register(Boleto)
admin.site.register(Pasajero)
admin.site.register(Avion)