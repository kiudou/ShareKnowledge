from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.

from books.models import Book, Category
from django.http import HttpResponse


def home(request):
    try:
        Categories = Category.objects.all()
    except Category.DoesNotExist:
        raise Http404
    return render(request, 'home.html', {'Categories': Categories})


def tags(request, book_tag):
    try:
        Books = Book.objects.filter(tag=str(book_tag))
    except Book.DoesNotExist:
        raise Http404
    return render(request, 'index.html', {'Books': Books})


def title(request, book_title):
    try:
        Book_single = Book.objects.get(title=book_title)
    except Book.DoesNotExist:
        raise Http404
    url = '/static/'+Book_single.title
    return redirect(str(url))
