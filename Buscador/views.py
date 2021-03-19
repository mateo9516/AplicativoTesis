# Librerias del django
import requests
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from random import randint
from django.views import generic
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView

# Librerias importadas para la consulta d

import sys
import os
import csv
import re
import json
import nltk
import numpy as np
from gensim.models import Word2Vec
from gensim.models import FastText
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tokenize import sent_tokenize
import nltk.data
from nltk.corpus import stopwords
import tempfile
from gensim.similarities.index import AnnoyIndexer
from sklearn.decomposition import IncrementalPCA    # inital reduction
from sklearn.manifold import TSNE                   # final reduction
import numpy as np
from gensim.models import KeyedVectors
import matplotlib.pyplot as plt
import random
import plotly.offline as py
import plotly.graph_objs as go
from IPython import get_ipython

# Create your views here.

class index(TemplateView):    
    template_name = 'buscador.html'
    def post(self, request, *args, **kwargs):
        buscar = request.POST['busqueda']
        modelo = request.POST['modeloE']
        print(modelo)
        retornoBusqueda,retornoPalabrasC = LiteralTG(str(buscar),str(modelo))
        Urls = []
        direccion = ""
       
        for i in range(len(retornoBusqueda)):
            direccion = f'../static/Resoluciones/{retornoBusqueda[i]}'
            Urls.append(direccion)
        
        comprimir = zip(retornoBusqueda, Urls, retornoPalabrasC)

        if(retornoBusqueda == "Vacio"):
            return render(request, "buscador.html")
        else:
            #actualizarApi(retornoBusqueda)
            return render(request, "resultado.html", {'resoluciones' : comprimir })

def LiteralTG(consultar,modelo):
    if(modelo == "word2vec255.model"):
        model = Word2Vec.load(f'static/RedNeu/{modelo}')
    elif(modelo == "W2VSkipGram16.model"):
        model = Word2Vec.load(f'static/RedNeu/{modelo}')
    elif(modelo == "word2vecCbow255.model"):
        model = Word2Vec.load(f'static/RedNeu/{modelo}')
    
    consulta = consultar.lower()
    entrada = []
    consulta = consulta.split()
    noExiste = "Vacio"

    for x in consulta:
        if x in model.wv.vocab:
            entrada.append(x)
    try:
        top = model.wv.most_similar(entrada,topn=30)

        lista_terminos = []
        lista_valores = []

        for palabra, valor in top:
            lista_terminos.append(palabra)
            lista_valores.append(valor)

        matriz = []
        with open('static/RedNeu/Categorias.txt', 'rt',encoding='utf-8') as f:
            lineas = f.readlines()
            for linea in lineas:
                linea = linea.split('*')
                matriz.append(linea)

        aux=[]
        resoluciones = []
        valores =[]
        
        for i in range(len(lista_terminos)):
            for a,b in matriz:
                aux=re.split(' |,',b)
                if lista_terminos[i] in aux:
                    elemento = matriz.index([a,b])
                    resoluciones.append(elemento)
                    valores.append(lista_valores[i])
        
        """      
        for a,b in matriz:
            aux=re.split(' |,',b)
            for i in range(len(lista_terminos)):
                if lista_terminos[i] in aux:
                    elemento = matriz.index([a,b])
                    if elemento not in resoluciones:
                        resoluciones.append(elemento)
                        valores.append(lista_valores[i])
        """
        listaarreglada = list(dict.fromkeys(resoluciones))
        ListadoResu = []
        ListadoPalabrasClave = []
        pdf = ""
        clavesP = ""

        for i in range(len(listaarreglada)):
            if( valores[i] > 0.79):
                pdf = matriz[listaarreglada[i]][0].replace("txt","pdf")
                ListadoResu.append(pdf)
                clavesP = matriz[listaarreglada[i]][1]
                ListadoPalabrasClave.append(clavesP)

    except:
        return noExiste,noExiste
    return ListadoResu,ListadoPalabrasClave


def actualizarApi(Listado):
    respuesta = requests.get('https://apitesisjson.herokuapp.com/votos')

    jsonactualizar = respuesta.json()

    for i in range(len(Listado)):
        for item in jsonactualizar:
            if(Listado[i] == item["resolucion"]):
                item["VecesSalido"] = int(item["VecesSalido"]) + 1 
                direccion = 'https://apitesisjson.herokuapp.com/votos/'+str(item["id"])
                requests.put(direccion, data= item)
                break