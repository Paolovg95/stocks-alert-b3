from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from scraping.models import AlarmStock, Stock
import requests
from bs4 import BeautifulSoup
from .forms import AlertStockForm

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

# MY ALARMS
def my_alarms(request):
    user = request.user
    queryset = AlarmStock.objects.filter(user=user)
    context = {
        'object_list': queryset
    }

    return render(request, "authenticate/my_alarms.html", context)

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

def delete_alarm(request, id=id):
    obj = get_object_or_404(AlarmStock, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect('my-alarms')

    context = {
        'object': obj
    }
    return render(request, "authenticate/delete_alarm.html", context)

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
