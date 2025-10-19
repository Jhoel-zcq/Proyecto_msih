# blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # Modelo asociado
        fields = ['titulo', 'contenido']  # Campos que el usuario puede llenar
