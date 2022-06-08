from multiprocessing import context
from django.shortcuts import render
from scraping.models import Stock, AlarmStock

def home_view(request, *args, **kwargs):
    queryset = Stock.objects.all()

    if request.user.is_authenticated:
        user = request.user
        my_alarms = AlarmStock.objects.filter(user=user)
        enumerated_alarms = enumerate(my_alarms)
        context = {
            'object_list': queryset,
            'user_object_list': enumerated_alarms
        }
    else:
        context = {
            'object_list': queryset,
        }
    return render(request, "home.html", context)
