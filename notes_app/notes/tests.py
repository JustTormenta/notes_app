import pytest
import factory
from django.urls import reverse
from django.forms.models import model_to_dict
from django.utils import timezone

from .models import Note, Category

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(lambda n: f'Category {n}')

class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    title = factory.Faker('sentence')
    text = factory.Faker('text', max_nb_chars=200)
    reminder = factory.LazyFunction(timezone.now)
    category = factory.SubFactory(CategoryFactory)

@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def note(category):
    return NoteFactory(category=category)

@pytest.mark.django_db
def test_note_creation(note):
    assert note.id is not None
    assert isinstance(note, Note)

@pytest.mark.django_db
def test_note_detail_view(client, note):
    url = reverse('note_detail', args=[note.pk])
    response = client.get(url)

    assert response.status_code == 200
    assert note.title.encode() in response.content


@pytest.mark.django_db
def test_note_create_view(client, category):
    url = reverse('create_note')
    data = {
        "title": "Test Note",
        "text": "This is a test note.",
        "reminder_time": timezone.now().isoformat(timespec='minutes'),
        "category": category.id,
    }

    response = client.post(url, data=data)
    assert response.status_code == 302
    assert Note.objects.filter(title="Test Note").exists()


@pytest.mark.django_db
def test_note_edit_view(client, note, category):
    url = reverse('edit_note', args=[note.id])
    data = model_to_dict(note)
    data['title'] = "Updated Note Title"
    data['category'] = category.id

    response = client.post(url, data)
    assert response.status_code == 302

    note.refresh_from_db()
    assert note.title == "Updated Note Title"


@pytest.mark.django_db
def test_note_delete_view(client, note):
    url = reverse('delete_note', args=[note.id])
    response = client.post(url)

    assert response.status_code == 302
    assert not Note.objects.filter(id=note.id).exists()