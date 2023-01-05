from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views


urlpatterns = [
    path("address/", views.AddressView.as_view()),
    path("address/<str:address_id>/", views.AddressDetailView.as_view()),
]
