import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def verify_username(username):

    # Nome de usuário pode conter maíusculas, minúsculas, underlines e pontos
    username_pattern = re.compile(r"[A-Za-z0-9_.]+")

    msg = msg = "O nome de usuário digitado é inválido! Lembre-se que ele só pode conter letras (exceto os acentuados), números, underlines(_) ou pontos(.)!"
        
    return username_pattern.fullmatch(username) != None, msg


def verify_password(password):

    has_uppercase_letter, has_lowercase_letter, has_number = False, False, False

    # Pega os caracteres de acordo com seu valor decimal na tabela unicode
    lowercase_alphapetic = [chr(dec) for dec in range(97, 123)]
    uppercase_alphapetic = [chr(dec) for dec in range(65, 91)]
    numbers = list(map(str, list(range(0, 10))))

    for c in password:

        if c in lowercase_alphapetic:
            has_lowercase_letter = True

        if c in uppercase_alphapetic:
            has_uppercase_letter = True

        if c in numbers:
            has_number = True


    msg = "A senha digitada deve conter pelo menos uma letra minúscula, uma letra maíuscula e um número!"

    return all([has_lowercase_letter, has_uppercase_letter, has_number]), msg


def verify_mail(email):

    mail_pattern = re.compile(r"[a-z0-9]+@[a-z]+.[a-z]+")

    msg = "O e-mail digitado é inválido! Ele deve conter, pelo menos, o arroba (@) e o ponto do subdomínio, e não pode conter caracteres especiais e acentuados (Ex: johndoe12345@gmail.com)!"

    return mail_pattern.fullmatch(email) != None, msg


def verify_name(name, field):

    space_pattern = re.compile(r"\s")
    name_pattern = re.compile(r"[A-Za-záÁóÓÚúéÉÍíêãâõç]+")

    frag_name = space_pattern.split(name)

    for part_name in frag_name:

        if name_pattern.fullmatch(part_name) == None:

            if field == "first-name":

                msg = "O primeiro nome digitado é inválido! Ele pode conter apenas letras e espaços (sem números)!"

            else:

                msg = "O último nome digitado é inválido! Ele pode conter apenas letras e espaços (sem números)!"

            return False, msg

    return True, None


def exist_username(username):

    try:

        # Dispara a exceção DoesNotExist caso não seja encontrado nenhum nome de usuário no banco igual ao passado como
        # parametro
        user = User.objects.get(username=username)

        return True

    except User.DoesNotExist:

        msg = "O e-mail digitado já existe!"

        return False, msg


def exist_mail(email):

    try:

        user = User.objects.get(email=email)

        return True, None

    except User.DoesNotExist:

        msg = "O nome de usuário digitado já existe!"

        return False, msg


def check_passwords(password, confirm_password):

    msg = "As senhas não coincidem!"

    return password == confirm_password, msg


