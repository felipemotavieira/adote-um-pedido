from django.urls import path

from . import views

urlpatterns = [
    path("pix_donation/", views.PixDonationView.as_view()),
]