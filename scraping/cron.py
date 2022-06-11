from .models import Stock, AlarmStock
from django.conf import settings
from django.core.mail import send_mail

def my_scheduled_job():

    stocks = Stock.objects.all()
    alarms = AlarmStock.objects.all()

    for alarm in alarms:
        for stock in stocks:
            if alarm.stock.id == stock.id:
                if alarm.buying_at >= stock.price:
                    send_mail(
                        subject="Stock Alert - Buying Opportunity",
                        message=f"Buying Opportunity for {alarm.stock.title} - Buying at: {alarm.buying_at} Current Price at: {stock.price}",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[settings.RECIPIENT_ADDRESS]
                        # Recipient can be modified for 'alarm.user.email'
                    )
                    alarm.status = "BUY"
                elif alarm.selling_at <= stock.price:
                    send_mail(
                        subject="Stock Alert - Selling Opportunity",
                        message=f"Selling Opportunity for {alarm.stock.title} - Selling at: {alarm.selling_at} Current Price at {stock.price}",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[settings.RECIPIENT_ADDRESS]
                    )
                    alarm.status = "SELL"
                else:
                    alarm.status = "Pending"

                alarm.save()
