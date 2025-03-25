from django.urls import path, include
from login.views import *

urlpatterns = [
    path('', LoginFormView1.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),

]