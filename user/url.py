from django.urls import path
from user.views import *

app_name = 'user'

urlpatterns = [
    path('list/', UsersListView.as_view(), name = 'user_list'),
]