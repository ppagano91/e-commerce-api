from apps.products.models import MeasureUnit, Category, Indicator

from rest_framework import serializers

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        exclude = ('state','created_date','modfield_date','deleted_date')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('state','created_date','modfield_date','deleted_date')

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        exclude = ('state','created_date','modfield_date','deleted_date')