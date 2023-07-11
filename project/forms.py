from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Korisnik,Predmeti

class AddUserForm(UserCreationForm):  
    username = forms.CharField(label='Username', min_length=5, max_length=50, widget=forms.TextInput)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)  

    class Meta:
        model = Korisnik
        fields = ['username', 'password1', 'password2', 'role', 'status']


class AddSubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddSubjectForm, self).__init__(*args, **kwargs)
        self.fields.get('nositelj').queryset = Korisnik.objects.filter(role='prof')

    class Meta:
        model = Predmeti
        fields = ['name', 'kod', 'program', 'ects', 'sem_red', 'sem_izv', 'nositelj', 'izborni']