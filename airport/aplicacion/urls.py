from django.urls import path
from .views import vista_usuario, vista_moderador,detalles_vuelo, vista_admin,index,vender_boleto,detalles_vuelo_pagina
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("", index,name = "index"),
    path("vuelos/", vista_usuario, name="vista_usuario"),
    path("moderador/", vista_moderador, name="vista_moderador"),
    path("admin-panel/", vista_admin, name="vista_admin"),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='vuelos'), name='logout'),  # Redirige a login tras cerrar sesión
    path('moderador/vender/<int:vuelo_id>/', vender_boleto, name='vender_boleto'),
    path('vuelo/detalles/pagina/<int:vuelo_id>/', detalles_vuelo_pagina, name='detalles_vuelo_pagina'),
    path('vender_boleto/<int:vuelo_id>/', views.vender_boleto, name='vender_boleto'),
    path('confirmacion_venta/', views.confirmacion_venta, name='confirmacion_venta'),
   path('obtener_asientos_disponibles/<int:vuelo_id>/<str:clase_asiento>/', views.obtener_asientos_disponibles, name='obtener_asientos_disponibles'),

]
