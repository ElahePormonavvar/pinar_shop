from django.urls import path
from . import views


app_name="accounts"
urlpatterns = [
    path('register/',views.RegisterUserView.as_view(),name='register'),
    path('verify/',views.VerifyRegisterCodeView.as_view(),name='verify'),
    path('login/',views.LoginUserView.as_view(),name='login'),
    path('logout/',views.LogoutUserView.as_view(),name='logout'),
    path('changepassword/',views.ChangePasswordView.as_view(),name='changepassword'),
    path('rememberpassword/',views.RememberPasswordView.as_view(),name='rememberpassword'),

    path('userpanel/',views.UserPanelView.as_view(),name='userpanel'),
    path('show_last_order/',views.show_last_order,name='show_last_order'),
    path('show_user_payments/',views.show_user_payments,name='show_user_payments'),
    path('update_profile/',views.UpdateProfileView.as_view(),name='update_profile'),

]