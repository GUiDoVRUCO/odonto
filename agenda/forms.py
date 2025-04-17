from django import forms
from .models import HistoricoSaude, FormularioPersonalizado, RespostaFormulario
from django.contrib.auth.models import User

class HistoricoSaudeForm(forms.ModelForm):
    class Meta:
        model = HistoricoSaude
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'ultima_consulta': forms.DateInput(attrs={'type': 'date'}),
        }
        exclude = ['usuario']

class LoginForm(forms.Form):
    username = forms.EmailField(label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirme a Senha")

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class FormularioPersonalizadoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        formulario = kwargs.pop('formulario', None)
        super().__init__(*args, **kwargs)
        if formulario:
            for campo in formulario.campos.all():
                if campo.tipo == 'texto':
                    self.fields[f'campo_{campo.id}'] = forms.CharField(
                        label=campo.nome, required=campo.obrigatorio, widget=forms.TextInput(attrs={'class': 'form-input'})
                    )
                elif campo.tipo == 'texto_longo':
                    self.fields[f'campo_{campo.id}'] = forms.CharField(
                        label=campo.nome, required=campo.obrigatorio, widget=forms.Textarea(attrs={'class': 'form-textarea'})
                    )
                elif campo.tipo == 'sim_nao':
                    self.fields[f'campo_{campo.id}'] = forms.ChoiceField(
                        label=campo.nome, required=campo.obrigatorio, choices=[('Sim', 'Sim'), ('Não', 'Não')], widget=forms.RadioSelect(attrs={'class': 'form-radio'})
                    )