from django.contrib import admin
from .models import HistoricoSaude, FormularioPersonalizado, CampoFormulario, RespostaFormulario

@admin.register(HistoricoSaude)
class HistoricoSaudeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'ultima_consulta')
    search_fields = ('nome', 'email')
    list_filter = ('ultima_consulta', 'possui_doencas_cronicas')

@admin.register(FormularioPersonalizado)
class FormularioPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em')
    search_fields = ('nome',)

@admin.register(CampoFormulario)
class CampoFormularioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'formulario', 'tipo', 'obrigatorio')
    search_fields = ('nome',)
    list_filter = ('formulario', 'tipo')

@admin.register(RespostaFormulario)
class RespostaFormularioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'formulario', 'campo', 'valor', 'respondido_em')
    search_fields = ('usuario__username', 'valor')
    list_filter = ('formulario', 'respondido_em')