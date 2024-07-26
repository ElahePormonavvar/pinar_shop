from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import CommentForm
from apps.products.models import Product
from .models import Comment
from django.contrib import messages
from apps.comment_scoring_favorites.models import Scoring,Favorite
from django.http import HttpResponse
from django.db.models import Avg
from django.db.models import Q
from .favorite import favoriteProduct
# ---------------------------------------------------------
class CommentView(View):
    def get(self,request, *args, **kwargs):
        product_id=request.GET.get('product_id')
        comment_id=request.GET.get('comment_id')
        slug=kwargs['slug']

        initial_dict={
            'product_id':product_id,
            'comment_id':comment_id,
        }
        form=CommentForm(initial=initial_dict)
        return render(request,'csf_app/partials/create_comment.html',{'form':form,'slug':slug})
    
    def post(self,request, *args, **kwargs):
        slug=kwargs.get('slug')
        product=get_object_or_404(Product,slug=slug)
        form=CommentForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            parent=None
            if(cd['comment_id']):
                parentId=cd['comment_id']
                parent=Comment.objects.get(id=parentId)
            Comment.objects.create(
                product=product,
                commenting_user=request.user,
                comment_text=cd['comment_text'],
                comment_parent=parent,
            )
            messages.success(request,'نظر شما با موفقیت ثبت شد')
            return redirect('products:product_details',product.slug)
        messages.error(request,'خطا در ارسال نظر','danger')
        return redirect('products:product_details',product.slug)
    
# -----------------------------------------------------------------------
def add_score(request):
    productId=request.GET.get('productId')
    score=request.GET.get('score')
    product=Product.objects.get(id=productId)
    Scoring.objects.create(
        product=product,
        scoring_user=request.user,
        score=score,
    )
    return HttpResponse('امتیاز شما با موفقیت ثبت شد')

# -----------------------------------------------------------------------
# def update_avg_score(request):

#     productId=request.GET.get('productId')
#     score=request.GET.get('score')
#     product=Product.objects.get(id=productId)

#     avgScore=Scoring.objects.all().aggregate(Avg('score'))['score__avg']
#     if avgScore==None:
#         avgScore=0

#     Scoring.objects.update(
#         product=product,
#         scoring_user=request.user,
#         score=score,
#     )
#     return HttpResponse(avgScore)

# ----------------------------------------------------------------------------
class ShowFavoriteListView(View):
    def get(self,request,*args,**kwargs):
        favorite_list=favoriteProduct(request)
        context={
            'compare_list':favorite_list,
        }
        return render(request,'csf_app/partials/create_favorites.html',context)
    
# -----------------------------------------
def statuse_of_favorite_list(request):
    favoriteList=favoriteProduct(request)
    print(favoriteList.count)
    return HttpResponse(favoriteList.count)

# ------------------------------------------
def add_to_favorite(request):
    productId=request.GET.get('productId')
    product=Product.objects.get(id=productId)
    flag=Favorite.objects.filter(
        Q(favorite_user_id=request.user.id) &
        Q(product_id=productId)).exists()
    if(not flag):
        Favorite.objects.create(
            product=product,
            favorite_user=request.user,
        )
        return HttpResponse('این کالا به لیست علایق شما اضافه شد')
    return HttpResponse('این کالا قبلا در لیست  علایق  شما قرار گرفته')

# ---------------------------------------------------
# حذف کالا از لیست علاقه مندی ها

def delete_from_favorite(request):
    productId=request.GET.get('productId')
    favoriteList=favoriteProduct(request)
    favoriteList.delete_from_favorite_product(productId)
    return redirect('csf:user_favorite_list')

# ---------------------------------------------------
# def update_favorite(request):
#     productId=request.GET.get('productId')
#     product=Product.objects.get(id=productId)

# ----------------------------------------------------
class UserFavoriteView(View):
    def get(self,request,*args,**kwargs):
        user_favorite_products=Favorite.objects.filter(Q(favorite_user_id=request.user.id))
        return render(request,'csf_app/user_favorite.html',{'user_favorite_products':user_favorite_products})
