import re

from donations.models import User


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
    """
    Validates email availability
    """
    errors = {}
    if User.objects.filter(email=email):
        errors["email_msg"] = "Podany adres email jest zajety"

    return errors


def validate_last_admin(request, user):
    """
    Validates if user is the last superuser
    """
    errors = {}
    current_user = request.user
    admin_count = User.objects.filter(is_staff=True).count()

    if user.is_staff and admin_count == 1:
        errors["message"] = "Usunięcie ostatniego administratora jest niemożliwe."

    if user == current_user:
        errors["message"] = "Usunięcie samego siebie jest niemożliwe."

    return errors
