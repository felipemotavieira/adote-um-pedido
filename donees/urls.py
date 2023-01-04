from django.urls import path
from . import views

urlpatterns = [
    path("donee/", views.doneeView.as_view()),
    path("donee/<str:pk>/", views.doneeDetailView.as_view()),
]
