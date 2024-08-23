from django.db.models import Q
from .models import Favorite, Product
class FavoriteManager:

    def __init__(self, user):
        self.user = user
        
    def add_to_favorite(self, product_id):
        product = Product.objects.get(id=product_id)
        flag = Favorite.objects.filter(
            Q(favorite_user_id=self.user.id) &
            Q(product_id=product_id)
        ).exists()
        if not flag:
            Favorite.objects.create(
                product=product,
                favorite_user=self.user,
            )
            return {'message': 'این کالا به لیست علایق شما اضافه شد', 'status': True}
        return {'message': 'این کالا قبلا در لیست علایق شما قرار گرفته', 'status': False}

    def remove_from_favorite(self, product_id):
        favorite_item = Favorite.objects.filter(
            favorite_user_id=self.user.id,
            product_id=product_id
        )
        if favorite_item.exists():
            favorite_item.delete()
            return {'message': 'این کالا از لیست علایق شما حذف شد', 'status': True}
        return {'message': 'این کالا در لیست علایق شما وجود ندارد', 'status': False}

    def get_favorite_count(self):
        return Favorite.objects.filter(favorite_user_id=self.user.id).count()








# from apps.products.models import Product
# class FavoriteProduct:
#     def __init__(self,request) -> None:
#         self.session=request.session
#         favorite_product=self.session.get('favorites')
#         if not favorite_product:
#             favorite_product=self.session['favorites']=[]
#         self.favorite_product=favorite_product
#         self.count=len(self.favorite_product)
  
#     # ----------------------------------------------
#     def __iter__(self):
#         favorite_product=self.favorite_product.copy()
#         for item in favorite_product:
#             yield item
        
#     # ----------------------------------------------
#     def add_to_favorite_product(self,productId):
#         productId=int(productId)
#         if productId  not in self.favorite_product:
#             self.favorite_product.append(productId)
#         self.count=len(self.favorite_product)
#         self.session.modified=True

#     ----------------------------------------------
#     def delete_from_favorite_product(self, productId):
#         self.favorite_product.remove(int(productId))
#         self.count=len(self.favorite_product)
#         self.session.modified=True

#     # ----------------------------------------------        
#     def cleare_favorite_product(self):
#         del self.session['favorites']
#         self.session.modified=True
        