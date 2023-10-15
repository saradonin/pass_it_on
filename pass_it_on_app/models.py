from django.db import models


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

