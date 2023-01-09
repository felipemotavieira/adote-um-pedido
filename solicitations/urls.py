from django.urls import path
from .views import SolicitationView, SolicitationDetailView, SolicitationAtributionView, SolicitationDropView


urlpatterns = [
    path("solicitations/", SolicitationView.as_view()),
    path("solicitations/<str:solicitation_id>/", SolicitationDetailView.as_view()),
    path("solicitations/<str:solicitation_id>/update_status/", SolicitationAtributionView.as_view()),
    path("solicitations/<str:solicitation_id>/drop/", SolicitationDropView.as_view())
]
