import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Game, Ranking
from .forms import SignUpForm, LoginForm

def index(request):
    return render(request, 'app/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('game')
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

@login_required
def game(request):
    player_score = 0
    computer_score = 0
    player_choice = None
    computer_choice = None
    result = None

    if request.method == 'POST':
        player_choice = request.POST['choice']
        computer_choice = random.choice(['pedra', 'papel', 'tesoura'])
        result = determine_winner(player_choice, computer_choice)
        
        # Salva o jogo no banco de dados
        Game.objects.create(player=request.user, player_choice=player_choice, computer_choice=computer_choice, result=result)
        
        # Atualiza o ranking do jogador
        update_ranking(request.user, result)
        
        # Calcula os placares
        player_score = Game.objects.filter(player=request.user, result='vitoria').count()
        computer_score = Game.objects.filter(player=request.user, result='derrota').count()

    context = {
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'result': result,
        'player_score': player_score,
        'computer_score': computer_score,
    }
    
    return render(request, 'app/game.html', context)

@login_required
def ranking(request):
    rankings = Ranking.objects.all()[:10]
    return render(request, 'app/ranking.html', {'rankings': rankings})

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return 'empate'
    elif (player_choice == 'pedra' and computer_choice == 'tesoura') or \
         (player_choice == 'papel' and computer_choice == 'pedra') or \
         (player_choice == 'tesoura' and computer_choice == 'papel'):
        return 'vitoria'
    else:
        return 'derrota'

def update_ranking(player, result):
    ranking, created = Ranking.objects.get_or_create(player=player)
    if result == 'vitoria':
        ranking.score += 1
    elif result == 'derrota':
        ranking.score -= 1
    ranking.save()

def logout_view(request):
    logout(request)
    return redirect('index')