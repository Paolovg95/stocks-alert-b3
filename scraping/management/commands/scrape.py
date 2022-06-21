from django.core.management.base import BaseCommand

import requests
from bs4 import BeautifulSoup
from scraping.models import Stock

class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    def handle(self, *args, **options):
        # collect html
        url = "https://br.investing.com/equities/brazil"
        headers= {
            "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
            "Accept-language": "en",
        }
        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, "lxml")

        table = soup.find('table', id="cross_rate_markets_stocks_1")
        rows = table.find("tbody").find_all("tr")

        for row in rows:

            id = row['id'].strip("pair_")
            detailed_url = row.find("td",class_="plusIconTd").a['href']
            name = row.find("td",class_="plusIconTd").a.text
            high = row.find("td",class_=f"pid-{id}-high").text
            low = row.find("td",class_=f"pid-{id}-low").text
            ultimo = row.find("td",class_=f"pid-{id}-last").text
            ultimo = row.find("td",class_=f"pid-{id}-last").text
            var = row.find("td",class_=f"pid-{id}-pc").text
            var_percentage = row.find("td",class_=f"pid-{id}-pcp").text


            try:
                 # Try to get the title of the Stock
                stock = Stock.objects.get(title=name)
                stock_updated = Stock.objects.get(id=stock.id)

                # If it's found, then update the Stock Fields.
                stock_updated.url = detailed_url
                # Convert String Scraped to Float
                stock_updated.price = float(ultimo.replace(",","."))
                stock_updated.max = float(high.replace(",","."))
                stock_updated.min = float(low.replace(",","."))
                stock_updated.variance = var
                stock_updated.variance_percentage = var_percentage
                stock_updated.save()

                print('%s Updated' % (name,))
            except:
                # If does not exists, then create a New Instance
                Stock.objects.create(
                    url = detailed_url,
                    title = name,
                    max = float(high.replace(",",".")), # Convert to Float
                    min = float(low.replace(",",".")),
                    price = float(ultimo.replace(",",".")),
                    variance = var,
                    variance_percentage = var_percentage
                )
                print('%s Created' % (name,))
        self.stdout.write( 'job complete' )
