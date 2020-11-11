from django import forms
from django.forms import Textarea, TextInput
from . import models

class ReviewForm(forms.ModelForm):
	class Meta:
		model = models.Reviews
		fields = ('rate', 'text')
		
		widgets = {
			"rate": TextInput(attrs={
				'id': 'rate',
				'type': 'range',
				'data-min': '0',
				'data-max': '5',
				'data-step': '1',
				'value': '0',
				'class': 'rating rating-loading'
			}),
			"text": Textarea(attrs={
				'class': 'form-control',
				'placeholder': 'Отзыв'
			})
		}
