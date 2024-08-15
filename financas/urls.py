from django.urls import path
from . import views


urlpatterns = [
    path('transacoes/', views.lista_transacoes, name='lista_transacoes'),
    path('', views.home,  name= 'home'),
    path('insights/', views.insights, name='insights'),
    # Adicione mais rotas conforme necessário
]