from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from apps.products.models import Product

class Supplier(BaseModel):
    ruc = models.CharField(unique=True, max_length=11)
    business_name = models.CharField('Razón Social', unique=True, max_length=150, null=False, blank=False)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['id']
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'   

    def __str__(self):
        return self.business_name

    def to_dict(self):
        return {
            'id': self.id,
            'ruc': self.ruc,
            'business_name': self.business_name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }

class Provider(BaseModel):
    ruc = models.CharField(unique=True, max_length=11)
    business_name = models.CharField('Razón Social',max_length=150, null=False, blank=False)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True)
    historical = HistoricalRecords()

    class Meta:
        ordering = ['id']
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'   

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    def __str__(self):
        return self.business_name

class PaymentType(BaseModel):
    name = models.CharField('Nombre de Medio de Pago', max_length = 100)
    historical = HistoricalRecords()

    class Meta:
        ordering = ['id']
        verbose_name = 'Medio de Pago'
        verbose_name_plural = 'Medio de Pagos'

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    def __str__(self):
        return self.name


class Voucher(BaseModel):
    name = models.CharField('Nombre de comprobante de Pago', max_length = 100)
    historical = HistoricalRecords()

    class Meta:
        ordering = ['id']
        verbose_name = 'Comprobante'
        verbose_name_plural = 'Comprobantes'

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    def __str__(self):
        return self.name


class ExpenseCategory(BaseModel):
    name = models.CharField('Nombre de Categoría de Gasto', max_length = 100)
    historical = HistoricalRecords()

    class Meta:
        ordering = ['id']
        verbose_name = 'Categoria de Gasto'
        verbose_name_plural = 'Categorias de Gastos'

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    def __str__(self):
        return self.name

class Expense(BaseModel):
    date = models.DateField(
        'Fecha de emisión de factura', auto_now=False, auto_now_add=False)    
    date = models.DateField('Fecha de emisión de factura', auto_now=False, auto_now_add=False)    
    quantity = models.DecimalField('Cantidad', max_digits=10, decimal_places=2)
    unit_price = models.DecimalField('Precio Unitario', max_digits=10, decimal_places=2, default=0)
    voucher_number = models.CharField('Número de comprobante', max_length=50)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    historical = HistoricalRecords()

    class Meta:
        ordering = ['id']
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value

    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        try:
            product = Product.objects.get(id=self.concepto.id)
            product.quantity += self.quantity
            product.save()
        except ObjectDoesNotExist as e:
            print("Producto No Registrado!")

        if self.unit_price == 0:
            self.unit_price = (self.quantity / self.cantidad)
        if self.quantity == 0:
            self.quantity = (self.unit_price * self.cantidad)
        super(Expense, self).save(*args, **kwargs)


class Merma(BaseModel):
    date = models.DateField('Fecha de emisión de Merma', auto_now = False, auto_now_add = False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField('Cantidad', max_digits = 7, decimal_places = 2)
    money_loss = models.DecimalField('Dinero perdido', max_digits = 7, decimal_places = 2)
    historical = HistoricalRecords()

    class Meta:
        ordering = ['id']
        verbose_name = 'Merma'
        verbose_name_plural = 'Mermas'

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_date(self, value):
        self.changed_by = value


    def __str__(self):
        return "Merma de {0}".format(self.product.name)

    def save(self, *args, **kwargs):
        self.money_loss = self.product.cost_price * self.quantity
        super(Merma, self).save(*args, **kwargs)