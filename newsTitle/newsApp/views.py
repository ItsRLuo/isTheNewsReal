from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.contrib.auth.models import User
import ConfigParser
import os
import threading
from datetime import datetime
import json
from django.utils.encoding import smart_str, smart_unicode
import webhoseio
import requests

# Create your views here.
def index(request):
	#print request.GET.get("query")
	webhoseio.config(token='0a2e1cc2-76a5-4486-b360-6e9898937e2b')
	output = webhoseio.query("filterWebContent", {"q":request.GET.get("query"),"order":"desc"})
	csvs = ""
	accuracy = 50
#open file for reading
	#f = open("out.txt", "w")
	ff= "Files sent to Azeura---------------------------\n"
	ff+=("\"")
	ff+=("author,title,text,site_url,text,language,country,domain_rank,spam_score,replies_count,participants_count,likes,comments,shares") 
	ff+=("\"\n")
	ss = {"rec":[]}
	counter = 0
	for val in range(100):
		if "english" not in (smart_str(output['posts'][val]['language'])):
			continue
		counter += 1
		if counter == 4:
			break
		ff+=("\"")
		ff+=(smart_str(output['posts'][val]['author']))
		ff+=("\",")

		ff+=("\"")
		ff+=(smart_str(output['posts'][val]['thread']['title']))
		ff+=("\",")



		ff+=("\"")
		ff+=(smart_str(output['posts'][val]['thread']['url']))
		ff+=("\",")


		texts = smart_str(output['posts'][val]['text']).replace("\n", "")
		ff+=("\"")
		ff+=(texts)
		ff+=("\",")

		ff+=("\"")
		ff+=(smart_str(output['posts'][val]['language']))
		ff+=("\",")

		ff+=("\"")
		ff+=(smart_str(output['posts'][val]['thread']['country']))
		ff+=("\",")

		ff+=("\"")
		ff+=(str(output['posts'][val]['thread']['domain_rank']))
		ff+=("\",")

		ff+=("\"")
		ff+=(str(output['posts'][val]['thread']['spam_score']))
		ff+=("\",")

		ff+=("\"")
		ff+=(str(output['posts'][val]['thread']['replies_count']))
		ff+=("\"")

		ff+=("\"")
		ff+=(str(output['posts'][val]['thread']['participants_count']))
		ff+=("\",")

		ff+=("\"")
		ff+=(str(output['posts'][val]['thread']['social']['facebook']['likes']))
		ff+=("\",")

		ff+=("\"")
		ff+=(str(output['posts'][val]['thread']['social']['facebook']['comments']))
		ff+=("\",")

		ff+=("\"")
		ff+=(str(output['posts'][val]['thread']['social']['facebook']['shares']))
		ff+=("\",")
		accuracy += 10
		ss["rec"].append(({'link':smart_str(output['posts'][val]['thread']['url']),'title':smart_str(output['posts'][val]['thread']['title']), 'text':smart_str(output['posts'][val]['text']).replace("\n", ""), "accuracy":accuracy}))
		ff+=('\n')

	# Get the next batch of posts
		output = webhoseio.get_next()
		#print(output['posts'][val]['thread']['site'] # print the site of the first post
	ss = json.dumps(ss)
	#erase all content of the file
	#f.close();
	r = requests.post("https://ussouthcentral.services.azureml.net/workspaces/986734c099e54db2b844ca45d9c40ed9/services/3258142446ef424f9633019cdad280ba/execute?api-version=2.0&details=true", data=ff)
	print(r.status_code, r.reason)
	print r.text[300:]

	print ss
	return HttpResponse(ss)
	
