from rest_framework import generics
from apps.products.models import MeasureUnit, Category, Indicator
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, CategorySerializer, IndicatorSerializer

class MeasureUnitListAPIView(generics.ListAPIView):    
    serializer_class = MeasureUnitSerializer

    def get_queryset(self):
        return MeasureUnit.objects.filter(state=True)
    
    
class CategoryListAPIView(generics.ListAPIView):    
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(state=True)
    

class IndicatorListAPIView(generics.ListAPIView):
    serializer_class = IndicatorSerializer

    def get_queryset(self):
        return Indicator.objects.filter(state=True)
