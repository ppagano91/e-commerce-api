from django.urls import path
from apps.products.api.views.general_views import MeasureUnitListAPIView, CategoryListAPIView, IndicatorListAPIView
from apps.products.api.views.products_views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyApiView

urlpatterns = [
    path('measure_unit/', MeasureUnitListAPIView.as_view(), name='measure-unit-list'),
    path('category_product/', CategoryListAPIView.as_view(), name='category-product-list'),
    path('indicator/', IndicatorListAPIView.as_view(), name='indicator-list'),    
    path('product/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('product/retrieve/<int:pk>/', ProductRetrieveUpdateDestroyApiView.as_view(), name='product-retrieve-update-destroy'),
]