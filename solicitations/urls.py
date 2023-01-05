from django.urls import path
from .views import SolicitationView,SolicitationDetailView


urlpatterns = [
    path("solicitations/<str:pk>/", SolicitationView.as_view()),
    path("solicitations/<str:pk>/", SolicitationDetailView.as_view())
]
