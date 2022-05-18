from django.urls import path

from .views import perform_apriori, view_results

urlpatterns = [
    path("", perform_apriori, name="csv-form"),
    path("results/", view_results, name="csv-results"),
]
