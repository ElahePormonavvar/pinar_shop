from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import CommentForm
from apps.products.models import Product
from .models import Comment
from django.contrib import messages
from apps.comment_scoring_favorites.models import Scoring,Favorite
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .favorites import FavoriteManager
from django.db.models import Avg
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
    avg_score = product.scoring_product.all().aggregate(Avg('score'))['score__avg']
    if avg_score is None:
        avg_score = 0

    # ارسال پاسخ به صورت JSON
    return JsonResponse({
        'message': 'امتیاز شما با موفقیت ثبت شد',
        'avg_score': round(avg_score, 2),  # میانگین با دو رقم اعشار
    })
    # return HttpResponse('امتیاز شما با موفقیت ثبت شد')

# ----------------------------------------------------------------------------
def add_to_favorite(request):
    productId = request.GET.get('productId')
    manager = FavoriteManager(request.user)
    result = manager.add_to_favorite(productId)
    return JsonResponse({
        'message': result['message'],
        'status': result['status'],
    })

# ----------------------------------------------------------------------------
def remove_from_favorite(request):
    productId = request.GET.get('productId')
    manager = FavoriteManager(request.user)
    result=manager.remove_from_favorite(productId)

    if result['status']:
        return redirect('csf:show_favorite_list')
    return JsonResponse({
        'message': result['message'],
        'status': result['status'],
    })

# ---------------------------------------------------------------------------
def update_favorite_count(request):
    manager = FavoriteManager(request.user)
    favorite_count = manager.get_favorite_count()
    return HttpResponse(favorite_count)

# ---------------------------------------------------------------------------
def show_favorite_list(request):
    return render(request,'csf_app/partials/create_favorites.html')

# ----------------------------------------------------------------------------
class UserFavoriteView(View):
    def get(self,request,*args,**kwargs):
        user_favorite_products=Favorite.objects.filter(Q(favorite_user_id=request.user.id))
        return render(request,'csf_app/user_favorite.html',{'user_favorite_products':user_favorite_products})
    
# -----------------------------------------------------------------------------









