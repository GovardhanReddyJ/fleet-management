"""
URL configuration for fleet_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from app import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'vehicle_cat', views.VehicleCategoryViewSet,basename='vehicle_cat')
router.register(r'all_vehicle', views.AllocateVehicleViewSet,basename='all_vehicle')
router.register(r'available', views.AvailableVehiclesViewSet,basename='available')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # path('available/', views.AvailableVehiclesAPIView.as_view(), name='available-vehicles'),
    # path('all_vehicle/', views.AllocateVehicleAPIView.as_view(), name='allocate-vehicle'),
    # path('all_vehicle/', views.AllocateVehicleViewSet.as_view(), name='allocate-vehicle'),
    # path('all_vehicle/<int:pk>', views.AllocateVehicleAPIView.as_view(), name='allocate-vehicle'),
    path('register_vehicle/', views.RegisterVehicleAPIView.as_view(), name='register-vehicle'),
    path('register_vehicle/<int:pk>', views.RegisterVehicleAPIView.as_view(), name='register-vehicle'),
    #payment paths
    path('pay/', views.start_payment, name="payment"),
    path('payment/success/', views.handle_payment_success, name="payment_success")
]

