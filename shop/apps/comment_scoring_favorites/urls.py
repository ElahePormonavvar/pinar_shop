from django.urls import path
from . import views

app_name='csf'

urlpatterns = [
    path('create_comment/<slug:slug>/',views.CommentView.as_view(),name='create_comment'),  
    path('add_score/',views.add_score,name='add_score'),
    # path('update_avg_score/',views.update_avg_score,name='update_avg_score'),  

    path('show_favorite_list/',views.show_favorite_list,name='show_favorite_list'),
    path('add_to_favorite/',views.add_to_favorite,name='add_to_favorite'),
    path('user_favorite_list/',views.UserFavoriteView.as_view(),name='user_favorite_list'),
    path('update_favorite_count/',views.update_favorite_count,name='update_favorite_count'),    
    path('remove_from_favorite/',views.remove_from_favorite,name='remove_from_favorite'),  
    
]