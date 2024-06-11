from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name ='login'),
    path('logout/', views.logoutUser, name ='logout'),
        path('register/', views.registerPage, name ='register'),


    path('cohort/<str:pk>/', views.cohort, name='cohort'),

    path('create-cohort/', views.createCohort, name="create-cohort"),
    path('update-cohort/<str:pk>', views.updateCohort, name="update-cohort"),
    path('delete-cohort/<str:pk>', views.deleteCohort, name="delete-cohort"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

]