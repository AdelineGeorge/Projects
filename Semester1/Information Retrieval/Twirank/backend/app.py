
from flask import Flask, jsonify, render_template,request,redirect,session
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
app = Flask(__name__)
CORS(app)
import os
import pysolr
import requests
import json
import urllib
from deep_translator import GoogleTranslator
import pickle
from langdetect import detect
from urllib.parse import urlencode
import nltk
nltk.download('vader_lexicon')
from textblob import TextBlob


from nltk.sentiment import SentimentIntensityAnalyzer

import string
app.config['CORS_HEADERS'] = 'Content-Type'
CORE_NAME = "BM25-12"
AWS_IP = "3.145.133.242"

@app.route("/")
@cross_origin()
def hello():
	return jsonify({"text": "Changed now"})


@app.route("/getAnalytics",methods=['GET'])
@cross_origin()

def getAnalytics():
	Analytics = dict()
	i = Indexer()
	if request.method=='GET':
		 Analytics['tweet_count_per_lang'] = i.tweet_count_per_lang()
		 Analytics['countrywise_vaccine_count'] = i.countrywise_vaccine_count()
		 Analytics['vacc_for_and_against'] = i.vacc_for_and_against()
		 Analytics['top_5_POIs'] = i.top_5_POIs()
		 Analytics['POI_covid_tweets'] = i.POI_covid_tweets()
		 Analytics['public_for_against'] = i.public_for_against()
		 response = app.response_class(
			response=json.dumps(Analytics),
			mimetype='application/json'
			)
			
	return response

@app.route("/search",methods=['POST'])
@cross_origin()

def search():
	i = Indexer()
	if request.method=="POST":
		query = request.json
		result = i.search1(query)
		response = app.response_class(
			response=json.dumps(result),
			mimetype='application/json'
			)
		return response
		#return jsonify({"text": "Query Received successfully", "query": str(query)})

@app.route("/filter",methods=['POST'])
@cross_origin()	

def filter():
	i = Indexer()
	if request.method=='POST':
		query = request.json
		return i.filter(query)


