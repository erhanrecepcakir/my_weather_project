from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=40, label='User Name')
    password = forms.CharField(max_length=20, label='Password', widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label='Confirm Password', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=50, label='Email', widget=forms.EmailInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        email = self.cleaned_data.get('email')

        if password and confirm and password != confirm:
            raise forms.ValidationError('Password Confirmation Error')

        values = {
            'username' : username,
            'password' : password,
            'email'     : email,
        }

        return values
