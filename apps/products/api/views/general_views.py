from rest_framework import viewsets
from rest_framework.response import Response

from apps.products.models import MeasureUnit
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, CategorySerializer, IndicatorSerializer

class MeasureUnitViewSet(viewsets.GenericViewSet):
    """
    A simple ViewSet for viewing and editing MeasureUnit instances.        
    """
    model = MeasureUnit
    serializer_class = MeasureUnitSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
    def list(self):
        """
        A simple ViewSet for viewing and editing Measure Unit instances.

        This view should return a list of all the MeasureUnit instances
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
class CategoryViewSet(viewsets.ModelViewSet):
    """    
    A simple ViewSet for viewing and editing Category instances.
    """
    serializer_class = CategorySerializer

class IndicatorViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Indicator instances.
    """
    serializer_class = IndicatorSerializer