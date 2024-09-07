from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,ProductGroup,FeatureValue,Brand
from django.db.models import Q,Count,Min,Max
from django.views import View
from .filters import ProductFilter
from .compare import CompareProduct
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView

# --------------------------------------------------------------------------------------
def get_root_group():
    
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))

# --------------------------------------------------------------------------------------
# ارزانترین محصولات
def get_chepest_products(request,*args,**kwargs):

    products=Product.objects.filter(Q(is_active=True)).order_by('price')[:5]
    product_groups=get_root_group()
    context={
        'products':products,
        'product_groups':product_groups,
    }
    return render(request,"products_app/partials/chepest_products.html",context)

# --------------------------------------------------------------------------------------
# جدیدترین محصولات
def get_last_products(request,*args,**kwargs):
    products=Product.objects.filter(Q(is_active=True)).order_by('-published_date')[:5]
    product_groups=get_root_group()
    context={
        'products':products,
        'product_groups':product_groups,
    }
    return render(request,"products_app/partials/last_products.html",context)

# --------------------------------------------------------------------------------------
# گروه های محبوب
def get_popular_products_group(request,*args,**kwargs):
    product_groups=ProductGroup.objects.filter(Q(is_active=True))\
                    .annotate(count=Count('products_of_groups'))\
                    .order_by('-count')

     
    context={
        'product_groups':product_groups,
    }
    return render(request,"products_app/partials/popular_products_group.html",context)

# --------------------------------------------------------------------------------------
# جزیییات محصول
class ProductDetailsView(View):
    def get(self,request,slug):
        product=get_object_or_404(Product,slug=slug)
        if product.is_active:
            product_group = product.product_group.first()
            return render(request,"products_app/product_details.html",{'product':product,'product_group': product_group})
        
# --------------------------------------------------------------------------------------
# محصولات مرتبط
def get_related_products(request,*args,**kwargs):
    current_product=get_object_or_404(Product,slug=kwargs['slug'])
    related_products=[]
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    return render(request,"products_app/partials/related_products.html",{'related_products':related_products})
        
# --------------------------------------------------------------------------------------
# لیست کلیه گروه های محصولات
class ProductsGroupsView(View):
    def get(self,request):
        product_groups=ProductGroup.objects.filter(Q(is_active=True))\
                .annotate(count=Count('products_of_groups'))\
                .order_by('-count')
        return render(request,"products_app/product_groups.html",{'product_groups':product_groups})

# --------------------------------------------------------------------------------------
# لیست گروه محصولات برای فیلتر
def get_product_groups(request):
    product_groups=ProductGroup.objects.annotate(count=Count('products_of_groups'))\
                                       .filter(Q(is_active=True) & ~Q(count=0))\
                                       .order_by('-count')
    return render(request,"products_app/partials/product_groups.html",{'product_groups':product_groups})
    
# --------------------------------------------------------------------------------------
#لیست برندها برای فیلتر
def get_brands(request,*args,**kwargs):
    product_groups=get_object_or_404(ProductGroup,slug=kwargs['slug'])
    brand_list_id=product_groups.products_of_groups.filter(is_active=True,).values('brand_id')
    brands=Brand.objects.filter(pk__in=brand_list_id)\
                        .annotate(count=Count('product_of_brands'))\
                        .filter(~Q(count=0))\
                        .order_by('-count')
    
    return render(request,"products_app/partials/brands.html",{'brands':brands})

# --------------------------------------------------------------------------------------
# لیست های دیگر فیلتر ها بر حسب مقادیر کالاهای درون گروه
def get_feature_for_filter(request,*args,**kwargs):
    product_groups=get_object_or_404(ProductGroup,slug=kwargs['slug'])
    feature_list=product_groups.features_of_groups.all()
    feature_dict=dict()
    for feature in feature_list:
        feature_dict[feature]=feature.feature_values.all()
    return render(request,"products_app/partials/features_filter.html",{'feature_dict':feature_dict})

# --------------------------------------------------------------------------------------
# two dropdown in adminpanel
from django.http import JsonResponse
def get_filter_value_for_feature(request):
    if request.method =='GET':
        feature_id=request.GET["feature_id"]
        feature_value=FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title:fv.id for fv in feature_value}
    return JsonResponse(data=res,safe=False)
    
# -------------------------# دسته بندی محصولات در navbar-----------------------------------

def build_group_tree(parent_group):
    children = ProductGroup.objects.filter(group_parent=parent_group, is_active=True)
    return [
        {
            'group': child,
            'children': build_group_tree(child)
        }
        for child in children
    ]


