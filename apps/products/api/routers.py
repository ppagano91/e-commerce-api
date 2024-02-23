from rest_framework.routers import DefaultRouter
from apps.products.api.views.products_viewsets import ProductViewSet
from apps.products.api.views.general_views import MeasureUnitViewSet, CategoryViewSet, IndicatorViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'measure_unit', MeasureUnitViewSet, basename='measure-unit')
router.register(r'category_product', CategoryViewSet, basename='category-product')
router.register(r'indicator', IndicatorViewSet, basename='indicator')

urlpatterns = router.urls