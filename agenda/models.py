from django.db import models
from datetime import date
from django.contrib.auth.models import User

class HistoricoSaude(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='historico')
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    data_nascimento = models.DateField()
    convenio = models.CharField(max_length=100, blank=True)
    motivo_da_consulta = models.TextField(blank=True)
    possui_doencas_cronicas = models.BooleanField(default=False)
    alergias = models.TextField(blank=True)
    uso_medicamentos = models.TextField(blank=True)
    historico_medico = models.TextField()
    ultima_consulta = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome

    def dias_desde_ultima_consulta(self):
        if self.ultima_consulta:
            return (date.today() - self.ultima_consulta).days
        return None

class FormularioPersonalizado(models.Model):
    nome = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class CampoFormulario(models.Model):
    TIPO_CAMPO_CHOICES = [
        ('texto', 'Texto Curto'),
        ('texto_longo', 'Texto Longo'),
        ('sim_nao', 'Sim/Não'),
    ]
    formulario = models.ForeignKey(FormularioPersonalizado, on_delete=models.CASCADE, related_name='campos')
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CAMPO_CHOICES)
    obrigatorio = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} ({self.formulario.nome})"

class RespostaFormulario(models.Model):
    formulario = models.ForeignKey(FormularioPersonalizado, on_delete=models.CASCADE, related_name='respostas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respostas_formularios')
    campo = models.ForeignKey(CampoFormulario, on_delete=models.CASCADE)
    valor = models.TextField()
    respondido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resposta de {self.usuario.username} para {self.campo.nome}"