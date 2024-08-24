from django.urls import path
from . import views


app_name="main"
urlpatterns = [
    path('',views.index,name="index"),
    path('sliders/',views.SlideView.as_view(),name="sliders"),
    path('about_us/',views.about_us,name="about_us"),
    path('contact_us/',views.ContactView.as_view(), name='contact_us'),

]     