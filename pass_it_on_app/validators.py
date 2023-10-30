import re

from pass_it_on_app.models import User


def validate_password(password, password2):
    """
    Validates password
    """
    errors = {}

    if not password:
        errors["password_msg"] = "Podaj hasło"
    elif len(password) < 8:
        errors["password_msg"] = "Hasło musi zawierać minimum 8 znaków"
    elif password.lower() == password:
        errors["password_msg"] = "Hasło musi zawierać wielką literę"
    elif password.upper() == password:
        errors["password_msg"] = "Hasło musi zawierać małą literę"
    elif not re.search(r'\d', password):
        errors["password_msg"] = "Hasło musi zawierać cyfrę"
    elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors["password_msg"] = "Hasło musi zawierać znak specjalny"

    if not password2 or password != password2:
        errors["password2_msg"] = "Hasła muszą być takie same"

    return errors


def validate_user_data(name, surname, email):
    """
    Validates user data
    """
    errors = {}

    if not name:
        errors["name_msg"] = "Podaj imię"
    if not surname:
        errors["surname_msg"] = "Podaj nazwisko"
    if not email:
        errors["email_msg"] = "Podaj email"

    return errors


def validate_email_unique(email):
    errors = {}
    if User.objects.filter(email=email):
        errors["email_msg"] = "Podany adres email jest zajety"

    return errors
