from django import forms
from django_jalali.admin.widgets import AdminjDateWidget
from .models import Product

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'register_date': AdminjDateWidget(),
            'published_date': AdminjDateWidget(),
            'update_date': AdminjDateWidget(),
        }