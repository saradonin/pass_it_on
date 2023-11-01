from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Token(models.Model):
    """
    Represents a token used for registration.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True)