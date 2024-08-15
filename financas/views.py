from django.shortcuts import render, redirect
from .models import Transacao
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import TransacaoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth

@login_required
def lista_transacoes(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user  # Atribui a transação ao usuário logado
            transacao.save()
            return redirect('lista_transacoes')
    else:
        form = TransacaoForm()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        transacoes = Transacao.objects.filter(usuario=request.user, data__range=[start_date, end_date])
    else:
        transacoes = Transacao.objects.filter(usuario=request.user)  # Apenas transações do usuário

    receitas = transacoes.filter(tipo='receita')
    despesas = transacoes.filter(tipo='despesa')

    return render(request, 'financas/lista_transacoes.html', {
        'transacoes': transacoes,
        'form': form,
        'receitas': receitas,
        'despesas': despesas
    })

def home(request):
    return render(request, 'financas/home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')  # Redireciona para a página inicial após o login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def insights(request):
    transacoes = Transacao.objects.filter(usuario=request.user)  # Apenas transações do usuário

    # Calcular totais de receitas, despesas e saldo
    total_receitas = transacoes.filter(tipo='receita').aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = transacoes.filter(tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_atual = total_receitas - total_despesas

    # Categorias mais gastas
    categorias_despesas = transacoes.filter(tipo='despesa').values('categoria__nome').annotate(total=Sum('valor')).order_by('-total')

    # Média de gastos mensais
    media_mensal = transacoes.filter(tipo='despesa').annotate(mes=TruncMonth('data')).values('mes').annotate(total=Sum('valor')).aggregate(media=Avg('total'))['media'] or 0

    # Lista de insights
    insights = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo_atual': saldo_atual,
        'categorias_despesas': categorias_despesas,
        'media_mensal': media_mensal,
    }

    return render(request, 'financas/insights.html', insights)
