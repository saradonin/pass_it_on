from django.core.validators import RegexValidator
from django.db import models

from accounts.models import User


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
        ("1", "fundacja"),
        ("2", "organizacja pozarządowa"),
        ("3", "zbiórka lokalna")
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

    class Meta:
        verbose_name = "Instytucja"
        verbose_name_plural = "Instytucje"


class Donation(models.Model):
    """
    Represents a donation.
    """
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Numer telefonu musi zawierać od 9 do 15 cyfr.")
    zipcode_regex = RegexValidator(regex=r'^\d{2}-\d{3}$|^\d{5}$',
                                 message="Kod pocztowy musi być podany w formacie 12345 lub 12-345")

    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, validators=[phone_regex])
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6, validators=[zipcode_regex])
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    is_taken = models.BooleanField(default=False)

