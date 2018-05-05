from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.

from books.models import Book, Category
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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



def upload(request):
    return render(request, 'upload.html')




@csrf_exempt
def upload_part(request):
    task = request.POST.get('task_id')  # 获取文件的唯一标识符
    chunk = request.POST.get('chunk', 0)  # 获取该分片在所有分片中的序号
    filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.FILES['file']
    destination = open(os.path.join("/Users/qidong/GitHub/Django2.0/ShareKnowledge/books/static/upload", filename),
                       'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in upload_file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    #upload_file.save('/upload/%s' % filename)  # 保存分片到本地
    return render(request, 'upload.html')


def upload_success(request):  # 按序读出分片内容，并写入新文件
    target_filename = request.GET.get('filename')  # 获取上传文件的文件名
    task = request.GET.get('task_id')  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open('/Users/qidong/GitHub/Django2.0/ShareKnowledge/books/static/upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = '/Users/qidong/GitHub/Django2.0/ShareKnowledge/books/static/upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    return render(request, 'upload.html')



# @csrf_exempt
# def upload_file(request):  # 不用webupload上传文件
#     if request.method == "POST":    # 请求方法为POST时，进行处理
#         myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
#         if not myFile:
#             return HttpResponse("no files for upload!")
#         destination = open(os.path.join("/Users/qidong/GitHub/Django2.0/ShareKnowledge/books/static/upload", myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
#         for chunk in myFile.chunks():      # 分块写入文件
#             destination.write(chunk)
#         destination.close()
#         return HttpResponse("upload over!")