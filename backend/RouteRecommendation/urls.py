# RouteRecommendation/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('solve_tsp/', views.solve_tsp, name='solve_tsp'),
]
