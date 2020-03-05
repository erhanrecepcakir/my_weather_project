from django import forms
from .models import City

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name', 'style' : 'text-transform:capitalize'})}
    
    def clean_name(self):
        return self.cleaned_data['name'].capitalize()


class SubscribeForm(forms.Form):
    task_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))