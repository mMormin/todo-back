from rest_framework import serializers
from .models import Task


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
            'title',
            'is_completed',
            'category',
            'category_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """
        Validate that the task title is not empty.

        Args:
            value (str): The task title to validate.

        Returns:
            str: The validated task title.

        Raises:
            serializers.ValidationError: If the title is empty or whitespace only.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("The task title cannot be empty.")
        return value.strip()

    def validate_category(self, value):
        """
        Validate that the category is provided.

        Args:
            value (Category): The category instance to validate.

        Returns:
            Category: The validated category instance.

        Raises:
            serializers.ValidationError: If no category is provided.
        """
        if not value:
            raise serializers.ValidationError("A category is required.")
        return value
