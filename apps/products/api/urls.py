from django.urls import path
from apps.products.api.views.general_views import MeasureUnitListAPIView, CategoryListAPIView, IndicatorListAPIView
from apps.products.api.views.products_views import ProductListAPIView, ProductCreateAPIView

urlpatterns = [
    path('measure_unit/', MeasureUnitListAPIView.as_view(), name='measure-unit-list'),
    path('category_product/', CategoryListAPIView.as_view(), name='category-product-list'),
    path('indicator/', IndicatorListAPIView.as_view(), name='indicator-list'),
    path('product/list/', ProductListAPIView.as_view(), name='product-list'),
    path('product/create/', ProductCreateAPIView.as_view(), name='product-create'),

]