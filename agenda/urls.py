from django.urls import path
from . import views

urlpatterns = [
    path('', views.enviar_formulario, name='formulario'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_paciente, name='login_paciente'),
    path('register/', views.register_paciente, name='register_paciente'),
    path('area/', views.area_paciente, name='area_paciente'),
    path('logout/', views.logout_paciente, name='logout_paciente'),
    path('formulario/<int:formulario_id>/', views.formulario_personalizado, name='formulario_personalizado'),
]