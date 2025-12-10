from django import forms
from .models import NewsItem

class NewsItemForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ['titulo', 'contenido', 'publicado', 'fecha_expiracion']
        widgets = {
            'fecha_expiracion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }