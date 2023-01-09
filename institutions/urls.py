from django.urls import path
from . import views


urlpatterns = [
    path("institutions/", views.InstitutionView.as_view()),
    path("institutions/<str:pk>/", views.InstitutionDetailView.as_view())
]
