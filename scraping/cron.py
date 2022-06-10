from .models import Stock

def my_scheduled_job():
  name = "3R Petroleum ON"
  stock = Stock.objects.get(title=name)
  stock.price = 96
  stock.save()
  print(stock.price)
