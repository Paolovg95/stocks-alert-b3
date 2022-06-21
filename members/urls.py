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
