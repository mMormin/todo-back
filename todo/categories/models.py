from django.db import models


class Category(models.Model):
    """
    Represents a category for grouping tasks.

    Attributes:
        name (str): The name of the category (unique, non-empty).
        icon (str): An emoji character used as the category icon.
        created_at (datetime): Timestamp when the category was created.
        updated_at (datetime): Timestamp when the category was last updated.
    """

    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=10, default='📁')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
