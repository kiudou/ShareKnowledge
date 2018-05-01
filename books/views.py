from django.shortcuts import render

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


# def title(request, book_title):
#     try:
#         Book_single = Book.objects.get(title=book_title)
#     except Book_single.DoesNotExist:
#         raise Http404
#     render(request, 'book_show.html', {'Book_single': Book_single})