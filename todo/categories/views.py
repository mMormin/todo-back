from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all categories or creating a new one.

    - **GET**: Returns a list of all categories.
    - **POST**: Creates a new Category entry.

    ### Permissions
    `AllowAny` — anyone can view and create categories.

    ### Example
        GET /api/categories/
        POST /api/categories/ with body: {"name": "Work", "icon": "💼"}
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Create a new category with proper validation.

        Returns:
            201: Category created successfully.
            400: Validation error (e.g., duplicate name, empty name).
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific category.

    - **GET**: Returns details of a single category.
    - **PUT/PATCH**: Updates an existing category.
    - **DELETE**: Deletes a category (and all associated tasks due to CASCADE).

    ### Permissions
    `AllowAny` — anyone can manage categories.

    ### Example
        GET /api/categories/1/
        PUT /api/categories/1/ with body: {"name": "Updated Name"}
        DELETE /api/categories/1/
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
