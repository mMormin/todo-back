from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all tasks or creating a new one.

    - **GET**: Returns a list of all tasks.
        Supports optional filtering by category.
    - **POST**: Creates a new Task entry.

    ### Query Parameters
    - `category_id` (int, optional): Filters tasks by category ID.
      Example: `?category_id=1`

    ### Permissions
    `AllowAny` — anyone can view and create tasks.

    ### Example
        GET /api/tasks/
        GET /api/tasks/?category_id=1
        POST /api/tasks/ with body: {"description": "Task", "category": 1}
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Optionally filter tasks by category_id query parameter.

        Returns:
            QuerySet: Filtered or complete list of tasks.
        """
        queryset = super().get_queryset()
        
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new task with proper validation.

        Returns:
            201: Task created successfully.
            400: Validation error (e.g., empty description, invalid category).
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


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a single Task.

    - **GET**: Returns a single Task by its ID.
    - **PATCH**: Partially updates the specified Task (e.g., is_completed).
    - **PUT**: Fully updates the specified Task.
    - **DELETE**: Removes the Task from the database.

    ### Permissions
    `AllowAny` — anyone can view, edit, or delete tasks.

    ### Example
        GET /api/tasks/1/
        PATCH /api/tasks/1/ with body: {"is_completed": true}
        DELETE /api/tasks/1/
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        """
        Update a task with proper validation.

        Returns:
            200: Task updated successfully.
            400: Validation error.
            404: Task not found.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a task.

        Returns:
            204: Task deleted successfully.
            404: Task not found.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
