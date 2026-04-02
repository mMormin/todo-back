import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from todo.categories.models import Category
from todo.tasks.models import Task


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def category(db):
    # Base category reused across all tests
    return Category.objects.create(name="Test Category")


@pytest.fixture
def api_client():
    # Unauthenticated DRF client
    return APIClient()


@pytest.fixture
def list_url():
    # URL for task list and creation
    return reverse("task-list-create")


def detail_url(pk: int) -> str:
    # URL for a single task by primary key
    return reverse("task-detail", kwargs={"pk": pk})


# ---------------------------------------------------------------------------
# Model-level tests
# ---------------------------------------------------------------------------

@pytest.mark.model
@pytest.mark.django_db
def test_new_task_is_not_completed_by_default(category):
    # is_completed must default to False on creation
    task = Task.objects.create(title="Ma tâche", category=category)
    assert task.is_completed is False


@pytest.mark.model
@pytest.mark.django_db
def test_mark_task_as_completed(category):
    # True must be persisted after save() and refresh_from_db()
    task = Task.objects.create(title="Ma tâche", category=category)
    task.is_completed = True
    task.save()
    task.refresh_from_db()
    assert task.is_completed is True


@pytest.mark.model
@pytest.mark.django_db
def test_cannot_create_task_without_title(category):
    # full_clean() must raise ValidationError when title is empty
    task = Task(title="", category=category)
    with pytest.raises(ValidationError):
        task.full_clean()


# ---------------------------------------------------------------------------
# Model-level edge-case tests
# ---------------------------------------------------------------------------

@pytest.mark.model
@pytest.mark.parametrize("title, expected", [
    ("Short title", "Short title"),
    ("A" * 51, "A" * 50 + "..."),
])
def test_str_representation(title, expected):
    # __str__ returns the title as-is (≤50 chars) or truncates with "..." (>50)
    category = Category(name="Edge Cases")
    task = Task(title=title, category=category)
    assert str(task) == expected


@pytest.mark.model
@pytest.mark.django_db
def test_created_at_and_updated_at_are_set_on_save(category):
    # Both timestamps must be populated automatically on creation
    task = Task.objects.create(title="Timestamp test", category=category)
    assert task.created_at is not None
    assert task.updated_at is not None


@pytest.mark.model
@pytest.mark.django_db
def test_cascade_delete_removes_tasks(category):
    # Deleting a category must cascade-delete all its tasks
    Task.objects.create(title="Orphan task", category=category)
    category_pk = category.pk
    category.delete()
    assert not Task.objects.filter(category_id=category_pk).exists()


# ---------------------------------------------------------------------------
# API-level tests
# ---------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.django_db
def test_can_create_task(api_client, category, list_url):
    # Valid POST → 201 with submitted data and is_completed set to False
    payload = {"title": "Write unit tests", "category": category.pk}
    response = api_client.post(list_url, payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Write unit tests"
    assert response.data["category"] == category.pk
    assert response.data["is_completed"] is False


@pytest.mark.api
@pytest.mark.django_db
@pytest.mark.parametrize("method, use_existing_task", [
    ("post", False),
    ("patch", True),
])
def test_empty_title_returns_400(api_client, category, list_url, method, use_existing_task):
    # Empty title via POST (create) or PATCH (update) must return 400 with "title" error
    if use_existing_task:
        task = Task.objects.create(title="Valid title", category=category)
        url = detail_url(task.pk)
    else:
        url = list_url

    payload = {"title": "", "category": category.pk}
    response = getattr(api_client, method)(url, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data


@pytest.mark.api
@pytest.mark.django_db
def test_task_list_returns_all_tasks(api_client, category, list_url):
    # GET on the list endpoint must return all existing tasks
    Task.objects.create(title="First task", category=category)
    Task.objects.create(title="Second task", category=category)

    response = api_client.get(list_url)

    assert response.status_code == status.HTTP_200_OK
    titles = [t["title"] for t in response.data]
    assert "First task" in titles
    assert "Second task" in titles


@pytest.mark.api
@pytest.mark.django_db
def test_can_delete_task(api_client, category):
    # DELETE → 204 and the task must no longer exist in the database
    task = Task.objects.create(title="To be deleted", category=category)
    response = api_client.delete(detail_url(task.pk))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(pk=task.pk).exists()


@pytest.mark.api
@pytest.mark.django_db
def test_can_retrieve_task(api_client, category):
    # GET on an existing task → 200 with the correct data
    task = Task.objects.create(title="Retrieve me", category=category)
    response = api_client.get(detail_url(task.pk))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == task.pk
    assert response.data["title"] == "Retrieve me"


@pytest.mark.api
@pytest.mark.django_db
def test_retrieve_nonexistent_task_returns_404(api_client):
    # GET on a non-existent pk → 404
    response = api_client.get(detail_url(99999))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.api
@pytest.mark.django_db
def test_patch_can_mark_task_as_completed(api_client, category):
    # PATCH is_completed → 200 and the value must be persisted in the database
    task = Task.objects.create(title="Complete me", category=category)
    response = api_client.patch(detail_url(task.pk), {"is_completed": True})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_completed"] is True
    task.refresh_from_db()
    assert task.is_completed is True


@pytest.mark.api
@pytest.mark.django_db
def test_put_can_update_title(api_client, category):
    # PUT with a new title → 200 and the title is updated
    task = Task.objects.create(title="Old title", category=category)
    payload = {"title": "New title", "category": category.pk}
    response = api_client.put(detail_url(task.pk), payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "New title"


@pytest.mark.api
@pytest.mark.django_db
def test_filter_tasks_by_category(api_client, category, list_url):
    # ?category_id=X must return only tasks belonging to that category
    other_category, _ = Category.objects.get_or_create(name="Personal", defaults={"icon": "🏠"})
    Task.objects.create(title="Work task", category=category)
    Task.objects.create(title="Personal task", category=other_category)

    response = api_client.get(list_url, {"category_id": category.pk})

    assert response.status_code == status.HTTP_200_OK
    titles = [t["title"] for t in response.data]
    assert "Work task" in titles
    assert "Personal task" not in titles


@pytest.mark.api
@pytest.mark.django_db
def test_response_includes_category_name(api_client, category):
    # The serializer must expose category_name as a read-only field
    task = Task.objects.create(title="Check fields", category=category)
    response = api_client.get(detail_url(task.pk))

    assert response.status_code == status.HTTP_200_OK
    assert "category_name" in response.data
    assert response.data["category_name"] == category.name


@pytest.mark.api
@pytest.mark.django_db
def test_title_is_stripped_on_create(api_client, category, list_url):
    # Leading/trailing whitespace must be stripped by validate_title
    payload = {"title": "  Padded title  ", "category": category.pk}
    response = api_client.post(list_url, payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Padded title"
