from django.contrib import admin
from scraping.models import AlarmStock, Stock

admin.site.register(Stock)
admin.site.register(AlarmStock)
# Register your models here.
