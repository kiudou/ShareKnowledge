from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=120)  # 书名字
    tag = models.CharField(max_length=120) # 标签
    uploader = models.CharField(max_length=120)  # 上传者
    uploader_mail = models.CharField(max_length=60)  # 给上传者发感谢信

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name