from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser

# ---------------------------------------------------------------------------------
class WarehouseType(models.Model):
    warehouse_type_title=models.CharField(max_length=50,verbose_name='نوع انبار')

    def __str__(self) -> str:
        return self.warehouse_type_title
    
    class Meta:
        verbose_name='نوع انبار'
        verbose_name_plural='انواع روش انبار'

# ---------------------------------------------------------------------------------
class Warehous(models.Model):
    warehouse_type=models.ForeignKey(WarehouseType,on_delete=models.CASCADE,related_name='warehous',verbose_name='انبار')
    user_register=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='warehoseuser_rigister',verbose_name='کاربرتغییرانبار')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='warehous_product',verbose_name='کالا')
    tedad=models.IntegerField(verbose_name='تعداد')
    price=models.IntegerField(verbose_name='قیمت',blank=True,null=True)
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')

    def __str__(self) -> str:
        return f"{self.warehouse_type} {self.product}"
    
    class Meta:
        verbose_name='انبار'
        verbose_name_plural='انبار ها'