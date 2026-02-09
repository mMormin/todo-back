from rest_framework import serializers
from .models import Task
from todo.categories.models import Category


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Manages the relationship with Category through a ForeignKey.
    """

    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        """
        Meta configuration for TaskSerializer.

        Attributes:
            model (Task): The model being serialized.
            fields (list): Fields to include in the serialized output.
            read_only_fields (list): Fields that cannot be modified through the API.
        """
        model = Task
        fields = [
            'id',
            'description',
            'is_completed',
            'category',
            'category_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_description(self, value):
        """
        Validate that the task description is not empty.

        Args:
            value (str): The task description to validate.

        Returns:
            str: The validated task description.

        Raises:
            serializers.ValidationError: If the description is empty or whitespace only.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("La description de la tâche ne peut pas être vide.")
        return value.strip()

    def validate_category(self, value):
        """
        Validate that the category exists.

        Args:
            value (Category): The category instance to validate.

        Returns:
            Category: The validated category instance.

        Raises:
            serializers.ValidationError: If the category does not exist.
        """
        if not value:
            raise serializers.ValidationError("La catégorie est obligatoire.")
        
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("La catégorie spécifiée n'existe pas.")
        
        return value
