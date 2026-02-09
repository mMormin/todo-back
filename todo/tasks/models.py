from django.db import models
from todo.categories.models import Category


class Task(models.Model):
    """
    Represents a task 

    Attributes:
        description (str): The description of the task (non-empty).
        is_completed (bool): Whether the task is completed (default: False).
        category (ForeignKey): The category this task belongs to.
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.
    """

    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.description[:50] + ('...' if len(self.description) > 50 else '')
