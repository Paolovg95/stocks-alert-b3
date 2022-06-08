from urllib import request
from django import forms
from django.forms import ModelForm
from scraping.models import AlarmStock,Stock
from django.contrib.auth.models import User


class AlertStockForm(ModelForm):
    class Meta:
        model = AlarmStock
        exclude = ['user', 'status']
