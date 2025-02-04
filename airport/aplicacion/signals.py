
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    if sender.name == "app_aeropuerto":  # Asegura que se ejecuta solo en tu app
        Group.objects.get_or_create(name="Usuario")
        Group.objects.get_or_create(name="Moderador")
        Group.objects.get_or_create(name="Administrador")
