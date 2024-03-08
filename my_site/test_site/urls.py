from django.urls import path
from .views import *

urlpatterns=[
path('',index.as_view()),
path('register/', RegisterView.as_view(),name="register"),
path('login/', LoginView.as_view(),name="login"),
path('account/',AccountView.as_view(), name='account'),
]