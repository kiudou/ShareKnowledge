from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.

from books.models import Book, Category
from django.http import HttpResponse

#主页
def home(request):
    try:
        Categories = Category.objects.all()
    except Category.DoesNotExist:
        raise Http404
    return render(request, 'home.html', {'Categories': Categories})

#该类标签下的书籍展示
def tags(request, book_tag):
    try:
        Books = Book.objects.filter(tag=str(book_tag))
    except Book.DoesNotExist:
        raise Http404
    return render(request, 'index.html', {'Books': Books})

#书籍的展示
def title(request, book_title):
    try:
        Book_single = Book.objects.get(title=book_title)
    except Book.DoesNotExist:
        raise Http404
    url = '/static/'+Book_single.tag+'/'+Book_single.title
    return redirect(str(url))

#根据书名搜索
def search_title(request):
    if 'input_title' in request.GET:
        title = request.GET['input_title']
        if not title:
            return redirect('/')
        else:
            Books = Book.objects.filter(title__icontains=title)
            return render(request, 'index.html', {'Books': Books})
    else:
        return redirect('/')

#根据标签搜索
def search_tag(request):
    if 'input_tag' in request.GET:
        tag = request.GET['input_tag']
        if not tag:
            return redirect('/')
        else:
            Categories = Category.objects.filter(name__icontains=tag)
            print(Categories)
            return render(request, 'show_tags.html', {'Categories': Categories})
    else:
        return redirect('/')
