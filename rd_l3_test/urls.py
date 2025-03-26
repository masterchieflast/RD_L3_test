from django.contrib import admin
from django.urls import path, include
from network import views as network_views
urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/', include('network.urls')),
]
