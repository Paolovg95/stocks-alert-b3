# stock-alert-b3

The purpose of this Project is to assist an investor in his decisions to buy/sell assets. To this end, he must periodically record the current price of B3's assets and also notify, via email, if there is a trading opportunity.

The First Step to develop this Project is to define from where to get our necessary information, so the proper Web scraping can be don effectively. 

investing.com was our best option to consultation of stored prices, Save to DB, configure the assets to be monitored and parameterize the price tunnels for each asset and check frequency for each asset. 


    class Stock(models.Model):
    
    url = models.CharField(max_length=100,unique=True,null=True)
    title = models.CharField(max_length=250, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=303)
    max = models.DecimalField(decimal_places=2, max_digits=30)
    min = models.DecimalField(decimal_places=2, max_digits=30)
    variance = models.CharField(max_length=20)
    variance_percentage = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
    class Admin:
        pass
        
        
This is what we’ll automatically schedule at the infrastructure level in order to automate Web Scraping using BeautifulSoup4, preventing the duplicates and automatically update the Data if there are any changes calling:

python manage.py scrape


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
                stock = Stock.objects.get(title=name)
                stock_updated = Stock.objects.get(id=stock.id)
                stock_updated.url = detailed_url
                stock_updated.price = float(ultimo.replace(",","."))
                stock_updated.max = float(high.replace(",","."))
                stock_updated.min = float(low.replace(",","."))
                stock_updated.variance = var
                stock_updated.variance_percentage = var_percentage
                stock_updated.save()

                print('%s Updated' % (name,))
            except:
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
        



<img width="1100" alt="Screen Shot 2022-06-06 at 8 50 22 PM" src="https://user-images.githubusercontent.com/106985050/172272722-6db8a1f3-b449-47a9-af65-84cf5a3945ae.png">


For our User Login and Registration, Django comes with a pretty nice user authentication system that we'll use for all of this. 
Add Members App,  Add URLS.py file to Members App with Paths, Add Templates to Members App where we are going to add all the views corresponding to the Logged In Members.

    from django.urls import path
    from .views import (
        delete_alarm,
        login_user,
        logout_user,
        register_user,
        my_alarms,
        create_alarm,
        update_alarm,
        delete_alarm,
        stock_detailed,
    )

    urlpatterns = [
        path('login_user', login_user, name="login"),
        path('logout_user', logout_user, name='logout'),
        path('register_user', register_user, name="register_user"),
        path('my_alarms', my_alarms, name="my-alarms"),
        path('create_alarm', create_alarm, name="create-alarm"),
        path('update_alarm/<str:id>', update_alarm, name="update-alarm"),
        path('delete_alarm/<str:id>', delete_alarm, name="delete-alarm"),
        path('stock_detailed/<str:id>', stock_detailed, name="stock-detailed"),

    ]
    
 
 
   <img width="250" alt="Screen Shot 2022-06-06 at 8 53 02 PM" src="https://user-images.githubusercontent.com/106985050/172273013-91c60ec6-b43f-4a47-a102-be2a81bfb82a.png">


    from django.contrib import admin
    from django.urls import path, include
    from pages.views import home_view


    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', home_view, name="home"),
        path('members/', include('django.contrib.auth.urls')),
        path('members/', include('members.urls')),
    ]
    
    
   
We create first the Login Page HTML. Making it simple and easy for users to Login. Added Bootstrap and Messages for alerts.

    {% extends 'base.html' %}

    {% block content %}
    <a href="{% url 'home' %}">Back to Home</a></button>

    <div class="m-5">
        <h1>Login Page</h1>
        <form method="POST">
          {% csrf_token %}
          <div class="form-group p-3">
            <label for="exampleInputEmail1">Username</label>
            <input type="text" class="form-control" name="username" aria-describedby="emailHelp"
              placeholder="Enter email">
           </div>
          <div class="form-group p-3">
            <label for="exampleInputPassword1">Password</label>
            <input type="password" class="form-control" name="password" placeholder="Password">
          </div>
          <div class="form-check p-3">
            <input type="checkbox" class="form-check-input" id="exampleCheck1">
            <label class="form-check-label" for="exampleCheck1">Check me out</label>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    {% endblock %}
    
   <img width="1440" alt="Screen Shot 2022-06-06 at 10 06 08 AM" src="https://user-images.githubusercontent.com/106985050/172273209-65638482-a25f-4502-808f-07166e60ca82.png">

  
    # USER LOGIN
    def login_user(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request,'There was an error Login in, try again.')
                return redirect('login')
        else:
            return render(request,'authenticate/login.html', {})

    # USER LOGOUT
    def logout_user(request):

        logout(request)
        messages.success(request,'You were Logged out!')
        return redirect('home')

