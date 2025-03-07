from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Product
from django.utils import timezone
import uuid
import utils
from django.db.models import Sum

# ---------------------------------------------
class PaymentType(models.Model):
    payment_title=models.CharField(max_length=50,verbose_name='نوع پرداخت')

    def __str__(self) -> str:
        return self.payment_title
    
    class Meta:
        verbose_name='پرداخت'
        verbose_name_plural='انواع روش پرداخت'
# --------------------------------------------------------------------------------
class OrderState(models.Model):
    order_state_title=models.CharField(max_length=50,verbose_name='عنوان وضعیت سفارش')

    def __str__(self) -> str:
        return self.order_state_title
    
    class Meta:
        verbose_name='وضعیت سفارش'
        verbose_name_plural='انواع وضعیت های سفارش'
# ----------------------------------------------------------------------------------
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='orders',verbose_name='مشتری')
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ درج سفارش')
    update_date=models.DateField(auto_now=True,verbose_name='تاریخ ویرایش سفارش')
    is_finaly=models.BooleanField(default=False,verbose_name='نهایی شده')
    order_code=models.UUIDField(unique=True,default=uuid.uuid4,editable=False,verbose_name='کد تولیدی سفارش')
    discount=models.IntegerField(blank=True,null=True,default=0,verbose_name='تخفیف روی فاکتور')
    description=models.TextField(blank=True,null=True,verbose_name='توضیحات')
    payment_type=models.ForeignKey(PaymentType,default=None,null=True,blank=True,on_delete=models.CASCADE,verbose_name='نوع پردخت',related_name='payment_types')
    order_state=models.ForeignKey(OrderState,on_delete=models.CASCADE,null=True,blank=True,verbose_name='وضعیت سفارش',related_name='orders_states')

    def get_order_total_price(self):
        sum=0
        for item in self.order_details1.all():
            sum+=item.product.get_price_by_discount()*item.tedad
        order_final_price,delivery,tax=utils.price_by_delivery_tax(sum,self.discount)
        return int(order_final_price)
    
# ----------------------------------------------------------

    def __str__(self) -> str:
        return f"{self.customer}\t{self.id}\t{self.is_finaly}"
    
    class Meta:
        verbose_name='سفارش'
        verbose_name_plural='سفارشات'
# --------------------------------------------------------------------------------
class OrderDetails(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_details1',verbose_name='سفارش')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_details2',verbose_name='کالا')
    tedad=models.PositiveIntegerField(default=1,verbose_name='تعداد')
    price=models.IntegerField(verbose_name='قیمت کالا در فاکتور')

    def __str__(self) -> str:
        return f"{self.order}\t{self.product}\t{self.tedad}\t{self.price}"
    
    def get_best_selling_products(limit=10):
        best_selling_products = Product.objects.filter(
            order_details2__order__is_finaly=True  # فقط سفارشات نهایی شده را در نظر بگیرید
        ).annotate(
            total_sales=Sum('order_details2__tedad')  # جمع تعداد فروش‌ها برای هر محصول
        ).order_by('-total_sales')[:limit]  # مرتب‌سازی نزولی بر اساس تعداد فروش و محدود کردن به تعداد دلخواه
        
        return best_selling_products