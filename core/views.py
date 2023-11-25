from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.cache import never_cache
from core.validations import *


@never_cache
def cadastrar(request):

    sludge_user = "none"

    if request.method == "POST":

        try:

            # Verifica se todos os campos não estão em branco
            if not all(request.POST[key] for key in ["username", "password", "confirm-password", "email", "first-name", "last-name"]):

                messages.error(request, "Todos os campos são obrigatórios. Por favor, preencha todos os campos.")
                return redirect(reverse('cadastro'))

            else:

                sludge_user = (request.POST["username"].replace("_", "-", len(request.POST["username"]))
                               .replace(".", "-", len(request.POST["username"])))
                # Substitui (Até o tamanho do nome de usuário vezes)
                # pontos ou underlines por hifens o nome de usuário passado (Caso tenha algum desses caracteres)

                validations = [
	                lambda x: verify_username(x['username']),
	                lambda x: verify_name(x['first-name'], "first-name"),
	                lambda x: verify_name(x['last-name'], "last-name"),
	                lambda x: verify_mail(x['email'].lower()),
	                lambda x: verify_password(x['password']),
	                lambda x: check_passwords(x['password'], x['confirm-password']),
                    lambda x: not_exist_username(x['username']),
                    lambda x: not_exist_mail(x['email'])
                ]

                for validation in validations:

                    result, message = validation(request.POST)
                    
                    # Mostra as mensagens apenas se o valor de result for False
                    # A mensagem de erro (message) também é pega se result for True (Menos em verify_name, exist_username e exist_mail)
                    if not result:

                        messages.error(request, message)

                        return redirect(reverse('cadastro'))     

                user = User(username=request.POST["username"],
                            password=request.POST["password"],
                            email=request.POST["email"].lower(),
                            first_name=request.POST["first-name"].capitalize(),
                            last_name=request.POST["last-name"].capitalize())

                user.set_password(request.POST["password"])  # Criptografa a senha
                user.is_superuser = 0  # Define que o usuário cadastrado não é um superusuário

                user.save()

                return redirect(reverse('login'))  # Redireciona para a tela de login

        except MultiValueDictKeyError as exc:

            messages.error(request, exc)
            return redirect(reverse('cadastro'))
        
        except Exception as exc:

            messages.error(request, "Houve um erro inesperado!")

            # Para o desenvolvedor
            print(exc)

            return redirect(reverse('cadastro'))

    else:
        print(f"Método da requisição: {request.method}")
        pass

@never_cache
def login(request):

    return render(request, "login.html")


def cadastro(request):

    return render(request, "cadastro.html")


def dashboard(request):

    if request.method == "POST":

        try:

            """
            Dispara a exceção DoesNotExist caso o usuário com esse nome de usuário não seja encontrado
            
            Devido ao valor atributo unique ser True em username (Que é uma instância de CharField), não é permitido
            que tenha duas instâncias de auth.user no banco com o mesmo username
            """

            usuario = User.objects.get(username=request.POST["username"])

            # Checa se a senha do usuário com o nome de usuário estabelecido corresponde ao que foi digitado
            if usuario.check_password(request.POST["password"]):

                return render(request, "dashboard.html", context={"username": usuario.first_name})

            else:

                messages.error(request, "A senha digitada não consta com a do usuário cadastrado!")
                return redirect(reverse('login'))

        except User.DoesNotExist:

            messages.error(request, "O nome de usuário digitado não existe! Você foi redirecionado para a página de cadastro para efetuá-lo!")

            return redirect(reverse('cadastro'))


def index(request):

    return render(request, 'index.html')
