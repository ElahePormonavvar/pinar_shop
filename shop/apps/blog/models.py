from django.utils import timezone
from django.db import models
from apps.accounts.models import CustomUser
from django.urls import reverse
from utils import FileUpload

class BlogPost(models.Model):
    article_title = models.CharField(max_length=200,verbose_name='عنوان مقاله')
    content = models.TextField(verbose_name='متن اصلی')
    file_upload=FileUpload('images','blogs')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر کالا')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,verbose_name='کاربر نویسنده')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد مقاله')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='تاریخ بروزر رسانی')
    published_at = models.DateTimeField(blank=True, null=True,default=timezone.now,verbose_name='تاریخ انتشار')
    is_active=models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    slug = models.SlugField(unique=True, max_length=200)
    ARTICLE_STATUS=[
        ('draft','پیش نویس'),
        ('publish','منتشر شده')
    ]
    status=models.CharField(max_length=100,choices=ARTICLE_STATUS,default='draft',verbose_name='وضعیت مقاله')
    

    class Meta:
        verbose_name='مقاله'
        verbose_name_plural='مقالات'
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.article_title}\t{self.created_at}\t{self.author}"

    def get_absolute_url(self):
        return reverse('blogs:blog_detail', args=[self.slug])