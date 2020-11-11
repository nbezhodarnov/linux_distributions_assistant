from django.shortcuts import render
from .models import Distributions, Reviews
from django.views.generic import DetailView
from django.contrib.auth.models import User
from . import forms

# Create your views here.

class DistributionDetailView(DetailView):
	model = Distributions
	template_name = 'distributions_list/dist.html'
	context_object_name = 'dist'
	
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['form'] = forms.ReviewForm()
		reviews = Reviews.objects.filter(dist_id=data['dist'].id).select_related('user_id')
		if (reviews):
			data['reviews'] = reviews.order_by('date')
		return data

def index(request):
	dists = Distributions.objects.order_by('name');
	criteries = {
		'slides': [
			{ 'id': 'popularity', 'name': 'Популярность'},
			{ 'id': 'support', 'name': 'Поддерживаемость сообществом'},
			{ 'id': 'stability', 'name': 'Надёжность и стабильность'},
			{ 'id': 'user-friendly', 'name': 'Простота в использовании'},
			{ 'id': 'program-update-frequency', 'name': 'Частота обновлений программ'},
			{ 'id': 'customizability', 'name': 'Настраиваемость системы'},
			{ 'id': 'consumption', 'name': 'Потребление'}
		]
	}
	return render(request, 'distributions_list/index.html', {'criteries': criteries, 'dists': dists})
