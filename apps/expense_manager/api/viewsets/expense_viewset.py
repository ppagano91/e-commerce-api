from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.expense_manager.models import Supplier
from apps.expense_manager.api.serializers.general_serializer import SupplierSerializer

from apps.expense_manager.api.serializers.expense_serializer import *

class ExpenseViewSet(viewsets.GenericViewSet):
    serializer_class = ExpenseSerializer

    @action(methods=["get"], detail=False)  # url_path="search_supplier"
    def search_supplier(self, request):
        ruc_or_business_name = request.query_params.get("ruc_or_business_name","")

        supplier = Supplier.objects.filter(
            Q(ruc__iexact=ruc_or_business_name)|Q(business_name__iexact=ruc_or_business_name)
        ).first()

        if supplier != None:
            supplier_serializer = SupplierSerializer(supplier)

            return Response(supplier_serializer.data, status=status.HTTP_200_OK)
        
        return Response({"mensaje":"No se ha encontrado un proveedor"},status=status.HTTP_400_BAD_REQUEST)