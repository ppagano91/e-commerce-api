from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.products.api.serializers.product_serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]    # Para que solo los usuarios autenticados puedan acceder a los productos
    
    def get_queryset(self, pk=None):
        if pk == None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
    
    def list(self, request):
        product_queryset = self.get_queryset()
        product_serializer = self.get_serializer(product_queryset, many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Producto agregado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            product_serializer = self.serializer_class(product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":f"No existe un producto con id {pk}"}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            product.state = False
            product.save()
            return Response({"message":"Producto eliminado correctamente"}, status=status.HTTP_200_OK)
        return Response({"message":f"No existe un producto con id {pk}"}, status=status.HTTP_400_BAD_REQUEST)