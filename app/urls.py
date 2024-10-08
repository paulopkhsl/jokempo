from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game, name='game'),
    path('ranking/', views.ranking, name='ranking'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]