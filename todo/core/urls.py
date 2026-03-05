from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok", "message": "API is healthy"})


def trigger_error(request):
    division_by_zero = 1 / 0
    return JsonResponse({"this": "will never be returned"})


urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('sentry-debug/', trigger_error, name='trigger_error'),
    path('admin/', admin.site.urls),
    path('api/', include('todo.categories.urls')),
    path('api/', include('todo.tasks.urls')),
]
