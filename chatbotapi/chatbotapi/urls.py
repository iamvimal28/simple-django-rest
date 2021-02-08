from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('controller/',include('controller.urls')),
    path('admin/', admin.site.urls),
]
