from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs = {'class': 'form-control', 'type': 'email', 'placeholder': 'Email'}
        self.fields['password'].widget.attrs = {'class': 'form-control', 'placeholder': 'Senha'}
