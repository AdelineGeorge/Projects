import os
import pysolr
import requests
import json
import urllib
from deep_translator import GoogleTranslator
from langdetect import detect
from urllib.parse import urlencode
import string

CORE_NAME = "IR-PROJECT-4"
AWS_IP = "18.117.217.60"


def delete_core(core=CORE_NAME):
    print(os.system('sudo su - solr -c "/opt/solr/bin/solr delete -c {core}"'.format(core=core)))


def create_core(core=CORE_NAME):
    print(os.system(
        'sudo su - solr -c "/opt/solr/bin/solr create -c {core} -n data_driven_schema_configs"'.format(
            core=core)))
    print(os.system(
        'sudo cp -f /home/ubuntu/project3/synonymns.txt /var/solr/data/' +CORE_NAME+'/conf/synonyms.txt'))

class Indexer:
    def __init__(self):
        self.solr_url = f'http://{AWS_IP}:8983/solr/'
        print(self.solr_url)
        self.connection = pysolr.Solr(self.solr_url + CORE_NAME, always_commit=True, timeout=5000000)

    def do_initial_setup(self):
        delete_core()
        create_core()

    def create_documents(self, docs):
        print(self.connection.add(docs))

    def add_fields(self):
        data = {
            "add-field": [


                {
                    "name": "country",
                    "type": "string",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "tweet_lang",
                    "type": "string",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "tweet_text",
                    "type": "string",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "text_en",
                    "type": "text_en",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "text_pt",
                    "type": "text_pt",
                    "indexed": True,
                    "multiValued": False
                },
                
                {
                    "name": "text_hi",
                    "type": "text_hi",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "text_es",
                    "type": "text_es",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "tweet_date",
                    "type": "pdate",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "verified",
                    "type": "boolean",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "poi_id",
                    "type": "plong",
                    "indexed": True,
                    "multiValued": False
                }, {
                    "name": "poi_name", 
                    "type": "string",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "replied_to_tweet_id",
                    "type": "plong",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "replied_to_user_id",
                    "type": "plong",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "reply_text",
                    "type": "text_general",
                    "indexed": True,
                    "multiValued": False
                },
                {
                    "name": "hashtags",
                    "type": "string",
                    "indexed": True,
                    "multiValued": True
                },
                {
                    "name": "mentions",
                    "type": "string",
                    "indexed": True,
                    "multiValued": True
                },
                {
                    "name": "tweet_urls",
                    "type": "string",
                    "indexed": True,
                    "multiValued": True
                },
                {
                    "name": "tweet_emoticons",
                    "type": "string",
                    "indexed": True,
                    "multiValued": True
                },
                {
                    "name": "geolocation",
                    "type": "string",
                    "indexed": True,
                    "multiValued": True
                },
                

            ]
        }

        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())


    def replace_BM25(self, b=None, k1=None):
        data = {
            "replace-field-type": [
                {
                    'name': 'text_en',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'indexAnalyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.StopFilterFactory',
                            'words': 'lang/stopwords_en.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.EnglishPossessiveFilterFactory'
                        }, {
                            'class': 'solr.KeywordMarkerFilterFactory',
                            'protected': 'protwords.txt'
                        }, {
                            'class': 'solr.PorterStemFilterFactory'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                    'queryAnalyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.SynonymGraphFilterFactory',
                            'expand': 'true',
                            'ignoreCase': 'true',
                            'synonyms': 'synonyms.txt'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'words': 'lang/stopwords_en.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.EnglishPossessiveFilterFactory'
                        }, {
                            'class': 'solr.KeywordMarkerFilterFactory',
                            'protected': 'protwords.txt'
                        }, {
                            'class': 'solr.PorterStemFilterFactory'
                        }]
                    }
                }, {
                    'name': 'text_hi',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'analyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'format': 'snowball',
                            'words': 'lang/stopwords_hi.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.SnowballPorterFilterFactory',
                            'language': 'Hindi'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                }, {
                    'name': 'text_es',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'analyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'format': 'snowball',
                            'words': 'lang/stopwords_es.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.SnowballPorterFilterFactory',
                            'language': 'Spanish'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                
                }
            ]
        }
        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())
    def search(self):
        count=1
        model_name='BM25'


        with open('/home/ubuntu/project3/test-queries.txt', encoding="utf-8") as inputfile:
            bm25_combine_output = open("bm25_combine_output.txt", 'w')
            bm25_combine_output.close()
            for line in inputfile:
                punc = string.punctuation.replace("#", "")
                query = line.translate(str.maketrans('', '', punc)).split(" ",1)
                #query = line.strip('\n').replace(':', '').split(" ", maxsplit=1)
                qid = query[0]
                queryText = query[1].replace("\n","")
                lang = detect(queryText)
                ru_t, de_t, en_t = "","",""
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
                    en_t = self.lang_trans("en", queryText)
                
                query = {
                    "fl" : "* score",
                    "q": "text_en: "+en_t+" text_hi: "+hi_t+" text_de: "+es_t+"",
                    "rows": 20,
                    "defType": "edismax",
                    "wt": "json",
                    "qf": "text_en^3 text_de^2 text_ru^1.5"
                }
                result = urlencode(query)
                inurl = 'http://18.216.1.251:8983/solr/' + model_name + '/select?'+ result

                outf = open(str(count) + '.txt', 'a+')
                bm25_combine_output = open("bm25_combine_output.txt", 'a+')
                data = urllib.request.urlopen(inurl).read()
                docs = json.loads(data.decode('utf-8'))['response']['docs']
                rank = 1

                for doc in docs:
                    outf.write(str(qid) + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(
                        doc['score']) + ' ' + "bm25" + '\n')
                    bm25_combine_output.write(str(qid) + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(
                        doc['score']) + ' ' + "bm25" + '\n')
                    rank += 1
                outf.close()
                count += 1

    def lang_trans(self, lang, query):
        trans = GoogleTranslator(source='auto', target=lang).translate(query)
        return trans
        
if __name__ == "__main__":
    i = Indexer()
    i.do_initial_setup()

    i.replace_BM25(b=0.75, k1=1.2)
    i.add_fields()
    path = '/home/ubuntu/my-new-app/data/data/'
    filelist = os.listdir(path)
    for i in filelist:
        car_pickle = open (path + i, "rb")
        print(path + i)
        car_contents = pickle.load(car_pickle)
        data = car_contents.to_json(orient='index')
        i.create_documents(data)
    #with open("/home/ubuntu/my-new-app/data/all_data.json",encoding='utf-8') as json_file:
        #collection = json.load(json_file)
    #i.create_documents(collection)
    #i.search()

    