from django.contrib import admin
from .models import Warehous,WarehouseType

# --------------------------------------------------
@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display=['id','warehouse_type_title']

# --------------------------------------------------
@admin.register(Warehous)
class WarehousAdmin(admin.ModelAdmin):
    list_display=['product','price','tedad','warehouse_type','register_date']