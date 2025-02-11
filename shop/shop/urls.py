
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("apps.main.urls",namespace="main")),
    path('accounts/',include("apps.accounts.urls",namespace="accounts")),
    path('products/',include("apps.products.urls",namespace="products")),
    path('orders/',include("apps.orders.urls",namespace="orders")),
    path('discounts/',include("apps.discounts.urls",namespace="discountss")),
    path('payments/',include("apps.payments.urls",namespace="payment")),
    path('warehouses/',include("apps.warehouses.urls",namespace="warehouses")),
    path('csf/',include("apps.comment_scoring_favorites.urls",namespace="csf")),
    path('search/',include("apps.search.urls",namespace="search")),
    # path('test_api/',include("apps.test_api.urls",namespace="test_api")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('blogs/',include("apps.blog.urls",namespace="blogs")),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# handler404='apps.main.views.handler404'

