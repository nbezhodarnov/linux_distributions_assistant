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
	return render(request, 'distributions_list/index.html')#, {'dists': dists})
