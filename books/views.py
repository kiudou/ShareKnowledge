from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.

from books.models import Book, Category
import os, shutil
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

base_url = '/Users/qidong/GitHub/Django2.0/ShareKnowledge/books/static/'
base_url_upload = base_url + 'upload/'

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

#提交表单
def submit_form(request):
    if 'book_name' in request.GET and 'people_name' in request.GET \
            and 'people_mail' in request.GET and 'book_tag' in request.GET:
        bn = request.GET['book_name']
        bt = request.GET['book_tag']
        pn = request.GET['people_name']
        pm = request.GET['people_mail']
        book_single = Book.objects.filter(title=bn)
        if book_single:
            return render(request, 'book_exist.html')
        old_file = base_url+'/upload/'+bn
        new_file = base_url+bt+'/'
        print(old_file, new_file)
        try:
            shutil.move(old_file, new_file)
            Book.objects.create(title=bn, tag=bt, uploader=pn, uploader_mail=pm)
        except BaseException:
            return render(request, 'faile.html')
        # if not Book.objects.get_or_create(title=bn, tag=bt, uploader=pn, uploader_mail=pm):
        #     return render(request, 'book_exist.html')
        #os.remove([x for x in os.listdir(base_url_upload) if os.path.isfile(x)])
        shutil.rmtree(base_url_upload)  # 移动文件
        os.mkdir(base_url_upload)  #删除目录下的所有文件
        return render(request, 'success.html')
    else:
        return render(request, 'faile.html')

# 上传书籍
def upload(request):
    return render(request, 'upload.html')

# 项目简介
def about_me(request):
    return render(request, 'about_me.html')


@csrf_exempt
def upload_part(request):  # 分片上传
    task = request.POST.get('task_id')  # 获取文件的唯一标识符
    chunk = request.POST.get('chunk', 0)  # 获取该分片在所有分片中的序号
    filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.FILES['file']
    destination = open(os.path.join(base_url_upload, filename),
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
    with open(base_url_upload +'%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = base_url_upload + '%s%d' % (task, chunk)
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