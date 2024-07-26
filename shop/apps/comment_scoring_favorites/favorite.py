from apps.products.models import Product


class favoriteProduct:
    def __init__(self,request) -> None:
        self.session=request.session
        favorite_product=self.session.get('favorite_product')
        if not favorite_product:
            favorite_product=self.session['favorite_product']=[]
        self.favorite_product=favorite_product
        self.count=len(self.favorite_product)
        # self.grouptype=Product.products_of_groups.group_title

    # ----------------------------------------------
    def __iter__(self):
        favorite_product=self.favorite_product.copy()
        for item in favorite_product:
            yield item
        
    # ----------------------------------------------
    def add_to_favorite_product(self,productId):
        productId=int(productId)
        # product=Product.objects.get(id=productId)
        if productId  not in self.favorite_product:   #and self.grouptype == product.getMainProductGroups()
            self.favorite_product.append(productId)
        self.count=len(self.favorite_product)
        self.session.modified=True

    # ----------------------------------------------
    def delete_from_favorite_product(self, productId):
        self.favorite_product.remove(int(productId))
        self.count=len(self.favorite_product)
        self.session.modified=True

    # ----------------------------------------------        
    # def cleare_favorite_product(self):
    #     del self.session['favorite_product']
    #     self.session.modified=True
        