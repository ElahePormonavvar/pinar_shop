from typing import Any
from django.http import HttpRequest
# from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .forms import RegisterUserForm,VerifyRegisterForm,LoginUserForm,ChangePasswordForm,RememberPasswordForm,UpdateProfileForm
import utils
from .models import CustomUser,Customer
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin     
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.main.models import Contact
# -----------------------------------------------------------------------------------------
class RegisterUserView(View):

    def dispatch(self, request,*args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    template_name="accounts_app/register.html"    
    
    def get(self,request,*args,**kwargs):
        form=RegisterUserForm()
        return render(request,self.template_name,{'form':form})
    
    # وقتی دکمه زده میشه  به متد پست ارسال میشه
    def post(self,request,*args,**kwargs):
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            active_code=utils.creat_random_code(5)
            CustomUser.objects.create_user(
                mobile_number=data['mobile_number'],
                active_code=active_code,
                password=data['password1'],
            )
            utils.send_sms(data['mobile_number'],active_code)
            request.session['user_session']={
                'active_code':str(active_code),
                'mobile_number':data['mobile_number'],
                'rememberpassword':False,

            }
            messages.success(request,'اطلاعات شما ثبت شد.کد فعال سازی را وارد کنید','success')
            return redirect('accounts:verify')
        messages.error(request,'خطا در انجام ثبت نام','danger')

        return render(request,self.template_name,{'form':form})

# ---------------------------------------------------------------------------------------------------
class VerifyRegisterCodeView(View):
    
    def dispatch(self, request,*args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    template_name="accounts_app/verify_register_code.html"

    def get(self,request,*args,**kwargs):
        form=VerifyRegisterForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=VerifyRegisterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session['user_session']
            if data['active_code']==user_session['active_code']:
                user=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                if user_session['rememberpassword']==False:
                    user.is_active=True
                    user.active_code=utils.creat_random_code(5)
                    user.save()
                    messages.success(request,'ثبت نام با موفقیت انجام شد','success')
                    return redirect('main:index')
                else:
                    return redirect("accounts:changepassword")
            else:
                messages.error(request,'کد فعال سازی وارد شده اشتباه می باشد','danger')
                return render(request,"accounts_app/verify_register_code.html",{"form":form})
        messages.error(request,'اطلاعات وارد شده معتبر نمی باشد','danger')
        return render(request,self.template_name,{"form":form})
    
# -------------------------------------------------------------------------------------------------------
class LoginUserView(View):

    def dispatch(self, request,*args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    template_name="accounts_app/login.html"
    def get(self,request,*args,**kwargs):
        form=LoginUserForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
            form=LoginUserForm(request.POST)
            if form.is_valid():
                data=form.cleaned_data
                user=authenticate(username=data['mobile_number'],password=data['password'])
                if user is not None:
                    db_user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                    
                    if db_user.is_admin==False:
                        messages.success(request,'ورود با موفقیت انجام شد','success')
                        login(request,user)
                        next_url=request.GET.get("next")
                        if next_url is not None:
                            return redirect(next_url)
                        else:
                            return redirect("main:index")
                    else:
                        messages.error(request,'کاربر ادمین نمی تواند از اینجا وارد شود','warning')
                        return render(request,self.template_name,{'form':form})
                    
                else:
                    messages.error(request,'اطلاعات وارد شده نادرست است','danger')
                    return render(request,self.template_name,{'form':form})
            else:
                messages.error(request,'اطلاعات وارد شده نامعتبر است','danger')
                return render(request,self.template_name,{"form":form})

# --------------------------------------------------------------------------------------------
class LogoutUserView(View):

    def dispatch(self, request,*args: Any, **kwargs: Any):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args,**kwargs):
        session_data=request.session.get('shop_cart')
        logout(request)
        request.session['shop_cart']=session_data
        return redirect("main:index")

# ----------------------------------------------------------------------------------------
class UserPanelView(LoginRequiredMixin,View):
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)
            user_info={
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "phone_number":customer.phone_number,
                "address":customer.address,
                "image":customer.image_name
            }
        except ObjectDoesNotExist:
            user_info={
                "name":user.name,
                "family":user.family,
                "email":user.email,
            } 
        return render(request,'accounts_app/userpanel.html',{'user_info':user_info})     


# ------------------------------------------------------------------------------------------------
class ChangePasswordView(View):
    template_name="accounts_app/changepassword.html"

    def get(self,request,*args,**kwargs):
        form=ChangePasswordForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session['user_session']
            user=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user.set_password(data['password1'])
            user.active_code=utils.creat_random_code(5)
            user.save()
            messages.success(request,'رمزعبور شما با موفقیت تغییر کرد','success')
            return redirect("accounts:login")
        else:
            messages.error(request,'اطلاعات وارد شده معتبر نمی باشد','danger')
            return render(request,self.template_name,{"form":form})

# ---------------------------------------------------------------------------------
class RememberPasswordView(View):
    template_name="accounts_app/rememberpassword.html"

    def get(self,request,*args,**kwargs):
        form=RememberPasswordForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RememberPasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=CustomUser.objects.get(mobile_number=data['mobile_number'])
            active_code=utils.creat_random_code(5)
            user.active_code=active_code
            user.save()

            utils.send_sms(data['mobile_number'],active_code)
            request.session['user_session']={
                'active_code':str(active_code),
                'mobile_number':data['mobile_number'],
                'rememberpassword':True,
               }
            messages.success(request,'جهت تغیر رمزعبور کد دریافتی را ارسال کنید','success')
            return redirect('accounts:verify')

# -----------------------------------------------------------------------------------------
class UpdateProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)
            initial_dict={
                "mobile_numbe":user.mobile_number,
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "phone_number":customer.phone_number,
                "address":customer.address,
                
            }
        except ObjectDoesNotExist:
            initial_dict={
                "mobile_numbe":user.mobile_number,
                "name":user.name,
                "family":user.family,
                "email":user.email,
            }
        form=UpdateProfileForm(initial=initial_dict)
        return render(request,'accounts_app/update_profile.html',{'form':form,'image_url':customer.image_name})

    def post(self,request):
        form=UpdateProfileForm(request.POST,request.FILES)
        if form.is_valid():
            cd=form.cleaned_data
            user=request.user
            user.name=cd["name"]
            user.family=cd["family"]
            user.email=cd["email"]
            user.save()
            try:
                customer=Customer.objects.get(user=request.user)
                customer.phone_number=cd["phone_number"]
                customer.address=cd["address"]
                customer.image_name=cd["image"]
                customer.save()

            except ObjectDoesNotExist:
                Customer.objects.create(
                    user=request.user,
                    phone_number=cd["phone_number"],
                    address=cd["address"],
                    image_name=cd["image"],
                )
            messages.success(request,'ویرایش پروفایل با موفقیت انجام شد','success')  
            return redirect('accounts:userpanel') 
        else:
            messages.error(request,'اطلاعات وارد شده معتبر نمی باشد','danger')
            return render(request,'accounts:update_profile.html',{'form':form,'image_url':customer.image_name})

        
# -----------------------------------------------------------------------------------------
@login_required
def show_last_order(request):
    orders = Order.objects.filter(customer_id=request.user.id).order_by('-register_date')[:4]

    # تبدیل تاریخ‌ها به شمسی
    orders_with_jalali_date = []
    for order in orders:
        order_jalali = {
            'id': order.id,
            'register_date': utils.gregorian_to_jalali(order.register_date),
            'order_state': order.order_state,
            'get_order_total_price': order.get_order_total_price(),
        }
        orders_with_jalali_date.append(order_jalali)

    # ارسال لیست جدید به قالب
    return render(request, 'accounts_app/partials/show_last_order.html', {'orders': orders_with_jalali_date})

# -----------------------------------------------------------------------------------------
@login_required
def show_user_payments(request):
    payments=Payment.objects.filter(customer_id=request.user.id).order_by('-register_date')
    return render(request,'accounts_app/show_user_payments.html',{'payments':payments})

# ------------------------------------------------------------------------------------------
@login_required
def show_last_messages(request):
    contacts=Contact.objects.filter(contact_user_id=request.user.id)
    print(contacts)
    return render(request,'accounts_app/partials/show_last_messages.html',{'contacts':contacts})