from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name ='login'),
    path('logout/', views.logoutUser, name ='logout'),
    path('register/', views.registerPage, name ='register'),


    path('cohort/<str:pk>/', views.cohort, name='cohort'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    path('create-cohort/', views.createCohort, name="create-cohort"),
    path('update-cohort/<str:pk>', views.updateCohort, name="update-cohort"),
    path('delete-cohort/<str:pk>', views.deleteCohort, name="delete-cohort"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

    path('update-user', views.updateUser, name="update-user"),
    path('toggle-follow', views.toggle_follow, name='toggle-follow'),
    path('profile/<int:pk>/followers/', views.followers_list, name='followers-list'),
    path('profile/<int:pk>/following/', views.following_list, name='following-list'),
]