from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MeasureUnit)
admin.site.register(Category)
admin.site.register(Indicator)
admin.site.register(Product)