For the Registration we Import UserCreationForms and we follow the same step process for the registration, taking in consideration all the requirements in our register_user on views.py.![image](https://user-images.githubusercontent.com/106985050/172273297-534c7507-b33c-459f-bd71-969c62cece8c.png)

      {% extends 'base.html' %}

    {% block content %}
    <a href="{% url 'home' %}">Back to Home</a></button>
    <div class="m-5">
      {% if form.errors %}
        <p>There was an error with the form</p>
      {% endif %}
      <h1>Register Page</h1>
      <form action="{% url 'register_user' %}" method=POST>
        {% csrf_token %}
        {{ form.as_p }}
        <!-- Bootstrap -->
        <!-- <div class="form-group p-3">
          <label for="exampleInputEmail1">Username</label>
          <input type="text" class="form-control" name="username" aria-describedby="emailHelp" placeholder="Enter email">
        </div>
        <div class="form-group p-3">
          <label for="exampleInputPassword1">Password</label>
          <input type="password" class="form-control" name="password" placeholder="Password">
        </div>
        <div class="form-group p-3">
          <label for="exampleInputPassword1">ConfirmPassword</label>
          <input type="password" class="form-control" name="password" placeholder="Password">
        </div>
        <div class="form-check p-3">
          <input type="checkbox" class="form-check-input" id="exampleCheck1">
          <label class="form-check-label" for="exampleCheck1">Check me out</label>
        </div> -->
        <button type="submit" class="btn btn-primary">Submit</button>
        <br></br>

      </form>
    </div>

    {% endblock %}
    
    # USER REGISTRATION
    def register_user(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(request, username=username, password=password)
                login(request, user)
                messages.success(request,'Registration successful!')
                return redirect('home')
        else:
            form = UserCreationForm()

    return render(request, 'authenticate/register_user.html', { 'form': form  })

In our Home Views the Scraping results are displayed with All the Details from: Last Price, Max, Min, Variation, Var Per centavo and the Date Created (will update every time this tsk is automated).

Displaying a small ‘Dashboard like’ for logged in users, with the Profile Info and the user’s current Alerts.

<img width="1420" alt="Screen Shot 2022-06-06 at 10 00 17 AM" src="https://user-images.githubusercontent.com/106985050/172273516-08c09ade-28da-4b39-8f1c-f5337bfa50d6.png">


There is also, a link to go into a Detailed Page to visualize the Daily Activity for the selected Stock. With all its main fields being displayed for the user to have better visualization.

For this, a second Web Scraping process is done inside our Views.py, where we collect the data for the daily activity from the stock. The scraping is updated every time the user goes back to this page.

<img width="1387" alt="Screen Shot 2022-06-06 at 10 04 06 AM" src="https://user-images.githubusercontent.com/106985050/172273705-bb4c5a75-6824-4557-90d6-8d923bb5fcea.png">


    def stock_detailed(request, id=id):

    obj = get_object_or_404(Stock,id=id)
    url_title = obj.title.lower()
    url_title = url_title.replace(" ", "-")

    url = f"https://br.investing.com{obj.url}-historical-data"
    headers= {
            "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
            "Accept-language": "en",
        }
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    table = soup.find('table', id="curr_table")
    rows = table.find('tbody').find_all("tr")

    history_data = []

    for row in rows:
        data = row.find(class_="noWrap")
        ultimo = data.find_next("td")
        abertura = ultimo.find_next("td")
        max = abertura.find_next("td")
        min = max.find_next("td")

        history_data.append(
            {
                'data': data.text,
                'ultimo': ultimo.text,
                'abertura': abertura.text,
                'max': max.text,
                'min': min.text
            }
        )
    context = {
        'object': obj,
        'history': history_data
    }
    return render(request, "authenticate/stock_detailed.html", context)



The project aims to make the user’s journey effective and simple, suggesting Buy whenever the price of a monitored asset crosses its lower limit, and suggesting Sell whenever the price of a monitored asset crosses its upper limit.

For that, AlarmStock Model is Added. 


    class AlarmStock(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
        buying_at = models.DecimalField(decimal_places=2, max_digits=5)
        selling_at = models.DecimalField(decimal_places=2, max_digits=5)
        status = models.CharField(max_length=20,null=True)
        updated_at = models.DateTimeField(auto_now=True,null=True)
        created_at = models.DateTimeField(auto_now_add=True,null=True)

        def __str__(self):
            return self.stock.title

A very simple CRUD(Create, Read, Update, Delete) processes to create Alarms for the user.

    # READ
    def my_alarms(request):
        user = request.user
        queryset = AlarmStock.objects.filter(user=user)
        context = {
            'object_list': queryset
        }




        return render(request, "authenticate/my_alarms.html", context)
    # CREATE
    def create_alarm(request):
        form = AlertStockForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                alarm = form.save(commit=False)
                alarm.user = request.user
                alarm.status = "Pending"
                alarm.save()
                return redirect('my-alarms')
        else:
            form = AlertStockForm()

        context = {
            'form': form
        }
        return render(request, "authenticate/create_alarm.html", context)
    # UPDATE
    def update_alarm(request, id=id):
        obj = get_object_or_404(AlarmStock, id=id)
        form = AlertStockForm(request.POST or None, instance=obj)

        if form.is_valid():
            alarm = form.save(commit=False)
            alarm.user = request.user
            alarm.save()
            return redirect('my-alarms')
        else:
            form = AlertStockForm()

        context = {
            'form': form
        }

        return render(request, "authenticate/create_alarm.html", context)
    # DELETE
    def delete_alarm(request, id=id):
        obj = get_object_or_404(AlarmStock, id=id)

        if request.method == 'POST':
            obj.delete()
            return redirect('my-alarms')

        context = {
            'object': obj
        }
        return render(request, "authenticate/delete_alarm.html", context)
        
        
 There is a detailed view for the User’s Alerts. We get Access to the Edit and Delete Actions.![image](https://user-images.githubusercontent.com/106985050/172273959-c54995f9-6f78-44f0-ab88-fbb5c905cd58.png)

<img width="1301" alt="Screen Shot 2022-06-06 at 10 00 28 AM" src="https://user-images.githubusercontent.com/106985050/172273974-7364d29d-0700-4897-8ad9-48759533c361.png">

On settings.py
To make the Email Notification Successfully, firstly, I needed to make some configuration in my Gmail Account, adding a 2F Authentication to Allow our Django App logi to send the email alert. Secondly, the .env files setup and installation. To use environmental variables we installed:

pip install django-environ

Adding at the beggining of the Module, making it available for settings.

.env file contains all the Key-value pairs to use it then in our Cron.py file where we will compare the current Stock Price with ours every 30min.


.env

    EMAIL_HOST_USER=paolo@email.com
    EMAIL_HOST_PASSWORD='password'
    RECIPIENT_ADDRESS=paolo9517@gmail.com ## Testing purpose


settings.py


    import os
    import environ

    env = environ.Env()
    environ.Env.read_env()

    # CRON TIME LIMIT SPECIFIC
    # CURRENTLY 1 MINUTE, AVAILABLE FOR MODIFICATION
    CRONJOBS = [
        ('*/30 * * * *', 'scraping.cron.my_scheduled_job') ## Check and send alerts every 30min
    ]

    # Application definition
    # EMAIL CONFIGURATIONS
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    RECIPIENT_ADDRESS = env('RECIPIENT_ADDRESS')


To Automate the Email notification process, Crontab is the tool we choose, lets you run Django/Python code on a recurring basis proving basic plumbing to track and execute tasks. The two most common ways in which most people go about this is either writing custom python scripts or a management command per cron.py.

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


Email Notification Every 1 MINUTE for a Buying opportunity. Set every 1 MINUTE for Testing Purposes.


<img width="1063" alt="Screen Shot 2022-06-11 at 2 24 00 AM" src="https://user-images.githubusercontent.com/26658714/173176234-e8e1d25f-bc4e-4f5c-9bdb-d64e6d2c94c7.png">

Status Updated Automatically every time an Alert is Sent. Buying or Selling Opportunity

<img width="1424" alt="Screen Shot 2022-06-11 at 2 30 56 AM 1" src="https://user-images.githubusercontent.com/26658714/173176335-2df07d41-4de0-4967-8aa4-5d005765739c.png">

       {% if item.status == "BUY" %}
        <td><strong class="font-weight-bold text-success" >{{ item.status }}</strong></td>
      {% elif item.status == "SELL" %}
        <td><strong class="font-weight-bold text-warning" >{{ item.status }}</strong></td>
      {% else %}
        <td><strong>{{ item.status }}</strong></td>
      {% endif %}

Finally for deploying, the project supports Heroku cloud platform as a service.
To prevent deploying unnecessary files.
These was added to gitignore file.

      .DS_Store
      assets/__pycache__
      scraping/__pycache__
      
 To boot up a web dyno, and to migrate the db, Profile was added to our Root folder.
 
     web: gunicorn jobs.wsgi
    release: python manage.py migrate



<img width="1243" alt="Screen Shot 2022-06-06 at 7 54 20 PM" src="https://user-images.githubusercontent.com/106985050/172274519-667e97dc-a5fa-4313-b28e-766f126ac559.png">

<img width="395" alt="Screen Shot 2022-06-06 at 7 55 22 PM" src="https://user-images.githubusercontent.com/106985050/172274578-1d57ecf4-3c7c-414c-b9a2-293c1d9258fc.png">

After pushing to Heroku, in Resource Tab of the main view, I looked for Heroku Scheduler to schedule our main Web Scraping process every 1 hour everyday. Keeping the latest data from Investing.com coming in.





