from django.shortcuts import render
from .models import Distributions
from django.views.generic import DetailView

# Create your views here.

class DistributionDetailView(DetailView):
	model = Distributions
	template_name = 'distributions_list/index.html'
	context_object_name = 'dist'

def index(request):
	#dists = Distributions.objects.order_by('name');
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
	return render(request, 'distributions_list/index.html', {'criteries': criteries})
