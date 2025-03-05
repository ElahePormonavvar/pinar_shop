from django.shortcuts import render,redirect
from django.conf import settings
from django.views import View
from .models import Slider
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import ContactForm
from .models import Contact
from django.contrib import messages
from apps.accounts.models import Customer
# ----------------------------------------------------------------
def media_admin(request):
    return {"media_url":settings.MEDIA_URL}

# ----------------------------------------------------------------
def index(request):
    return render(request,"main_app/index.html")

# ----------------------------------------------------------------
class SlideView(View):
    def get(self,request):
        sliders=Slider.objects.filter(Q(is_active=True))
        return render(request,"main_app/sliders.html",{'sliders':sliders})
    
# ----------------------------------------------------------------
def handler404(request,exception=None):
    return render(request,'main_app/404.html')

# -------------------------------------------------------------------
def about_us(request):
    return render(request,"partials/about_us.html")

# ---------------------------------------------------------------------
class ContactView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            customer=Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            customer = None
        if customer:
            data = {
                'name': customer.user.name,
                'family': customer.user.family,
                'email': customer.user.email,
                'phone_number': customer.phone_number,
            }
        else:
            data = {}

        form = ContactForm(initial=data)  # فرم را با اطلاعات اولیه پر می‌کنیم
        context = {
            'form': form,
        }
        return render(request, 'partials/contact_us.html', context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)  # فرم را ذخیره نمی‌کنیم تا کاربر را اضافه کنیم
            try:
                    customer = Customer.objects.get(user=request.user)
                    contact.contact_user = customer  # مشتری جاری را به فرم اضافه می‌کنیم
                    contact.save()  # فرم را ذخیره می‌کنیم

                    messages.success(request, 'پیام شما با موفقیت ارسال شد.')
                    return redirect('main:index')  # هدایت به صفحه اصلی
            except Customer.DoesNotExist:
                messages.error(request, 'خطا در یافتن مشتری. لطفاً وارد حساب کاربری خود شوید.')

            context = {
                'form': form,
            }
        return render(request, 'partials/contact_us.html', context)

