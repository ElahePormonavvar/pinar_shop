from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogPost
# Create your views here.
def create_blog(request):
    return render(request,"blog_app/create_blog.html")

class PostListView(ListView):
    model = BlogPost
    template_name = 'blog_app/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # تعداد مقالات در هر صفحه

    def get_queryset(self):
        return BlogPost.objects.filter(status='publish', is_active=True).order_by('-published_at')
    

class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_app/blog_detail.html'
    context_object_name = 'post'