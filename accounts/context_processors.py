def current_user(request):
    """
    A context processor that returns the user object of the currently logged-in user.
    """
    if request.user.is_authenticated:
        return {'current_user': request.user}
    else:
        return {'current_user': None}