class Indexer:
	def __init__(self):
		self.solr_url = f'http://{AWS_IP}:8983/solr/'
		self.connection = pysolr.Solr(self.solr_url + CORE_NAME, always_commit=True, timeout=5000000)

	# Tweet Count per language
	def tweet_count_per_lang(self):

		tweet_count = dict()
		model_name='BM25-12'
		query = {
			"fl" : "*,score",
			"q": "tweet_lang:\"en\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"qf": ""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		tweet_count['English_tweets'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
			"q": "tweet_lang:\"hi\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"qf": ""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		tweet_count['Hindi_tweets'] = json.loads(data.decode('utf-8'))['response']['numFound']

		
		query = {
			"fl" : "*,score",
			"q": "tweet_lang:\"es\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"qf": ""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		tweet_count['Spanish_tweets'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		return tweet_count

	# Country-wise preferred vaccines
	def countrywise_vaccine_count(self):

		countrywise_vaccine_count = dict()
		model_name='BM25-12'
		query = {
			"fl" : "*,score",
			"q":"text_en:\"pfizer\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"qf": ""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		countrywise_vaccine_count['USA_Pfizer'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
			"q":"text_en:\"moderna\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"qf": ""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		countrywise_vaccine_count['USA_Moderna'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		query = {
			"fl" : "*,score",
			"q":"text_es:\"pfizer\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"qf": ""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		countrywise_vaccine_count['Mexico_Pfizer'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
			"q":"text_es:\"moderna\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"qf": ""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		countrywise_vaccine_count['Mexico_Moderna'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		query = {
			"fl" : "*,score",
			"q":"text_hi:\"covishield\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"qf": ""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		countrywise_vaccine_count['India_Covishield'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		query = {
			"fl" : "*,score",
			"q":"text_hi:\"covaxin\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"qf": ""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		countrywise_vaccine_count['India_Covaxin'] = json.loads(data.decode('utf-8'))['response']['numFound']

		countrywise_vaccine_count['USA_Total'] = countrywise_vaccine_count['USA_Pfizer'] + countrywise_vaccine_count['USA_Moderna']
		countrywise_vaccine_count['USA_Pfizer'] = countrywise_vaccine_count['USA_Pfizer'] / countrywise_vaccine_count['USA_Total'] * 100
		countrywise_vaccine_count['USA_Moderna'] = countrywise_vaccine_count['USA_Moderna'] / countrywise_vaccine_count['USA_Total'] * 100
		countrywise_vaccine_count['Mexico_Total'] = countrywise_vaccine_count['Mexico_Pfizer'] + countrywise_vaccine_count['Mexico_Moderna']
		countrywise_vaccine_count['Mexico_Pfizer'] = countrywise_vaccine_count['Mexico_Pfizer'] / countrywise_vaccine_count['Mexico_Total'] * 100
		countrywise_vaccine_count['Mexico_Moderna'] = countrywise_vaccine_count['Mexico_Moderna'] / countrywise_vaccine_count['Mexico_Total'] * 100			
		countrywise_vaccine_count['India_Total'] = countrywise_vaccine_count['India_Covishield'] + countrywise_vaccine_count['India_Covaxin']
		countrywise_vaccine_count['India_Covishield'] = countrywise_vaccine_count['India_Covishield'] / countrywise_vaccine_count['India_Total'] * 100
		countrywise_vaccine_count['India_Covaxin'] = countrywise_vaccine_count['India_Covaxin'] / countrywise_vaccine_count['India_Total'] * 100
		
		return countrywise_vaccine_count

	# Country-wise metric - for and against Vaccines
	def vacc_for_and_against(self):

		vacc_for_and_against = dict()
		model_name='BM25-12'
		query = {
			"fl" : "*,score",
			"q":"text_en: \"vaccine hesitancy\"  \ntext_en: \"skeptic\"\ntext_en: \"fear\" OR \"vaccine\" \ntext_en: \"against\" OR \"vaccines\"\ntext_es: \"hesitancy\" \ntext_es: \"vacilación de la vacuna\" \ntext_es:  \"vacilación\" \ntext_es: \"miedo\"\ntext_hi: \"संदेह\"\ntext_hi:\"hesitancy\" OR \"fear\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "country:\"USA\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		vacc_for_and_against['USA_against'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
			"q":"text_en:\"vaccine hesitancy\"  \ntext_en: \"skeptic\"\ntext_en: \"fear\" OR \"vaccine\" \ntext_en: \"against\" OR \"vaccines\"\ntext_es: \"hesitancy\" \ntext_es: \"vacilación de la vacuna\" \ntext_es:  \"vacilación\" \ntext_es: \"miedo\"\ntext_hi: \"संदेह\"\ntext_hi:\"hesitancy\" OR \"fear\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "country:\"INDIA\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		vacc_for_and_against['INDIA_against'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		query = {
			"fl" : "*,score",
			"q":"text_en:\"vaccine hesitancy\"  \ntext_en: \"skeptic\"\ntext_en: \"fear\" OR \"vaccine\" \ntext_en: \"against\" OR \"vaccines\"\ntext_es: \"hesitancy\" \ntext_es: \"vacilación de la vacuna\" \ntext_es:  \"vacilación\" \ntext_es: \"miedo\"\ntext_hi: \"संदेह\"\ntext_hi:\"hesitancy\" OR \"fear\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "country:\"MEXICO\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		vacc_for_and_against['MEXICO_against'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
			"q":"text_en: \"pro vaccine\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "country:\"USA\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		vacc_for_and_against['USA_for'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		query = {
			"fl" : "*,score",
			"q":"text_en: \"pro vaccine\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "country:\"INDIA\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		vacc_for_and_against['INDIA_for'] = json.loads(data.decode('utf-8'))['response']['numFound']		

		query = {
			"fl" : "*,score",
			"q":"text_en: \"pro vaccine\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "country:\"MEXICO\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		vacc_for_and_against['MEXICO_for'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		return vacc_for_and_against

	# Top 5 POIs persuading public to take vaccines
	def top_5_POIs(self):

		top_5_POIs = dict()
		model_name='BM25-12'
		query = {
			"fl" : "*,score",
			"q":"text_en: \"pro vaccine\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"CDCgov\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		top_5_POIs['CDCgov'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
			"q":"text_en: \"pro vaccine\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"MoHFW_INDIA\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		top_5_POIs['MoHFW_INDIA'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		query = {
			"fl" : "*,score",
			"q":"text_en: \"pro vaccine\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"POTUS\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		top_5_POIs['POTUS'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
			"q":"text_en: \"pro vaccine\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"narendramodi\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		top_5_POIs['narendramodi'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		query = {
			"fl" : "*,score",
			"q":"text_en: \"pro vaccine\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"LeaderMcConnell\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		top_5_POIs['LeaderMcConnell'] = json.loads(data.decode('utf-8'))['response']['numFound']		
		
		return top_5_POIs

	# Covid related POI tweets
	def POI_covid_tweets(self):

		POI_covid_tweets = dict()
		model_name='BM25-12'
		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"CDCgov\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['CDCgov'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"MoHFW_INDIA\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['MoHFW_INDIA'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"POTUS\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['POTUS'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"narendramodi\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['narendramodi'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"LeaderMcConnell\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['LeaderMcConnell'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"VP\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['VP'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"PressSec\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['PressSec'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"RahulGandhi\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['RahulGandhi'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"AmitShah\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['AmitShah'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"ArvindKejriwal\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['ArvindKejriwal'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"Lopezobrador\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['Lopezobrador'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"HLGatell\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['HLGatell'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"SaludEdomex\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['SaludEdomex'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"MarkoCortes\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['MarkoCortes'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"SSalud_mx\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['SSalud_mx'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"Irma_Sandoval\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['Irma_Sandoval'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"Claudiashein\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['Claudiashein'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"myogiadityanath\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['myogiadityanath'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"INCIndia\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['INCIndia'] = json.loads(data.decode('utf-8'))['response']['numFound']	

		query = {
			"fl" : "*,score",
      		"q":"text_en: \"pro vaccine\"\ntext_en: \"covid\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_en: \"free shots\"\ntext_en: \"vaccine camps\"\ntext_en: \"pfizer\"\ntext_en: \"moderna\"\ntext_en: \"astrazeneca\"\ntext_en: \"covishield\"\ntext_en: \"covaxin\"\ntext_hi: \"covid\"\ntext_hi:\"टीका\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_hi: \"covishield\"\ntext_hi: \"covaxin\"\ntext_hi: \"astrazeneca\"\ntext_es: \"covid\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"\ntext_es: \"pfizer\"\ntext_es: \"moderna\"\ntext_es: \"covishield\"\ntext_es: \"covaxin\"\ntext_es: \"astrazeneca\"\n\nhashtags: \"[\"pfizer\", \"covishield\", \"covaxin\", \"astrazeneca\", \"moderna\", \"vacuna\", \"getvaccinated\"]\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "poi_name:\"GOPLeader\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		POI_covid_tweets['GOPLeader'] = json.loads(data.decode('utf-8'))['response']['numFound']		
		
		return POI_covid_tweets

	# Public opinion for and against vaccines
	def public_for_against(self):

		public_for_against = dict()
		model_name='BM25-12'
		query = {
			"fl" : "*,score",
			"q":"text_en:\"vaccine hesitancy\"  \ntext_en: \"skeptic\"\ntext_en: \"fear\" OR \"vaccine\" \ntext_en: \"against\" OR \"vaccines\"\ntext_es: \"hesitancy\" \ntext_es: \"vacilación de la vacuna\" \ntext_es:  \"vacilación\" \ntext_es: \"miedo\"\ntext_hi: \"संदेह\"\ntext_hi:\"hesitancy\" OR \"fear\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "verified: \"false\""
		}
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		public_for_against['Public_against'] = json.loads(data.decode('utf-8'))['response']['numFound']

		query = {
			"fl" : "*,score",
			"q":"text_en: \"pro vaccine\"\ntext_en: \"vaccine\" OR \"positive\"\ntext_en: \"get vaccinated\"\ntext_hi: \"टीका लगवाना\"\ntext_hi: \"get vaccinated\"\ntext_hi: \"pro vaccine\"\ntext_es: \"pro vaccine\"\ntext_es: \"vaccine\" OR \"positive\"\ntext_es: \"get vaccinated\"\ntext_es: \"vacunarse\"\ntext_es: \"pro vacuna\"\ntext_es: \"vacunate\"",
			"rows": 50,
			"defType": "lucene",
			"wt": "json",
			"fq": "verified: \"false\""
		}			
		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		data = urllib.request.urlopen(inurl).read()
		public_for_against['Public_for'] = json.loads(data.decode('utf-8'))['response']['numFound']
		
		return public_for_against

	# Time series graph on POI tweets
	def timeline_data():
		time_line = dict()
		model_name='BM25-12'


	# Query filters
	# def filter(self, q):
	# 	model_name='BM25-12'
	# 	print(q)
	# 	w = q['query']
	# 	punc = string.punctuation.replace("#", "")
	# 	w = w.translate(str.maketrans('', '', punc)).split(" ",1)
	# 	hin, esp, eng = "","",""
	# 	for word in w:
	# 		queryText = word.replace("\n","")
	# 		lang = detect(queryText)
	# 		hi_t, es_t, en_t = "","",""
	# 		if lang == "hi":
	# 			hi_t = hi_t+" "+queryText
	# 			es_t = self.lang_trans("es", queryText)
	# 			en_t = self.lang_trans("en", queryText)
	# 		elif lang == "es":
	# 			es_t = queryText
	# 			hi_t = self.lang_trans("hi", queryText)
	# 			en_t = self.lang_trans("en", queryText)
	# 		else:
	# 			en_t = queryText
	# 			es_t = self.lang_trans("es", queryText)
	# 			hi_t = self.lang_trans("hi", queryText)
	# 		hin = hin + " " + hi_t
	# 		esp = esp + " " + es_t
	# 		eng = eng + " " + en_t

	# 	# Filters
	# 	#for lang in q['filters']['languages']:
	# 	# q1 = ''
	# 	# if 'Hindi' in q['filters']['languages']:
	# 	# 	q1 = q1 +  " text_hi: "+hin.strip()
	# 	# if 'English' in q['filters']['languages']:
	# 	# 	q1 = q1 +  " text_en: "+eng.strip()
	# 	# if 'Spanish' in q['filters']['languages']:
	# 	# 	q1 = q1 +  " text_es: "+esp.strip()
	# 	lang_filter = ' '.join(q['filters']['languages'])
	# 	if len(lang_filter) != 0:		
	# 		lang_filter = lang_filter.replace('Hindi', 'hi')
	# 		lang_filter = lang_filter.replace('Spanish', 'es')
	# 		lang_filter = lang_filter.replace('English', 'en')
	# 	else:
	# 		lang_filter = '*'
	# 	country_filter = ' '.join(q['filters']['country']).upper()
	# 	if len(country_filter) == 0:		
	# 		country_filter = '*'
	# 	POI_filter = ' '.join(q['filters']['poi'])
	# 	if len(POI_filter) == 0:		
	# 		POI_filter = '*'
	# 	verified_filter = q['filters']['verified']
	# 	if len(verified_filter) == 0:		
	# 		verified_filter = '*'

	# 	query = {
	# 		"fl" : "* score",
	# 		"q": "text_en: "+en_t+" text_hi: "+hi_t+" text_es: "+es_t+"",
	# 		"rows": 50,
	# 		"defType": "lucene",
	# 		"wt": "json",
	# 		"fq": "tweet_lang: "+lang_filter+" country: "+country_filter+" poi_name: "+POI_filter+" verified: "+verified_filter+""
	# 	}
	# 	# print(q1)
	# 	result = urlencode(query)
	# 	inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
	# 	data = urllib.request.urlopen(inurl).read()
	# 	docs = json.loads(data.decode('utf-8'))['response']['docs']

	def search1(self, q):
		model_name='BM25-12'
		punc = string.punctuation.replace("#", "")
		query = q['query'].translate(str.maketrans('', '', punc)).split(" ",1)
		hin, esp, eng = "","",""
		for word in query:
			queryText = word.replace("\n","")
			lang = detect(queryText)
			hi_t, es_t, en_t = "","",""
			if lang == "hi":
				hi_t = queryText
				es_t = self.lang_trans("es", queryText)
				en_t = self.lang_trans("en", queryText)
			elif lang == "es":
				es_t = queryText
				hi_t = self.lang_trans("hi", queryText)
				en_t = self.lang_trans("en", queryText)
			else:
				en_t = queryText
				es_t = self.lang_trans("es", queryText)
				hi_t = self.lang_trans("hi", queryText)

			hin = hin + " " + hi_t
			esp = esp + " " + es_t
			eng = eng + " " + en_t	


		if len(q['filters']['verified']) == 0 and len(q['filters']['poi']) and len(q['filters']['country']) == 0 and len(q['filters']['languages']) == 0:
			query = {
			"fl" : "* score",
			"q": "text_en: "+eng.strip()+" text_hi: "+hin.strip()+" text_es: "+esp.strip()+"",
			"rows": 500,
			"defType": "lucene",
			"wt": "json",
			"qf": "text_en^6 text_es^2 text_hi^1.5"
		}
		else:

			f = ""
			# lang_filter = ' '.join(q['filters']['languages'])
			if len(q['filters']['languages']) != 0:		
				for l in q['filters']['languages']:
					l = l.replace('Hindi', 'hi')
					l = l.replace('Spanish', 'es')
					l = l.replace('English', 'en')
					f = f + "tweet_lang: " + l

			# country_filter = ' '.join(q['filters']['country']).upper()
			if len(q['filters']['country']) != 0:
				if len(f) != 0:
					f = f + " AND"
				for c in q['filters']['country']:
					f = f + " country:" + c

			# POI_filter = ' '.join(q['filters']['poi'])
			if len(q['filters']['poi']) != 0:
				if len(f) != 0:
					f = f + " AND"
				for p in q['filters']['poi']:
					f = f + " poi_name:" + p 

			# verified_filter = ' '.join(q['filters']['verified'])
			if len(q['filters']['verified']) != 0:
				if len(f) != 0:
					f = f + " AND"
				for v in q['filters']['verified']:
					f = f + " verified:" + v	

			query = {
				"fl" : "* score",
				"q": "text_en: "+eng.strip()+" text_hi: "+hin.strip()+" text_es: "+esp.strip()+"",
				"rows": 50,
				"defType": "lucene",
				"wt": "json",
				"fq": f
			}

		result = urlencode(query)
		inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
		print(inurl)
		bm25_combine_output = open("bm25_combine_output.txt", 'a+')
		data = urllib.request.urlopen(inurl).read()
		docs = json.loads(data.decode('utf-8'))['response']['docs']

		q_data = dict()
		lang_data = dict()

		q_data['pos_count'] = 0
		q_data['neg_count'] = 0
		q_data['neu_count'] = 0
		q_data['lang_en'] = 0
		q_data['lang_es'] = 0
		q_data['lang_hi'] = 0
		q_data['USA'] = 0
		q_data['INDIA'] = 0
		q_data['MEXICO'] = 0

		for doc in docs:
			sia = SentimentIntensityAnalyzer()
			score = sia.polarity_scores(doc['tweet_text'])
			doc['sentimentScore'] = score
			
			testimonial = TextBlob(doc['tweet_text'])
			
			# set sentiment
			if testimonial.sentiment.polarity > 0:
				doc['sentiment'] = 'positive'
				q_data['pos_count'] += 1	
			elif testimonial.sentiment.polarity == 0:
				doc['sentiment'] = 'neutral'
				q_data['neu_count'] += 1	
			else:
				doc['sentiment'] = 'negative'
				q_data['neg_count'] += 1

			if doc['tweet_lang'] == "en":
				q_data['lang_en'] += 1

			elif doc['tweet_lang'] == "es":
				q_data['lang_es'] += 1
			
			elif doc['tweet_lang'] == "hi":
				q_data['lang_hi'] += 1

			if doc['country'] == "USA":
				q_data['USA'] += 1

			elif doc['country'] == "INDIA":
				q_data['INDIA'] += 1
			
			elif doc['country'] == "MEXICO":
				q_data['MEXICO'] += 1

		if len(docs) != 0:
			q_data['pos_count'] = (q_data['pos_count'] / len(docs)) * 100 
			q_data['neg_count'] = (q_data['neg_count'] / len(docs)) * 100
			q_data['neu_count'] = (q_data['neu_count'] / len(docs)) * 100
			q_data['lang_en'] = (q_data['lang_en'] / len(docs)) * 100
			q_data['lang_es'] = (q_data['lang_es'] / len(docs)) * 100
			q_data['lang_hi'] = (q_data['lang_hi'] / len(docs)) * 100
			q_data['USA'] = (q_data['USA'] / len(docs)) * 100
			q_data['INDIA'] = (q_data['INDIA'] / len(docs)) * 100
			q_data['MEXICO'] = (q_data['MEXICO'] / len(docs)) * 100			
		
		queryresults = dict()
		queryresults['results'] = docs
		queryresults['q_data'] = q_data

		return queryresults

	def search(self):
		count=1
		model_name='BM25-12'


		with open('/home/ubuntu/IR-Project-4/backend/queries.txt', encoding="utf-8") as inputfile:
			bm25_combine_output = open("bm25_combine_output.txt", 'w')
			bm25_combine_output.close()
			for line in inputfile:
				punc = string.punctuation.replace("#", "")
				query = line.translate(str.maketrans('', '', punc)).split(" ",1)
				#query = line.strip('\n').replace(':', '').split(" ", maxsplit=1)
				for word in query:
					queryText = word.replace("\n","")
					lang = detect(queryText)
					hi_t, es_t, en_t = "","",""
					if lang == "hi":
						hi_t = queryText
						es_t = self.lang_trans("es", queryText)
						en_t = self.lang_trans("en", queryText)
					elif lang == "es":
						es_t = queryText
						hi_t = self.lang_trans("hi", queryText)
						en_t = self.lang_trans("en", queryText)
					else:
						en_t = queryText
						es_t = self.lang_trans("es", queryText)
						hi_t = self.lang_trans("hi", queryText)
					
					query = {
						"fl" : "* score",
						"q": "text_en: "+en_t+" text_hi: "+hi_t+" text_es: "+es_t+"",
						"rows": 50,
						"defType": "lucene",
						"wt": "json",
						"qf": "text_en^3 text_es^2 text_ru^1.5"
					}
					result = urlencode(query)
					inurl = f'http://{AWS_IP}:8983/solr/'+ model_name + '/select?'+ result
					#inurl = 'http://18.216.1.251:8983/solr/' + model_name + '/select?'+ result

					outf = open(str(count) + '.txt', 'a+')
					bm25_combine_output = open("bm25_combine_output.txt", 'a+')
					data = urllib.request.urlopen(inurl).read()
					docs = json.loads(data.decode('utf-8'))['response']['docs']
					rank = 1

					for doc in docs:
						outf.write(str(doc)+ '\n')
			
					outf.close()
					count += 1
				
	def lang_trans(self, lang, query):
		trans = GoogleTranslator(source='auto', target=lang).translate(query)
		return trans

if __name__ == '__main__':
	i = Indexer()
	# q = {"query":"covid vaccine","filters":{"languages":["Spanish"],"country":['INDIA'],"poi":["CDCgov"],"verified":["True"]}}
	# i.search1(q)
	app.run(host="0.0.0.0", port=9995, debug=True)