def product_navigation(request):
    top_level_groups = ProductGroup.objects.filter(group_parent__isnull=True, is_active=True)
    group_tree = []
    for group in top_level_groups:
        group_tree.append({
            'group': group,
            'children': build_group_tree(group)
        })
    return render(request, 'partials/navbar.html', {'group_tree': group_tree})


class ProductListView(ListView):
    model = Product
    template_name = 'partials/sub_group/category2.html'
    context_object_name = 'products'

    def get_queryset(self):
        try:
            group = ProductGroup.objects.get(slug=self.kwargs['slug'])
            return Product.objects.filter(product_group__in=[group], is_active=True)
        except ProductGroup.DoesNotExist:
            return Product.objects.none()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = ProductGroup.objects.get(slug=self.kwargs['slug'])
        return context
    

# ------------------------------------------------------------------------------------------
from django.core.paginator import Paginator
# لیست محصولات هر گروه محصولات
class ProductByGroupsView(View):
    def get(self,request,*args,**kwargs):
        slug=kwargs["slug"]
        current_group=get_object_or_404(ProductGroup,slug=slug)
        products=Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))
        res_aggre=products.aggregate(min=Min('price'),max=Max('price'))

        # price filter
        filter=ProductFilter(request.GET,queryset=products)
        products=filter.qs
        # brand filter
        brands_filter=request.GET.getlist('brand')
        if brands_filter:
            products=products.filter(brand__id__in=brands_filter)
        # features filter
        featuers_filter=request.GET.getlist('feature')
        if featuers_filter:
            products=products.filter(product_features__filter_value__id__in=featuers_filter).distinct()
        # sort typeee
        sort_type=request.GET.get('sort_type')
        if not sort_type:
            sort_type='0'
        if sort_type=='1':
            products=products.order_by('price')
        elif sort_type=='2':
            products=products.order_by('-price')
        group_slug=slug
        product_per_page=5                                 #تعداد کالاها در هر صفحه
        paginator=Paginator(products,product_per_page)       
        page_number=request.GET.get('page')                 #شماره صفحه جاری  
        page_obj=paginator.get_page(page_number)            #لیست کالاها بعد از صفحه بندی برای نمایش در صفحه جاری
        product_count=products.count()                      #تعداد کالاها ی موجود در این گروه
        # لیست اعداد برای منوبازشونده برای تعیین تعداد کالای هر صفحه توسط کاربر
        show_count_product=[]
        i=product_per_page
        while i<product_count:
            show_count_product.append(i)
            i*=2
        show_count_product.append(i)
        context={
            'current_group':current_group,
            'products':products,
            'res_aggre':res_aggre,
            'group_slug':group_slug,
            'page_obj':page_obj,
            'product_count':product_count,
            'show_count_product':show_count_product,
            'filter':filter,
            'sort_type':sort_type,
        }
        return render(request,"products_app/products.html",context)
# ----------------------------------------------------------------
# صفحه اصلی مقایسه : نمایش کالاهای اضافه شده به لیست مقایسه
class ShowCompareListView(View):
    def get(self,request,*args,**kwargs):
        compare_list=CompareProduct(request)
        context={
            'compare_list':compare_list,
        }
        return render(request,'products_app/compare_list.html',context)

# ---------------------------------------------------------------------------
# نمایش جدول کالاهای لیست مقایسه
def compare_table(request):
    compareList=CompareProduct(request)
    products=[]
    # سرستون های جدول مقایسه
    for productId in compareList.compare_product:
        product=Product.objects.get(id=productId)
        products.append(product)
    # ویژگی ها و مقادیر/اطلاعات داخل جدول مقایسه
    featuress=[]
    for product in products:
        for item in product.product_features.all():
            if item.features not in featuress:
                featuress.append(item.features)
 
    context={
        'products':products,
        'features':featuress,
    }
    return render(request,'products_app/partials/compare_table.html',context)

# ------------------------------------------------------------------------------------------
# محاسبه تعداد کالاهای موجود د ر لیست مقایسه
def statuse_of_compare_list(request):
    compareList=CompareProduct(request)
    return HttpResponse(compareList.count)

# ------------------------------------------------------------------------------------------
# اضافه کردن کالا به لیست مقایسه
def add_to_compare_list(request):
    productId=request.GET.get('productId')
    # productGroupId=request.GET.get('productGroupId')
    compareList=CompareProduct(request)
    compareList.add_to_compare_product(productId)
    return HttpResponse('کالا به لیست مقایسه اضافه شد')

# ------------------------------------------------------------------------------------------
# حذف کالا از لیست مقایسه
def delete_from_compare_list(request):
    productId=request.GET.get('productId')
    compareList=CompareProduct(request)
    compareList.delete_from_compare_product(productId)
    return redirect('products:compare_table')

