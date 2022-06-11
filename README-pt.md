# stock-alert-b3

O objetivo deste Projeto é auxiliar um investidor em suas decisões de compra/venda de ativos. Para tanto, ele deve 
registrar periodicamente o preço atual dos ativos da B3 e também notificar, por e-mail, se houver oportunidade de negociação.


O primeiro passo para desenvolver este projeto é definir de onde obter nossas informações necessárias, para que o web scraping adequado possa ser feito de forma eficaz.

A investing.com foi a minha melhor opção para consultar os preços armazenados, Salvar no BD, configurar os ativos a serem monitorados e parametrizar os túneis de preços para cada ativo e verificar a frequência de cada ativo.


    
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
 
 Isso é o que vamos agendar automaticamente no nível de infraestrutura para automatizar o Web Scraping usando BeautifulSoup4, evitando as duplicates e atualizando automaticamente os dados se houver alguma alteração chamando:
 
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


Para nosso login e registro de usuário, o Django vem com um sistema de autenticação de usuário muito bom que usaremos para tudo isso.
Adicione o aplicativo de membros, adicione o arquivo URLS.py ao aplicativo de membros com caminhos, adicione modelos ao aplicativo de membros, onde adicionaremos todas as visualizações correspondentes aos membros logados.


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
    
  Criamos primeiro o HTML da página de login. Tornando simples e fácil para os usuários fazerem login. Adicionado Bootstrap e Mensagens para alertas.
  
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
        
        
  Para o Registro importamos UserCreationForms e seguimos a mesma etapa do processo de registro, levando em consideração todos os requisitos em nosso register_user em views.py.
  
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
    
    
    
Em nossas visualizações iniciais, os resultados de Web Scraping são exibidos com todos os detalhes de: último preço, máximo, mínimo, variação, variation percentage e a data de criação (será atualizada toda vez que esta task for realizada, depois configuramos a frequency de atualizacao no Heroku).

Exibindo um pequeno 'Dashboard' para usuários logados, com as informações do perfil e os alertas atuais do usuário.


<img width="1420" alt="Screen Shot 2022-06-06 at 10 00 17 AM" src="https://user-images.githubusercontent.com/106985050/172273516-08c09ade-28da-4b39-8f1c-f5337bfa50d6.png">

Há também um link para entrar em uma página detalhada para visualizar a atividade diária para o estoque selecionado. Com todos os seus principais campos sendo exibidos para que o usuário tenha uma melhor visualização.

Para isso, um segundo processo de Web Scraping é feito dentro do nosso Views.py, onde coletamos os dados da atividade diária do Stock. A Web Scraping é atualizada toda vez que o usuário volta a esta página.


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





O projeto visa tornar a jornada do usuário efetiva e simples, sugerindo Compre sempre que o preço de um ativo monitorado ultrapassar seu limite inferior e sugerindo Vender sempre que o preço de um ativo monitorado ultrapassar seu limite superior.

Para isso, o modelo AlarmStock.

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
            
  Um processo CRUD (Create, Read, Update, Delete) muito simples para criar alarms para o usuário.
  
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
        
Uma vista detalhada dos Alertas do Usuário. Obtemos acesso às ações de edição e exclusão.

<img width="1301" alt="Screen Shot 2022-06-06 at 10 00 28 AM" src="https://user-images.githubusercontent.com/106985050/172273974-7364d29d-0700-4897-8ad9-48759533c361.png">

Em settings.py para fazer a notificação por e-mail com sucesso, primeiro precisei fazer algumas configurações na minha conta do Gmail, adicionando uma autenticação 2F para permitir que nosso aplicativo Django faz Login e enviei alerta por e-mail.  Segundo, a configuração e instalação dos arquivos .env.  para usar variáveis de ambiente e aplicativo Django login enviasse o alerta por e-mail instalamos:

           pip instalar django-environ

O arquivo .env contém todos os pares Key-Pair para usá-lo em nosso arquivo Cron.py, onde compararemos o preço atual da ação com o nosso a cada 30 minutos.

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


Para automatizar o processo de notificação por e-mail, o Crontab é a ferramenta que escolhemos, permite executar código Django/Python de forma recorrente para rastrear e executar tarefas.


    from .models import Stock, AlarmStock
        from django.core.mail import EmailMessage
        import requests
        from django.conf import settings

    def my_scheduled_job(request):
        user = request.user
        print(user)
        queryset = AlarmStock.objects.filter(user=user)
        stocks = Stock.objects.all()
        for stock in stocks:
            for alarm in queryset:
                if stock.id == alarm.stock.id:
                    user_email = user.email
                    if alarm.buying_at <= stock.price:
                        alarm.status = "Buying Opportunity"
                        EmailMessage(
                            'Alarm Stock Alert',
                            'Buying Opportunity',
                            settings.EMAIL_HOST_USER,
                            [user_email],
                        )
                    if alarm.selling_at >= stock.price:
                        alarm.status = "Selling Opportunity"
                        EmailMessage(
                            'Alarm Stock Alert',
                            'Selling Opportunity:',
                            settings.EMAIL_HOST_USER,
                            ['user.email'],
                        )
Notificação por e-mail a cada 1 MINUTO para uma oportunidade de compra. Defina a cada 1 MINUTO para fins de teste.

<img width="1063" alt="Screen Shot 2022-06-11 at 2 24 00 AM" src="https://user-images.githubusercontent.com/26658714/173176234-e8e1d25f-bc4e-4f5c-9bdb-d64e6d2c94c7.png">


Status Atualizado Automaticamente sempre que um Alerta é Enviado. Oportunidade de compra ou venda

<img width="1424" alt="Screen Shot 2022-06-11 at 2 30 56 AM 1" src="https://user-images.githubusercontent.com/26658714/173176335-2df07d41-4de0-4967-8aa4-5d005765739c.png">


Finalmente, para implantação, o projeto suporta a plataforma de Cloud Heroku.
Para evitar a implantação de arquivos desnecessários.
Estes foram adicionados ao arquivo gitignore.

     .DS_Store
      assets/__pycache__
      scraping/__pycache__
      
 
 Para inicializar um web dyno e migrar o banco de dados, o perfil foi adicionado à nossa Root file.

 
     web: gunicorn jobs.wsgi
    release: python manage.py migrate
    
 <img width="1243" alt="Screen Shot 2022-06-06 at 7 54 20 PM" src="https://user-images.githubusercontent.com/106985050/172274519-667e97dc-a5fa-4313-b28e-766f126ac559.png">

<img width="395" alt="Screen Shot 2022-06-06 at 7 55 22 PM" src="https://user-images.githubusercontent.com/106985050/172274578-1d57ecf4-3c7c-414c-b9a2-293c1d9258fc.png">


Depois de fazer o push para o Heroku, na guia Resource da visualização principal, procurei o Heroku Scheduler para agendar nosso principal processo de Web Scraping a cada 1 hora todos os dias. Mantendo os dados mais recentes do Investing.com chegando.
