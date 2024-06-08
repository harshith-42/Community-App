from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cohort/<str:pk>/', views.cohort, name='cohort'),

    path('create-cohort/', views.createCohort, name="create-cohort"),
    path('update-cohort/<str:pk>', views.updateCohort, name="update-cohort"),

]