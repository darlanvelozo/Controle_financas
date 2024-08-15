from django.contrib import admin
from .models import Categoria, Transacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'categoria', 'valor', 'descricao', 'data')
    list_filter = ('tipo', 'categoria', 'data')
    search_fields = ('descricao', 'valor')