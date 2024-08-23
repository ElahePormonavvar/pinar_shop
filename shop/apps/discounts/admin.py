from django.contrib import admin
from .models import Coupon,DiscountBasket,DiscountBasketDetails


@admin.register(Coupon)
class CouponsAdmin(admin.ModelAdmin):
    list_display=['coupon_code','start_date','end_date','discount','is_active',]
    ordering=['is_active']


class DiscountBasketDetailsInLine(admin.TabularInline):
    model=DiscountBasketDetails


@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display=['discount_title','start_date','end_date','discount','is_active',]
    ordering=['is_active',]
    inlines=[DiscountBasketDetailsInLine,]


