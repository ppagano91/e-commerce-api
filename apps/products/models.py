from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel

# Create your models here.
class MeasureUnit(BaseModel):
    description = models.TextField('Descripción', max_length=100, blank=False, null=False, unique=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        return self.description
    
class Category(BaseModel):
    description = models.TextField('Descripción', max_length=100, blank=False, null=False, unique=True)    
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Producto'

    def __str__(self):
        return self.description


class Indicator(BaseModel):
    descount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Indicador de Oferta')
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Indicador de Oferta'
        verbose_name_plural = 'Indicadores de Ofertas'

    def __str__(self):
        return f"Oferta de la categoría {self.category_product}: {self.descount_value}%"
    

class Product(BaseModel):
    name = models.CharField('Nombre de Producto', max_length=100, blank=False, null=False, unique=True)
    description = models.TextField('Descripción de Producto', max_length=200, blank=False, null=False)
    image = models.ImageField('Imagen del Producto', upload_to='products/', blank=True, null=True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, verbose_name='Unidad de Medida', null=True)
    category_product = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría de Producto', null=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name