from .models import HistoricoSaude
from datetime import date
import webbrowser
import urllib.parse

def enviar_mensagens_retorno(dias_sem_consulta=30):
    hoje = date.today()
    pacientes = HistoricoSaude.objects.filter(ultima_consulta__isnull=False)

    for paciente in pacientes:
        dias_passados = (hoje - paciente.ultima_consulta).days
        if dias_passados >= dias_sem_consulta:
            msg = f"Olá {paciente.nome}, sentimos sua falta! Que tal agendar sua próxima consulta? 😁🦷"
            link = f"https://wa.me/55{paciente.telefone}?text={urllib.parse.quote(msg)}"
            webbrowser.open(link)
