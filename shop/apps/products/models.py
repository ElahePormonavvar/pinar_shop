from django.db import models
from utils import FileUpload
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from datetime import datetime
from django.db.models import Sum,Avg,Q
from middlewares.middleware import RequestMiddleware
# from ckeditor.fields import RichTextField
# from django.db.models.signals import post_delete
# from django.dispatch import receiver

# ---------------------------------------------------------
class Brand(models.Model):
    brand_title=models.CharField(max_length=100,verbose_name='نام برند')
    file_upload=FileUpload('images','brand')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر برند ')
    slug=models.SlugField(max_length=200,null=True)

    def __str__(self):
        return self.brand_title
    
    class Meta:
        verbose_name='برند'
        verbose_name_plural='برندها'

# ---------------------------------------------------------
class ProductGroup(models.Model):
    group_title=models.CharField(max_length=100,verbose_name='عنوان گروه کالا')
    file_upload=FileUpload('images','product_group')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر گروه کالا')
    description=RichTextUploadingField(config_name='default',blank=True,verbose_name='توضیحات')
    is_active=models.BooleanField(default=True,blank=True,verbose_name='وضعیت فعال/غیرفعال')
    group_parent=models.ForeignKey('ProductGroup',on_delete=models.CASCADE,blank=True,null=True,verbose_name='والد گروه کالا',related_name='groups')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج ')
    published_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ آخرین بروز رسانی')
    slug=models.SlugField(max_length=200,null=True)
 
    def __str__(self) -> str:
        return self.group_title
    
    class Meta:
        verbose_name='گروه کالا'
        verbose_name_plural='گروه های کالا'

# -----------------------------------------------------------------------
class Feature(models.Model):
    feature_name=models.CharField(max_length=100,verbose_name='نام ویژگی')
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='features_of_groups')

    def __str__(self) -> str:
        return self.feature_name
    
    class Meta:
        verbose_name='ویژگی'
        verbose_name_plural='ویژگی ها'

# -----------------------------------------------------------------------
class Product(models.Model):
    product_name=models.CharField(max_length=500,verbose_name='نام کالا')
    summery_description=models.TextField(default='',null=True,blank=True,verbose_name='توضیحات مختصر')
    description=RichTextUploadingField(config_name='default',blank=True,verbose_name='توضیحات کامل')
    file_upload=FileUpload('images','product')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر کالا')
    price=models.PositiveIntegerField(default=0,verbose_name='قیمت کالا')
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='products_of_groups')
    features=models.ManyToManyField(Feature,through='ProductFeature')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,verbose_name='برند کالا',related_name='product_of_brands')
    is_active=models.BooleanField(default=True,blank=True,verbose_name='وضعیت فعال/غیرفعال')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج ')
    published_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ آخرین بروز رسانی')
    slug=models.SlugField(max_length=200,null=True)

    def __str__(self) -> str:
        return self.product_name
    
    def get_absolute_url(self):
        return reverse('products:product_details', kwargs={'slug': self.slug})
    

# ================قیمت با تخفیف کالا====================
    def get_price_by_discount(self):
        list1=[]
        for dbd in self.discount_basket_details2.all(): 
          if (dbd.discount_basket.is_active == True and
              dbd.discount_basket.start_date <= datetime.now() and
              datetime.now() <= dbd.discount_basket.end_date):
            list1.append(dbd.discount_basket.discount)
             
        discount=0
        if(len(list1) > 0):
            discount = max(list1)
        return self.price-(self.price*discount/100)
    
# ==============تعداد موجودی کالا در انبار================
    def get_number_in_warehouse(self):
        sum1=self.warehous_product.filter(warehouse_type_id=1).aggregate(Sum('tedad'))
        sum2=self.warehous_product.filter(warehouse_type_id=2).aggregate(Sum('tedad'))
        input=0
        if sum1['tedad__sum']!=None:
            input=sum1['tedad__sum']
        output=0
        if sum2['tedad__sum']!=None:
            output=sum2['tedad__sum']
        return input-output

# ======میزان امتیازی که کاربر جاری به این کالا داده========
    def get_user_score(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        score=0
        user_score=self.scoring_product.filter(scoring_user=request.user)
        if user_score.count()>0:
            score=user_score[0].score
        return score
 
# =======میانگین امتیازی که این کالا کسب کرده============
    def get_average_score(self):
        avgScore=self.scoring_product.all().aggregate(Avg('score'))['score__avg']
        if avgScore==None:
            avgScore=0
        return round(avgScore,2)

# ======================================================
# آیا این کالا مورد علاقه کاربر جاری بوده یا خیر
    def get_user_favorite(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        flag=self.favorite_product.filter(favorite_user=request.user).exists()
        return flag

# ======================================================
    def getMainProductGroups(self):
        return self.product_group.all()[0].id
        
# ======================================================
    class Meta:
        verbose_name='کالا'
        verbose_name_plural='کالاها'

# --------------------------------------------------------------------------------------------------------
class FeatureValue(models.Model):
    value_title=models.CharField(max_length=100,verbose_name='عنوان مقدار')
    feature=models.ForeignKey(Feature,on_delete=models.CASCADE,blank=True,null=True,verbose_name='ویژگی',related_name='feature_values')

    def __str__(self) -> str:
        return f"{self.id} {self.value_title}"

    class Meta:
        verbose_name='مقدار ویژگی'
        verbose_name_plural='مقدار ویژگی ها'

# -----------------------------------------------------------------------
class ProductFeature(models.Model):
    products=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='product_features')
    features=models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name='ویژگی')
    value=models.CharField(max_length=100,verbose_name='مقدار ویژگی کالا')
    filter_value=models.ForeignKey(FeatureValue,null=True,blank=True,on_delete=models.CASCADE,verbose_name='مقدار ویژگی فیلتر',related_name='filter_feature_value')


    def __str__(self) -> str:
        return f"{self.products} - {self.features} : {self.value}"
    
    class Meta:
        verbose_name='ویژگی محصول'
        verbose_name_plural='ویژگی محصولات'

# -----------------------------------------------------------------------
class ProductGallery(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='gallery_images')
    file_upload=FileUpload('images','product_gallery')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر کالا')

    class Meta:

        verbose_name='تصویر'
        verbose_name_plural='تصاویر'

# -----------------------------------------------------------------------
