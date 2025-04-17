from django.shortcuts import render, redirect, get_object_or_404
from .forms import HistoricoSaudeForm, LoginForm, RegisterForm, FormularioPersonalizadoForm
from .models import HistoricoSaude, FormularioPersonalizado, RespostaFormulario
from datetime import date, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import urllib.parse

def enviar_formulario(request):
    if request.method == 'POST':
        form = HistoricoSaudeForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            instancia = form.save(commit=False)
            instancia.usuario = request.user
            instancia.save()

            mensagem = f"""
📋 *Novo formulário de paciente recebido*:
👤 Nome: {instancia.nome}
📱 Telefone: {instancia.telefone}
📧 Email: {instancia.email}
🎂 Data de nascimento: {instancia.data_nascimento}
🏥 Convênio: {instancia.convenio}
🦷 Motivo: {instancia.motivo_da_consulta}
❗ Doenças crônicas? {'Sim' if instancia.possui_doencas_cronicas else 'Não'}
⚠️ Alergias: {instancia.alergias}
💊 Medicamentos: {instancia.uso_medicamentos}
📝 Histórico Médico: {instancia.historico_medico}
"""
            numero_destino = '5582982137598'
            mensagem_encoded = urllib.parse.quote(mensagem)
            link_whatsapp = f"https://wa.me/{numero_destino}?text={mensagem_encoded}"

            return redirect(link_whatsapp)
    else:
        form = HistoricoSaudeForm()
    
    return render(request, 'formulario.html', {'form': form})

def dashboard(request):
    total_pacientes = HistoricoSaude.objects.count()
    ultimos_30_dias = date.today() - timedelta(days=30)
    consultas_recentes = HistoricoSaude.objects.filter(ultima_consulta__gte=ultimos_30_dias).count()
    contexto = {
        'total_pacientes': total_pacientes,
        'consultas_recentes': consultas_recentes,
    }
    return render(request, 'dashboard.html', contexto)

def login_paciente(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('area_paciente')  # Redireciona para área do paciente
    else:
        form = LoginForm()
    return render(request, 'paciente_login.html', {'form': form})

def register_paciente(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('area_paciente')
    else:
        form = RegisterForm()
    return render(request, 'paciente_register.html', {'form': form})

@login_required
def area_paciente(request):
    try:
        historico = request.user.historico
    except HistoricoSaude.DoesNotExist:
        return redirect('formulario')
    
    formularios = FormularioPersonalizado.objects.all()
    respostas = RespostaFormulario.objects.filter(usuario=request.user)
    
    return render(request, 'paciente_area.html', {
        'user': request.user,
        'historico': historico,
        'formularios': formularios,
        'respostas': respostas,
    })

def logout_paciente(request):
    logout(request)
    return redirect('login_paciente')

@login_required
def formulario_personalizado(request, formulario_id):
    formulario = get_object_or_404(FormularioPersonalizado, id=formulario_id)
    if request.method == 'POST':
        form = FormularioPersonalizadoForm(request.POST, formulario=formulario)
        if form.is_valid():
            for campo in formulario.campos.all():
                valor = form.cleaned_data[f'campo_{campo.id}']
                RespostaFormulario.objects.create(
                    formulario=formulario,
                    usuario=request.user,
                    campo=campo,
                    valor=valor
                )
            return redirect('area_paciente')
    else:
        form = FormularioPersonalizadoForm(formulario=formulario)
    return render(request, 'formulario_personalizado.html', {'form': form, 'formulario': formulario})