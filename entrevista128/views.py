from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint
from django.contrib import messages
import urllib.request

import json
from django.http import JsonResponse

#import jsonpickle
from django.core import serializers

from .models import Modelo128

# Create your views here.
def modelo_view(request):

	dadosModelo = Modelo128.objects.all()
	dadosPaginacao = paginacao(request,dadosModelo)
	return render(request, 'entrevista128/modelo128_view.html', {'paginacao':dadosPaginacao})


def paginacao(request,dadosModelo):
    
    paginator = Paginator(dadosModelo, 10)# Show 100 registros per page
    page = 1

    if request.GET.get('page'):
    	page = request.GET.get('page')
    
    try:
        contacts = paginator.page(page)        
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return contacts

#salvar update
def salvar(request):
	if request.POST:
		
		objModelo = Modelo128.objects.get(campo1=request.POST.get('id'))
		objModelo.campo2 = request.POST.get('campo2')
		objModelo.save()
		messages.add_message(request, messages.SUCCESS,"Registro alterado com sucesso!")

	dadosModelo = Modelo128.objects.all()
	dadosPaginacao = paginacao(request,dadosModelo)
	return render(request, 'entrevista128/modelo128_view.html', {'dadosModelo':dadosModelo,'paginacao':dadosPaginacao})


def create(request):

	try:
		#gera o numero aleatorio
		random = gera_numero_aleatorio()#randint(1,100000)
		#pega o texto atraves da api
		texto_api = get_dados_api()
		
		Modelo128.objects.create(campo1=random, campo2=texto_api)
		
		messages.add_message(request, messages.SUCCESS,"Novo registro criado com sucesso!")	

	except Exception as e:
		messages.add_message(request, messages.DANGER,"Não foi possível adicionar novo registro!")
	
	dadosModelo = Modelo128.objects.all()
	dadosPaginacao = paginacao(request,dadosModelo)

	return render(request, 'entrevista128/modelo128_view.html', {'dadosModelo':dadosModelo,'paginacao':dadosPaginacao})	

def remover(request):
	
	try:
		codigo = request.GET.get('id')
		#a = Modelo128.objects.exclude(campo1=codigo)
		objModelo = Modelo128.objects.filter(campo1=codigo).delete()
		#objModelo.delete()
		messages.add_message(request, messages.SUCCESS,"Registro removido com sucesso!")
	except Exception as e:
		messages.add_message(request, messages.DANGER,"Não foi possivel remover o registro!")
		
	dadosModelo = Modelo128.objects.all()
	dadosPaginacao = paginacao(request,dadosModelo)
	return render(request, 'entrevista128/modelo128_view.html', {'dadosModelo':dadosModelo,'paginacao':dadosPaginacao,'codigo':codigo})	
	
def editar(request):
	codigo = request.GET.get('id')
	edit = Modelo128.objects.get(campo1=codigo)
	return render(request, 'entrevista128/editar_view.html', {'editar':edit,'codigo':codigo})

# gera numero aleatorio e verifica se o mesmo ja esta cadastrado evitando duplicidade
def gera_numero_aleatorio():
	#gera o numero aleatorio
	random = randint(1,100000)
	#verifica se o numero ja encontra-se cadastrado
	objModelo = Modelo128.objects.filter(campo1=random)

	if objModelo:
		gera_numero_aleatorio()
	else:
		return random
	

def get_dados_api():
	
	url = "https://api.randomuser.me/"

	request_api = urllib.request.urlopen(url)
	response_api = request_api.read()

	return response_api

# acessada via ajax
def pesquisar(request):

	campo_pesquisa = request.GET.get('pesquisa')
	
	if campo_pesquisa:
		#objModelo = Modelo128.objects.filter(campo1=campo_pesquisa)
		parametros = " campo1 LIKE '%{0}%' or campo2 LIKE '%{1}%' ".format(campo_pesquisa,campo_pesquisa);
		objModelo = Modelo128.objects.extra(where=[parametros])
		#objModelo = Modelo128.objects.extra(where=["campo1 LIKE '%\%s%' or campo2 LIKE '%\%s%' "campo_pesquisa,campo_pesquisa])
	else: 
		objModelo = Modelo128.objects.all()

	if objModelo:
		dados = {'qtdRegistros':objModelo.count(),'success':True,'objModelo':serializers.serialize("json", objModelo),'error':False}

		return JsonResponse(dados)

	else:
		dados = {'success':False,'error':'Nenhum registro encontrado!'}
		return JsonResponse(dados)

def sobre(request):
	return render(request, 'entrevista128/sobre_view.html', {})	

#Modelo128.objects.all()#todos
#Modelo128.objects.get(campo='valor')#filtro filtra somente um registro
#Modelo128.objects.filter(campo=valor)#filtro filtra varios

#salvar
#obj = Modelo128.objects.get(id=1)
#obj.publish()

#ordenando
#Modelo128.objects.order_by('campo')

#ordenando invertido - basta acrescentar sinal de '-'
#Modelo128.objects.order_by('-campo')