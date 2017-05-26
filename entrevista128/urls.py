from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.modelo_view),
    url(r'novo', views.create),
    url(r'remover', views.remover),
    url(r'editar', views.editar),
    url(r'salvar', views.salvar),
    url(r'pesquisar', views.pesquisar),
    url(r'sobre', views.sobre),
]
