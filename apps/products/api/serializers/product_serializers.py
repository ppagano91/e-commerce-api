from apps.products.models import Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    # Esto llama al método str de las clases relacionadas
    # measure_unit = serializers.StringRelatedField()
    # category_product = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ('state','created_date','modified_date','deleted_date')

    def validate_measure_unit(self, value):
        if value == "" or value == None:
            raise serializers.ValidationError("Debe ingresar una Unidad de Medida")
        return value
    
    def validate_category_product(self, value):
        if value == "" or value == None:
            raise serializers.ValidationError("Debe ingresar una Categoría de Producto")
        return value

    def validate(self,data):
        if "measure_unit" not in data.keys():
            raise serializers.ValidationError({"measure_unit":"Debe ingresar una Unidad de Medida"})
        
        if "category_product" not in data.keys():
            raise serializers.ValidationError({"category_product":"Debe ingresar una Categoría de Producto"})
        
        return data

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['measure_unit'] = instance.measure_unit.description if instance.measure_unit != None else ''
        data['category_product'] = instance.category_product.description if instance.category_product != None else ''
        data['image'] = instance.image.url if instance.image != '' else ''
        return data