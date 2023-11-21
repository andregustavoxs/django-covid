from django.urls import path
from core.views import *

urlpatterns = [
    path('cadastro/', cadastro, name="cadastro"),
    path('cadastro/{sludge_user}', cadastrar, name="cadastrar"),
    path('login/', login, name="login"),
    path('', index),
    path('dashboard/', dashboard, name="dashboard"),
]