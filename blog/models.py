import uuid, os

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='分类名称')
	
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name



def article_img_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}{}'.format(uuid.uuid4().hex[:8],ext)
    # return '{0}/{1}/{2}'.format(instance.user.id,"acatar",filename)
    return os.path.join("article",filename)

class Article(models.Model):
    
    title = models.CharField(verbose_name='文章标题', max_length=50)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    img = models.ImageField(upload_to=article_img_path, null=True, blank=True, verbose_name='文章配图')
    content = models.TextField(verbose_name='文章内容')
    abstract = models.TextField(verbose_name='文章摘要', null=True, blank=True)
    visited = models.PositiveIntegerField(verbose_name='访问量', default=0)
    category = models.ManyToManyField('Category', verbose_name='文章分类')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    updated_time = models.DateTimeField('修改时间',auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
        verbose_name = '文章内容'
        verbose_name_plural = verbose_name

    # 可以通过调用这个函数，直接返回详情页的url地址
    def get_absolute_url(self):
        link = "http://127.0.0.1:8000"
        return link + reverse("blog:blog_detail", kwargs={'a_id':self.id})

    # 访问量+1
    def increase_visited(self):
        self.visited += 1
        self.save(update_fields=['visited'])




