import re


def validate_password(password, password2):
    errors = {}

    if not password:
        errors["password_msg"] = "Podaj hasło"
    elif len(password) < 8:
        errors["password_msg"] = "Hasło musi zawierać co najmniej 8 znaków"
    elif password.lower() == password:
        errors["password_msg"] = "Hasło musi zawierać co najmniej jedną wielką literę"
    elif password.upper() == password:
        errors["password_msg"] = "Hasło musi zawierać co najmniej małą małą literę"
    elif not re.search(r'\d', password):
        errors["password_msg"] = "Hasło musi zawierać co najmniej jedną cyfrę"
    elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors["password_msg"] = "Hasło musi zawierać co najmniej jeden znak specjalny"

    if not password2 or password != password2:
        errors["password2_msg"] = "Hasła muszą być takie same"

    return errors


def validate_user_data(name, surname, email):
    errors = {}

    if not name:
        errors["name_msg"] = "Podaj imię"
    if not surname:
        errors["surname_msg"] = "Podaj nazwisko"
    if not email:
        errors["email_msg"] = "Podaj email"

    return errors
