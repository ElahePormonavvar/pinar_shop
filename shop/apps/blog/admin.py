from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ('article_title','is_active', 'author', 'published_at', 'status',)
    search_fields = ('article_title', 'content')
    prepopulated_fields = {'slug': ('article_title',)}
    list_filter = ('status', 'is_active', 'published_at')