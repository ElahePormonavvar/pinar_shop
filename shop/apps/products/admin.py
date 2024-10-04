from django.contrib import admin
from django.db.models.fields.related import ManyToManyField
from django.forms.models import ModelMultipleChoiceField
from .models import Brand,ProductGroup,Product,ProductFeature,Feature,ProductGallery,FeatureValue
from django.db.models.aggregates import Count
from django.http import HttpRequest, HttpResponse
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description,order_field
from django.contrib.admin.widgets import AdminSplitDateTime
from .forms import ProductAdminForm
from django.db import models
import jdatetime
# ----------------------------------------------------------------------------
from django.utils.formats import date_format
def jdate_display(value):
    return jdatetime.datetime.fromgregorian(datetime=value).strftime('%Y/%m/%d')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=('brand_title','slug',)
    list_filter=('brand_title',)
    search_fields=('brand_title',)
    ordering=('brand_title',)

# ------------------------------------------------------------------------------
def de_active_product_group(modeladmin,request,queryset):
    res=queryset.update(is_active=False)
    message=f'تعداد گروه {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)

# ====================================

def active_product_group(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f'تعداد گروه {res} کالا فعال شد'
    modeladmin.message_user(request,message)

# ====================================
def export_json(modeladmin,request,queryset):
    response=HttpResponse(content_type='application/json')
    serializers.serialize("json",queryset,stream=response)
    return response

 
# ====================================
class GroupFilter(SimpleListFilter):
    title='گروه محصولات'
    parameter_name='group'

    def lookups(self, request, model_admin):
        sub_groups=ProductGroup.objects.filter(~Q(group_parent=None))
        groups=set([item.group_parent for item in sub_groups])
        return [(item.id,item.group_title)for item in groups]
    
    def queryset(self, request, queryset):
        if self.value()!=None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset
# ====================================
class ProductGroupInstansInLine(admin.TabularInline):
    model=ProductGroup

# ======================================
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display=('group_title','is_active','group_parent','slug','register_date_shamsi', 'update_date_shamsi','count_sub_group','count_produc_of_group')
    list_filter=(GroupFilter,'is_active',)
    # list_filter = (('published_date', JDateFieldListFilter),)
    search_fields=('group_title',)
    ordering=('group_parent','group_title',)
    inlines=[ProductGroupInstansInLine]
    actions=[de_active_product_group,active_product_group,export_json,]
    list_editable=['is_active']
    form = ProductAdminForm

    # formfield_overrides ={models.DateTimeField: {'widget': AdminSplitDateTime},
    #                       models.DateField: {'widget': AdminjDateWidget},}
    
    def published_date_shamsi(self, obj):
        return jdate_display(obj.published_date)
    published_date_shamsi.short_description = 'تاریخ انتشار '
 
    def register_date_shamsi(self, obj):
        return jdate_display(obj.register_date)
    published_date_shamsi.short_description = 'تاریخ درج '

    def update_date_shamsi(self, obj):
        return jdate_display(obj.update_date)
    published_date_shamsi.short_description = 'تاریخ آخرین بروزرسانی'

    # def get_update_date(self, obj):
    #     return obj.update_date.strftime('%Y/%m/%d')  
    # get_update_date.short_description = 'تاریخ آخرین بروزرسانی'

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name in ['published_date',]:
    #          kwargs['widget'] = AdminjDateWidget(attrs={'date_format': '%Y/%m/%d'}) 
    #     return super().formfield_for_dbfield(db_field, **kwargs)
    
# ====================================
    def  get_queryset(self,*args,**kwargs):
        qs = super(ProductGroupAdmin , self).get_queryset(*args,**kwargs)
        qs=qs.annotate(sub_group=Count('groups'))
        qs=qs.annotate(produc_of_group=Count('products_of_groups'))
        return qs
 
# ====================================    
    def count_sub_group(self,obj):
        return obj.sub_group
    
# ==================================== 
    @short_description('تعداد کالاهای گروه')
    @order_field('product_of_group')
    def count_produc_of_group(self,obj):
        return obj.produc_of_group
    
# ==================================== 

    count_sub_group.short_description='تعداد زیر گروه ها'
    de_active_product_group.short_description='غیرفعال کردن گروه های انتخاب شده'
    active_product_group.short_description='فعال کردن گروه های انتخاب شده'
    export_json.short_description='خروجی جیسون از گروه های انتخاب شده'

# ------------------------------------------------------------------------------
def de_active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)

# ====================================

def active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f'تعداد {res} کالا فعال شد'
    modeladmin.message_user(request,message)
    
# ------------------------------------------------------------------------
class ProductFeatureInstansInLine(admin.TabularInline):
    model=ProductFeature
    extra=3

    class Media:
        css = {
            'all' : ('css/admin_style.css',)
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js',
            'js/admin_script.js',)

class ProductGalleryInstansInLine(admin.TabularInline):
    model=ProductGallery
    extra=3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','display_product_groups','price','brand','is_active','update_date','slug',)
    list_filter=('brand','product_group',)
    search_fields=('product_name',)
    ordering=('update_date','product_name',)
    inlines=[ProductFeatureInstansInLine,ProductGalleryInstansInLine]
    list_editable=['is_active']
    actions=[de_active_product,active_product,]



    de_active_product.short_description='غیرفعال کردن کالا انتخاب شده'
    active_product.short_description='فعال کردن کالا انتخاب شده'

    def display_product_groups(self,obj):
        return ','.join([group.group_title for group in obj.product_group.all()])

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name=='product_group':
            kwargs["queryset"]=ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    display_product_groups.short_description='گروه های کالا'
    
    fieldsets = (
        ('اطلاعات محصول',{'fields':(
            'product_name',
            'image_name',
            ('product_group','brand','is_active',),
            'price',
            'summery_description',
            'description',
            'slug',

            )}),
        ('تاریخ و زمان',{'fields':(
            'published_date',

            )}),

    )
    



# ------------------------------------------------------------------------------
class FeatureValueInLine(admin.TabularInline):
    model=FeatureValue
    extra=3

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display=('feature_name','display_groups','display_feature_values',)
    list_filter=('feature_name',)
    search_fields=('feature_name',)
    ordering=('feature_name',)
    inlines=[FeatureValueInLine,]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name=='product_group':
            kwargs["queryset"]=ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def display_groups(self,obj):
        return ','.join([group.group_title for group in obj.product_group.all()])
    
    def display_feature_values(self,obj):
        return ','.join([feature_value.value_title for feature_value in obj.feature_values.all()])
    
    display_groups.short_description='گروه های دارای این ویژگی'
    display_feature_values.short_description='مقادیر ممکن برای این ویژگی'


@admin.register(FeatureValue)
class FeatureValueAdmin(admin.ModelAdmin):
    list_display=('value_title','feature',)

    fieldsets = (
        (None, {
            'fields': (
                'feature',
                'value_title',
            ),
        }),
    )