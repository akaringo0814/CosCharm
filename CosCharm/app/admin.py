from django.contrib import admin

# Register your models here.
from .models import CosmeticMaster, MyCosmetic

admin.site.register(CosmeticMaster)
admin.site.register(MyCosmetic)
