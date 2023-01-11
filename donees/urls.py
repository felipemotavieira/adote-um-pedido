from django.urls import path
from . import views

urlpatterns = [
    path("donees/", views.doneeView.as_view()),
    path("donees/<str:pk>/", views.doneeDetailView.as_view())
]
