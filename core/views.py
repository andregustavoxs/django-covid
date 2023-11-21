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

                if verify_username(request.POST["username"]):

                    if verify_password(request.POST["password"]):

                        if verify_mail(request.POST["email"]):

                            if verify_name(request.POST["first-name"]):

                                if verify_name(request.POST["last-name"]):

                                    if not exist_username(request.POST["username"]):

                                        if not exist_mail(request.POST["email"]):

                                            if check_passwords(request.POST["password"], request.POST["confirm-password"]):

                                                user = User(username=request.POST["username"],
                                                            password=request.POST["password"],
                                                            email=request.POST["email"],
                                                            first_name=request.POST["first-name"].capitalize(),
                                                            last_name=request.POST["last-name"].capitalize())

                                                user.set_password(request.POST["password"])  # Criptografa a senha
                                                user.is_superuser = 0  # Define que o usuário cadastrado não é um superusuário

                                                user.save()

                                                return redirect(reverse('login'))  # Redireciona para a tela de login

                                            else:

                                                messages.error(request, "As senhas não coincidem!")
                                                return redirect(reverse('cadastro'))

                                        else:

                                            messages.error(request, "O e-mail digitado já existe!")

                                            return redirect(reverse('cadastro'))

                                    else:

                                        messages.error(request, "O nome de usuário digitado já existe!")

                                        return redirect(reverse('cadastro'))

                                else:

                                    messages.error(request, "O último nome digitado é inválido! " +
                                                            "Ele pode conter apenas letras e espaços (sem números)!")

                                    return redirect(reverse('cadastro'))

                            else:
                                messages.error(request, "O primeiro nome digitado é inválido! " +
                                                        "Ele pode conter apenas letras e espaços (sem números)!")
                                return redirect(reverse('cadastro'))

                        else:
                            messages.error(request, "O e-mail digitado é inválido! " +
                                                    "Ele deve conter, pelo menos, o arroba (@) e o ponto do subdomínio, " +
                                                    "e não pode conter caracteres especiais e acentuados" +
                                                    "(Ex: johndoe12345@gmail.com)!")

                            return redirect(reverse('cadastro'))
                    else:
                        messages.error(request, "A senha digitada deve conter pelo menos uma letra minúscula," +
                                                " uma letra maíuscula e um número!")

                        return redirect(reverse('cadastro'))
                else:
                    messages.error(request, "O nome de usuário digitado é inválido! " +
                                            "Lembre-se que ele só pode conter letras (exceto os acentuados), " +
                                            "números, underlines(_) ou pontos(.)!")

                    return redirect(reverse('cadastro'))

        except MultiValueDictKeyError as exc:

            messages.error(request, exc)
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

            messages.error(request, "O nome de usuário digitado não existe! " +
                                    "Você foi redirecionado para a página de cadastro para efetuá-lo!")

            return redirect(reverse('cadastro'))


def index(request):

    return render(request, 'index.html')
