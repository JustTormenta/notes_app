from django.http import HttpResponse
from .models import Note
from django.shortcuts import render, get_object_or_404, redirect
from .models import Note, Category
from .forms import NoteForm
from django.db.models import Q


def hello_view(request):
    return HttpResponse("Hello from Notes app.")

def index(request):
    notes = [
        {'title': 'Перша нотатка', 'content': 'Прочитати документацію на кроковий двигун NEMA17.'},
        {'title': 'Покупки', 'content': 'Купити (Фарба камуфляжна Deco Color Military RAL 6014).'},
        {'title': 'Ідеї', 'content': 'Розробити конструкцію автоматичної подачі припою.'}
    ]
    return render(request, 'index.html', {'notes': notes})

def note_view(request):
    notes = Note.objects.select_related('category').all()
    return render(request, 'index40.html', {'notes': notes})

def index_hw(request):
    category_id = request.GET.get('category')
    search = request.GET.get('search')
    reminder_filter = request.GET.get('reminder')

    notes = Note.objects.select_related('category')

    if category_id:
        notes = notes.filter(category_id=category_id)
    if search:
        notes = notes.filter(title__icontains=search)
    if reminder_filter == 'upcoming':
        from django.utils import timezone
        notes = notes.filter(reminder__gte=timezone.now())

    categories = Category.objects.all()

    return render(request, 'note_list.html', {
        'notes': notes,
        'categories': categories,
        'selected_category': category_id,
        'search': search,
        'reminder_filter': reminder_filter
    })

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'note_form.html', {'form': form})

def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'note_detail.html', {'note': note})

def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'note_form.html', {'form': form, 'note': note})

def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    return render(request, 'note_confirm_delete.html', {'note': note})