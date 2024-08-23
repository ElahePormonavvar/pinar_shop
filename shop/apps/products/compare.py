# from .models import Product

class CompareProduct:
    def __init__(self,request) -> None:
        self.session=request.session
        compare_product=self.session.get('compare_product')
        if not compare_product:
            compare_product=self.session['compare_product']=[]
        self.compare_product=compare_product
        self.count=len(self.compare_product)
        # self.grouptype=Product.products_of_groups.group_title

    # ----------------------------------------------
    def __iter__(self):
        compare_product=self.compare_product.copy()
        for item in compare_product:
            yield item
        
    # ----------------------------------------------
    def add_to_compare_product(self,productId):
        productId=int(productId)
        # product=Product.objects.get(id=productId)
        if productId  not in self.compare_product:   #and self.grouptype == product.getMainProductGroups()
            self.compare_product.append(productId)
        self.count=len(self.compare_product)
        self.session.modified=True

    # ----------------------------------------------
    def delete_from_compare_product(self, productId):
        self.compare_product.remove(int(productId))
        self.count=len(self.compare_product)
        self.session.modified=True

    # ----------------------------------------------        
    def cleare_compare_product(self):
        del self.session['compare_product']
        self.session.modified=True
