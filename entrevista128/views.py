from django.shortcuts import render
from .models import Modelo128

# Create your views here.
def modelo_view(request):
	dadosModelo = Modelo128.objects.all()#filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'entrevista128/modelo128_view.html', {'dadosModelo':dadosModelo})

def post_create(request):
	objModelo = Modelo128.objects.create(campo1='', campo2='')
	return render(request, 'entrevista128/modelo128_view.html', {'objModelo' : objModelo})


#Modelo128.objects.all()#todos
#Modelo128.objects.get(campo='valor')#filtro
#Modelo128.objects.filter(campo=valor)#filtro

#salvar
#obj = Modelo128.objects.get(id=1)
#obj.publish()

#ordenando
#Modelo128.objects.order_by('campo')

#ordenando invertido - basta acrescentar sinal de '-'
#Modelo128.objects.order_by('-campo')