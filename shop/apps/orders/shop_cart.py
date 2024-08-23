# کدهایی که نیاز به دیتا بیس ندارد بهتره در این فایل مجزا نوشته بشه
# ماژول مجزا
from apps.products.models import Product


class ShopCart:
    def __init__(self,request):
        self.session=request.session
        temp=self.session.get('shop_cart')
        if not temp:
            temp=self.session['shop_cart']={}
        self.shop_cart=temp
        self.count=len(self.shop_cart.keys())

    def update(self,product_id_list,tedad_list):
        i=0
        for product_id in product_id_list:
            self.shop_cart[product_id]['tedad']=int(tedad_list[i])
            i+=1
        self.save()

    def save(self):
        self.session.modified=True

    def add_to_shop_cart(self,product,tedad):
        product_id=str(product.id)
        if product_id not in self.shop_cart:
            self.shop_cart[product_id]={"tedad":0,"price":product.price,"final_price":product.get_price_by_discount()}
        self.shop_cart[product_id]["tedad"]+=int(tedad)
        self.count=len(self.shop_cart.keys())
        self.save()

    def delete_from_shop_cart(self,product):
        product_id=str(product.id)
        del self.shop_cart[product_id]
        self.save()

    def __iter__(self):
        list_ids=self.shop_cart.keys()
        products=Product.objects.filter(id__in=list_ids)
        temp=self.shop_cart.copy()
        for product in products:
            temp[str(product.id)]["product"]=product

        for item in temp.values():
            item["tutal_price"]=int(item["final_price"])*item["tedad"]
            yield item          #آیتم را برگردان

    def calc_tutal_price(self):
        sum=0
        for item in self.shop_cart.values():
            sum+=int(item['final_price'])*item['tedad']
        return sum
    