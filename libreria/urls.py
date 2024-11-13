from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path("inicio", views.inicio, name="inicio"),
    path("ingreso", views.ingreso, name="ingreso"),
    path("resultados", views.resultados, name="resultados"),
]
