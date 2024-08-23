from django.urls import path
from . import views


app_name="blogs"
urlpatterns = [
    path('createblog/',views.create_blog,name='createblog'),
    path('blog_list/', views.PostListView.as_view(), name='blog_list'),
    path('blog_detail/<slug:slug>/', views.PostDetailView.as_view(), name='blog_detail'),

]