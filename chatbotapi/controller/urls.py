from django.urls import path
from controller import views

urlpatterns = [
    path('handlerequest',views.handler)
]