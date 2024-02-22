from django.contrib import admin
from .models import *

# Register your models here.
class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')

admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Indicator)
admin.site.register(Product)