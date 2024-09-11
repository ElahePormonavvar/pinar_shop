from django.urls import path
from . import views
app_name="products"
urlpatterns = [
    path('chepest_products/',views.get_chepest_products,name='chepest_products'),
    path('last_products/',views.get_last_products,name='last_products'),
    path('popular_products_group/',views.get_popular_products_group,name='popular_products_group'),
    path('product_details/<slug:slug>/',views.ProductDetailsView.as_view(),name='product_details'),
    path('related_products/<slug:slug>/',views.get_related_products,name='related_products'),
    path('product_groups/',views.ProductsGroupsView.as_view(),name='product_groups'),
    path('products_of_group/<slug:slug>/',views.ProductByGroupsView.as_view(),name='products_of_group'),
    path('ajax_admin/',views.get_filter_value_for_feature,name='filter_value_for_feature'),
    path('products_groups_partials',views.get_product_groups,name='products_groups_partials'),
    path('brands_partials/<slug:slug>/',views.get_brands,name='brands_partials'),
    path('feature_partials/<slug:slug>/',views.get_feature_for_filter,name='feature_partials'),
    path('compare_table/',views.compare_table,name='compare_table'),
    path('product_compare/',views.ShowCompareListView.as_view(),name='product_compare'),
    path('add_to_compare_list/',views.add_to_compare_list,name='add_to_compare_list'),
    path('delete_from_compare_list/',views.delete_from_compare_list,name='delete_from_compare_list'),
    path('statuse_of_compare_list/',views.statuse_of_compare_list,name='statuse_of_compare_list'),
    path('category/<slug:slug>/',views.ProductListView.as_view(),name='category'),
    path('product_navigation/',views.product_navigation,name='product_navigation'),
    path('get_new_products/',views.get_new_products,name='get_new_products'),

 
]