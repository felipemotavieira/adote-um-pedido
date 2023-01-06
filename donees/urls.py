from django.urls import path
from . import views

urlpatterns = [
    path("donee/create/<str:pk>/", views.doneeView.as_view()),
    path("donee/<str:pk>/", views.doneeDetailView.as_view()),
    path("donee/", views.doneeListView.as_view())
]
