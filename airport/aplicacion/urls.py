from django.urls import path
from .views import vista_usuario, vista_moderador, vista_admin,index

urlpatterns = [
    path("", index,name = "index"),
    path("vuelos/", vista_usuario, name="vista_usuario"),
    path("moderador/", vista_moderador, name="vista_moderador"),
    path("admin-panel/", vista_admin, name="vista_admin"),
]
