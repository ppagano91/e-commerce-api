from apps.base.api import GeneralListApiView
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, CategorySerializer, IndicatorSerializer

class MeasureUnitListAPIView(GeneralListApiView):
    serializer_class = MeasureUnitSerializer    
    
class CategoryListAPIView(GeneralListApiView):    
    serializer_class = CategorySerializer

class IndicatorListAPIView(GeneralListApiView):
    serializer_class = IndicatorSerializer