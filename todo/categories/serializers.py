from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Handles the conversion between Category instances and their JSON
    representations.
    Validates that the category name is unique and non-empty.
    """

    class Meta:
        """
        Meta configuration for CategorySerializer.

        Attributes:
            model (Category): The model being serialized.
            fields (list): Fields to include in the serialized output.
            read_only_fields (list): Fields that cannot be modified through the API.
        """
        model = Category
        fields = ['id', 'name', 'icon', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        """
        Validate that the category name is not empty.

        Args:
            value (str): The category name to validate.

        Returns:
            str: The validated category name.

        Raises:
            serializers.ValidationError: If the name is empty or whitespace only.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("The category name cannot be empty.")
        return value.strip()
