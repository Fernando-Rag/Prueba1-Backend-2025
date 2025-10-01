"""
URL configuration for GestorDeVisitas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.registroVisitante, name='home'),
    path('registroVisitante/', views.registroVisitante, name='registroVisitante'),
    path('registroEntrada/', views.registroEntrada, name='registroEntrada'),
    path('registroSalida/', views.registroSalida, name='registroSalida'),
    path('busquedaVisitantes/', views.busquedaVisitantes, name='busquedaVisitantes'),
    path('visitante/<int:pk>/update/', views.visitante_update, name='visitante_update'),
    path('visitante/<int:pk>/delete/', views.visitante_delete, name='visitante_delete'),
]