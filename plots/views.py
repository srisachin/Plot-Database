#from django.shortcuts import render
from django.shortcuts import render_to_response
import pickle
#from django.http import HttpResponse
#from django.template import RequestContext, loader
import pandas as pd;
from collections import defaultdict;
from django.template.context_processors import csrf
import re;
import numpy as np;
import Generate;
import Groupby;
import Genplots;
import settings;

def index(request):
	plots = defaultdict(list);    
	with open('/home/sachin/mysite/plots/static/plots/plots.pickle', 'rb') as handle:
		plots = pickle.load(handle)
	with open('/home/sachin/mysite/plots/static/plots/scores.pickle', 'rb') as handle:
		scores = pickle.load(handle)
	
	if request.method == 'POST':
#		X = plots['all'];
#		T = [scores[i] for i in X];
#		T = [0 if np.isnan(x) else x for x in T];
#		Y= [x for (t,x) in sorted(zip(T,X),reverse=True)];
#		Y = map(str, Y)
#		T = sorted(T,reverse=True)
		if(not request.FILES):
			f='wine.csv';
		else:
			f=request.FILES['myfile']
			fs=request.FILES['myschema']
		
		with open('file.csv', 'wb+') as destination:
		        for chunk in f.chunks():
		            destination.write(chunk)
		
		with open('schema.csv', 'wb+') as destination:
		        for chunk in fs.chunks():
		            destination.write(chunk)
		
		Generate.main("schema.csv", "prototype.csv")
		Groupby.main("file.csv", "schema.csv")
		Genplots.main("file.csv", "experiment.csv", "groups.csv")
		p=list(range(settings.count))
		p=map(str,p)
#		return render_to_response("plots/index.html", {'plots_scores': zip(Y,T), 'filename' : f})
		return render_to_response("plots/index.html", { 'plots':p, 'filename' : f})		

	if request.method == 'GET': # If the form is submitted		        	
		f='';		
		search_query = request.GET.get('search_box', None)
		X = plots[str(search_query).lower()];
		T = [scores[i] for i in X];
		T = [0 if np.isnan(x) else x for x in T];
		Y= [x for (t,x) in sorted(zip(T,X),reverse=True)];
		Y = map(str, Y)
		T = sorted(T,reverse=True)
	return render_to_response('plots/index.html',
#                              {'plots': plots[search_query]})
				{'plots_scores': zip(Y,T), 'filename' : f})
