from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """
    Represents a category.
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        """
        Return a string representation of the category.
        """
        return self.name


class Institution(models.Model):
    """
    Represents an institution.
    """
    TYPE_CHOICES = {
        (1, "fundacja"),
        (2, "organizacja pozarządowa"),
        (3, "zbiórka lokalna")
    }
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    type = models.CharField(max_length=64, choices=TYPE_CHOICES, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        """
        Return a string representation of the institution.
        """
        return self.name


class Donation(models.Model):
    """
    Represents a donation.
    """
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
