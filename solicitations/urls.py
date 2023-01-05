from django.urls import path
from .views import SolicitationView,SolicitationDetailView


urlpatterns = [
    # path("solicitations/<str:donee_id>/", SolicitationView.as_view()),
    path("solicitations/", SolicitationView.as_view()),
    path("solicitations/<str:solicitation_id>/", SolicitationDetailView.as_view())
]
