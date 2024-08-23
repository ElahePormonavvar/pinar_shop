from django.shortcuts import render,redirect
from django.views import View
from django.db.models import Q
from apps.products.models import Product

class SearchResultView(View):
    def get(self,request,*args,**kwarg):
        query=self.request.GET.get("q")
        products=Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(summery_description__icontains=query) 
        )
        context={
            'products':products,
        }
        return render(request,'searchs_app/search_results.html',context)
