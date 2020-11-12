from django.shortcuts import render
from .models import Distributions, Reviews
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime
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
			data['reviews'] = reviews.order_by('-date')
		return data
	
	def post(self, request, *args, **kwargs):
		form = forms.ReviewForm(request.POST)
		self.object = self.get_object()
		data = super(DistributionDetailView, self).get_context_data(**kwargs)
		if (self.request.user.is_authenticated):
			data['form'] = forms.ReviewForm(request.POST)
			if (form.is_valid() and form.cleaned_data.get("text")):
				obj = form.save(commit=False)
				if (obj.rate > 0):
					obj.user_id = self.request.user
					obj.dist_id = data['dist']
					obj.date = datetime.now()
					obj.save()
					reviews = Reviews.objects.filter(dist_id=data['dist'].id).select_related('user_id')
					if (reviews):
						data['reviews'] = reviews.order_by('-date')
					data['form'] = forms.ReviewForm()
					return self.render_to_response(context=data)
				else:
					data['error'] = 'Пожалуйста, выставите оценку'
			else:
				if (form.cleaned_data.get("text")):
					data['error'] = 'Ошибка валидации данных'
				else:
					data['error'] = 'Пожалуйста, напишите отзыв'
		else:
			data['error'] = 'Только авторизированные пользователи могут оставлять отзывы'
		reviews = Reviews.objects.filter(dist_id=data['dist'].id).select_related('user_id')
		if (reviews):
			data['reviews'] = reviews.order_by('-date')
		return self.render_to_response(context=data)

class ReviewUpdateView(UpdateView):
	model = Reviews
	template_name = 'distributions_list/dist_edit.html'
	context_object_name = 'review'
	
	form_class = forms.ReviewForm
	
	

def index(request):
	criteries = {
		'slides': [
			{ 'id': 'popularity', 'name': 'Популярность', 'from': '0', 'to': '5'},
			{ 'id': 'support', 'name': 'Поддерживаемость сообществом', 'from': '0', 'to': '5'},
			{ 'id': 'stability', 'name': 'Надёжность и стабильность', 'from': '0', 'to': '5'},
			{ 'id': 'user-friendly', 'name': 'Простота в использовании', 'from': '0', 'to': '5'},
			{ 'id': 'program-update-frequency', 'name': 'Частота обновлений программ', 'from': '0', 'to': '5'},
			{ 'id': 'customizability', 'name': 'Настраиваемость системы', 'from': '0', 'to': '5'},
			{ 'id': 'consumption', 'name': 'Потребление', 'from': '0', 'to': '5'}
		]
	}
	
	parameters = [[0, 5]] * 7
	i = 0
	
	if (request.method == 'POST'):
		for element in criteries['slides']:
			if (request.POST[element['id']][0].isnumeric() and request.POST[element['id']][2].isnumeric()):
				parameters[i] = [request.POST[element['id']][0], request.POST[element['id']][2]]
				criteries['slides'][i]['from'] = parameters[i][0]
				criteries['slides'][i]['to'] = parameters[i][1]
			i += 1
	
	dists = Distributions.objects.filter(
		Q(popularity__gte=parameters[0][0]) & Q(popularity__lte=parameters[0][1]) &
		Q(society_support__gte=parameters[1][0]) & Q(society_support__lte=parameters[1][1]) &
		Q(stability__gte=parameters[2][0]) & Q(stability__lte=parameters[2][1]) &
		Q(user_friendly__gte=parameters[3][0]) & Q(user_friendly__lte=parameters[3][1]) &
		Q(programs_update_frequency__gte=parameters[4][0]) & Q(programs_update_frequency__lte=parameters[4][1]) &
		Q(customizability__gte=parameters[5][0]) & Q(customizability__lte=parameters[5][1]) &
		Q(consumption__gte=parameters[6][0]) & Q(consumption__lte=parameters[6][1])
	).order_by('name')
	
	return render(request, 'distributions_list/index.html', {'criteries': criteries, 'dists': dists})
