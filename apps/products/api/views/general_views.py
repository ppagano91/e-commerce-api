from rest_framework import viewsets, status
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
    
    def get_authenticate_header(self, request):
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs["pk"], state=True)
    
    def list(self, request):
        """
        A simple ViewSet for viewing and editing Measure Unit instances.

        This view should return a list of all the MeasureUnit instances
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
class CategoryViewSet(viewsets.GenericViewSet):
    """    
    A simple ViewSet for viewing and editing Category instances.
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
    def get_authenticate_header(self, request):
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs["pk"], state=True)
    
    def list(self, request):
        """
        A simple ViewSet for viewing and editing Category instances.

        This view should return a list of all the Category instances
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """
        A simple ViewSet for viewing and editing Category instances.

        This view should return a list of all the Category instances
        """        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Categoría registrada correctamente'},status=status.HTTP_201_CREATED)
        return Response({'message':'','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """
        A simple ViewSet for viewing and editing Category instances.

        This view should return a list of all the Category instances
        """
        if self.get_object().exists():
            category = self.get_object().get()
            serializer = self.serializer_class(category,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Categoría actualizada correctamente'},status=status.HTTP_200_OK)
        return Response({'message':'','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        A simple ViewSet for viewing and editing Category instances.

        This view should return a list of all the Category instances
        """
        if self.get_object().exists():
            category = self.get_object().get()
            category.state = False
            category.save()
            return Response({'message':'Categoría eliminada correctamente'},status=status.HTTP_200_OK)
        return Response({'message':'La categoría no existe'},status=status.HTTP_400_BAD_REQUEST)

class IndicatorViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Indicator instances.
    """
    serializer_class = IndicatorSerializer