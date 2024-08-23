# from apps.products.models import Product
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import ProductSerializer
# from CustomPermissions import CustomPermissionForProduct

# class AllProductsApi(APIView):
#     permission_classes=[CustomPermissionForProduct]
#     def get(self,request):
#         products=Product.objects.filter(is_active=True).order_by('-published_date')
#         self.check_object_permissions(request,products)
#         ser_data=ProductSerializer(instance=products,many=True)
#         return Response(data=ser_data.data)
