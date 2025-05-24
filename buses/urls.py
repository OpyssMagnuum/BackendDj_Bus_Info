"""
URL configuration for buses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from main import views
from main.views import BusViewSet, RouteViewSet, LRNViewSet

r = DefaultRouter()
r.register('buses', BusViewSet)
r.register('routes', RouteViewSet)
r.register('long_route_names', LRNViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('route/<str:route_number>/stops/<int:stop_count>/reverse/<int:reverse>', views.route_stops_form, name='route_stops_form'),
    # добавьте также путь для обработки формы
    path('save-route-stops/', views.save_route_stops, name='save_route_stops'),
    path('route/<str:route_id>/', views.route_detail, name='route_detail'),
] + r.urls
