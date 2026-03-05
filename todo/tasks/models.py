from django.db import models
from todo.categories.models import Category


class Task(models.Model):
    """
    Represents a task

    Attributes:
        title (str): The title of the task (non-empty).
        is_completed (bool): Whether the task is completed (default: False).
        category (ForeignKey): The category this task belongs to.
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.
    """

    title = models.CharField(max_length=50)
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
        return self.title[:50] + ('...' if len(self.title) > 50 else '')
