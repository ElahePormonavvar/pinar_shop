from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product,ProductGroup
from apps.accounts.models import Customer
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order,OrderDetails,PaymentType
from .forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist
from apps.discounts.forms import CouponForm
from apps.discounts.models import Coupon
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
import utils

# ----------------------------------------------------------
def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
# -------------------------------------------------------------------
class ShopCartView(View):
    def get(self,request,*args,**kwargs):
        shop_cart=ShopCart(request)
        return render (request,"orders_app/shop_cart.html",{"shop_cart":shop_cart})

# ---------------------------------------------------------------
def show_shop_cart(request):
    shop_cart=ShopCart(request)

    tutal_price=shop_cart.calc_tutal_price()
    order_final_price,delivery,tax=utils.price_by_delivery_tax(tutal_price)

    context={
        "shop_cart":shop_cart,
        "shop_cart_count":shop_cart.count,
        "tutal_price":tutal_price,
        "delivery":delivery,
        "tax":tax,
        "order_final_price":order_final_price,
    }
    return render (request,"orders_app/partials/show_shop_cart.html",context)
 
# ---------------------------------------------------------------
def add_to_shop_cart(request):
    product_id=request.GET.get('product_id')
    tedad=request.GET.get('tedad')
    shop_cart=ShopCart(request)
    product=get_object_or_404(Product,id=product_id)
    shop_cart.add_to_shop_cart(product,tedad)
    return HttpResponse(shop_cart.count)

# ---------------------------------------------------------------
def delete_from_shop_cart(request):
    product_id=request.GET.get('product_id')
    product=get_object_or_404(Product,id=product_id)
    shop_cart=ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect("orders:show_shop_cart")

# ---------------------------------------------------------------
def update_shop_cart(request):
    product_id_list=request.GET.getlist('product_id_list[]')
    tedad_list=request.GET.getlist('tedad_list[]')
    shop_cart=ShopCart(request)
    shop_cart.update(product_id_list,tedad_list)
    return redirect("orders:show_shop_cart")

# ---------------------------------------------------------------
def status_of_shop_cart(request):
    shop_cart=ShopCart(request)
    return HttpResponse(shop_cart.count)

# ---------------------------------------------------------------
class CreateOrderView(LoginRequiredMixin,View):
    def get(self, request):
        try:
            customer=Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer=Customer.objects.create(user=request.user)

        order=Order.objects.create(customer=customer,payment_type=get_object_or_404(PaymentType,id=1))
        
        shop_cart=ShopCart(request)
        for item in shop_cart:
            OrderDetails.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                tedad=item['tedad']
            )
        return redirect('orders:checkout_order',order.id)
    
# ----------------------------------------------------------------
class CheckOutOrderView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        user=request.user
        customer=get_object_or_404(Customer,user=user)
        shop_cart=ShopCart(request)
        order=get_object_or_404(Order,id=order_id)

        tutal_price=shop_cart.calc_tutal_price()
        order_final_price,delivery,tax=utils.price_by_delivery_tax(tutal_price,order.discount)
             
        data={
            'name':user.name,
            'family':user.family,
            'email':user.email,
            'phone_number':customer.phone_number,
            'address':customer.address,
            'description':order.description,
            'payment_type':order.payment_type,
            'order':order,
        }
        form=OrderForm(data)
        form_coupon=CouponForm()
        context={
            'shop_cart':shop_cart,
            'tutal_price':tutal_price,
            'delivery':delivery,
            'tax':tax,
            'order_final_price':order_final_price,
            'form':form,
            'form_coupon':form_coupon,
            'order':order,
        } 
        return render(request,'orders_app/checkout.html',context)
    
    def post(self,request,order_id):
        form=OrderForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            try:
                order=Order.objects.get(id=order_id)
                order.description=cd['description']
                order.payment_type=PaymentType.objects.get(id=cd['payment_type'])
                order.save()

                order_detail=OrderDetails.objects.filter(order_id=order_id)             
                for od in order_detail: 
                    od.price=od.product.get_price_by_discount()
                    od.save()
                    
                user=request.user
                user.name=cd['name']
                user.family=cd['family']
                user.email=cd['email']
                user.save()

                customer=Customer.objects.get(user=user)
                customer.phone_number=cd['phone_number']
                customer.address=cd['address']
                customer.save()
                
                messages.success(request,'اطلاعات با موفقیت ثبت شد','')
                return redirect('payments:request',order_id)                      
            except ObjectDoesNotExist:
                messages.error(request,'فاکتوری با این مشخصات یافت نشد','danger')
                return redirect('orders:checkout_order',order_id)
            
        return redirect('orders:checkout_order',order_id)
# ---------------------------------------------------------------------------
class ApplyCoupon(View):
    def post(self,request,*args,**kwargs):
        order_id=kwargs["order_id"]
        coupon_form=CouponForm(request.POST)
        if coupon_form.is_valid():
            cd=coupon_form.cleaned_data
            coupon_code=cd["coupon_code"]
        coupon=Coupon.objects.filter(
           Q(coupon_code=coupon_code) &
           Q(is_active=True) &
           Q(start_date__lte=datetime.now()) &
           Q(end_date__gte=datetime.now())
        )
        deiscount=0
        try:
            order=Order.objects.get(id=order_id)
            if coupon:
                deiscount=coupon[0].discount
                order.discount=deiscount
                order.save()
                messages.success(request,'اعمال کد با موفقیت انجام شد')
                return redirect('orders:checkout_order',order_id)
            else:
                order.discount=deiscount
                order.save()
                messages.error(request,'کد وارد شده معتبر نیست','danger')
        except ObjectDoesNotExist:
            messages.error(request,'سفارش موجود نیست')
        return redirect('orders:checkout_order',order_id)

# ------------------------------------------------------------------------------
def best_selling_products_view(request):
    best_selling_products = OrderDetails.get_best_selling_products()
    new_products=Product.objects.filter(Q(is_active=True)).order_by('-published_date')[:5]
    product_groups = get_root_group()
    context={
        'best_selling_products':best_selling_products,
        'new_products':new_products,
        'product_groups':product_groups,
    }
    return render(request, 'products_app/partials/seller_best.html',context)

# ------------------------------------------------------------------------------
