from .models import Stock
import smtplib
from email.message import EmailMessage


def my_scheduled_job():


    # url = "https://stocks-price-alert-b3.herokuapp.com/"
    # email = EmailMessage()
    # email['from'] = 'Python <vargasdegasperi@orastudio.tech>'
    # email['to'] = 'paolo9517@gmail.com'
    # email['subject'] = 'Stock Alert'

    # email.set_content('New Opportunity {}'.format(url))

    # with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    #     smtp.ehlo()
    #     smtp.starttls()
    #     smtp.ehlo()

    #     smtp.login('vargasdegasperi@orastudio.tech', 'password')
    #     smtp.send_message(email)
