import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def verify_username(username):

    # Nome de usuário pode conter maíusculas, minúsculas, underlines e pontos
    username_pattern = re.compile(r"[A-Za-z0-9_.]+")

    if username_pattern.fullmatch(username) != None:
        return True
    else:
        return False


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

    if [has_lowercase_letter, has_uppercase_letter, has_number] == [True, True, True]:
        return True
    else:
        return False


def verify_mail(email):

    mail_pattern = re.compile(r"[a-z0-9]+@[a-z]+.[a-z]+")

    if mail_pattern.fullmatch(email.lower()) != None:
        return True
    else:
        return False


def verify_name(name):

    space_pattern = re.compile(r"\s")
    name_pattern = re.compile(r"[A-Za-záÁóÓÚúéÉÍíêãâõç]+")

    frag_name = space_pattern.split(name)

    for part_name in frag_name:

        if name_pattern.fullmatch(part_name) == None:

            return False

    return True


def exist_username(username):

    try:

        # Dispara a exceção DoesNotExist caso não seja encontrado nenhum nome de usuário no banco igual ao passado como
        # parametro
        user = User.objects.get(username=username)

        return True

    except User.DoesNotExist:

        return False


def exist_mail(email):

    try:

        user = User.objects.get(email=email)

        return True

    except User.DoesNotExist:

        return False


def check_passwords(password, confirm_password):

    if password == confirm_password:

        return True

    else:

        return False



