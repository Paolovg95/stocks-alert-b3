from django.contrib.auth.models import User
from django.db import models

class Stock(models.Model):
    url = models.CharField(max_length=100,null=True)
    title = models.CharField(max_length=250, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=303)
    max = models.DecimalField(decimal_places=2, max_digits=30)
    min = models.DecimalField(decimal_places=2, max_digits=30)
    variance = models.CharField(max_length=20)
    variance_percentage = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True) # update the field every time the save method is called.
    created_at = models.DateTimeField(auto_now_add=True) # Set Timezone.now() only when the instance is created.

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

    class Admin:
        pass

class AlarmStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    buying_at = models.DecimalField(decimal_places=2, max_digits=5)
    selling_at = models.DecimalField(decimal_places=2, max_digits=5)
    status = models.CharField(max_length=20,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True) # Set Null if the alarm instance not created.
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.stock.title
