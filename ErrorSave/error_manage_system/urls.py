from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('loggingError/', views.loggingError, name='logging_error'),
    path('myError/', views.myError, name='my_error'),
    path('loggingError/createError/', views.createError, name='createError'),
    path('<int:e_id>/deleteError/', views.deleteError, name='deleteError'),

    path('<int:e_id>/myDetailError/', views.myDetailError, name='myDetailError'),
    path('<int:e_id>/myDetailError/updateError/', views.update_error, name='updateError'),

    path('<int:e_id>/detailError/', views.detailError, name='detailError'),
    path('<int:e_id>/detailError/loggingSolution/', views.logging_solution, name='logging_solution'),
    path('<int:e_id>/detailError/loggingSolution/createSolution/', views.createSolution, name='createSolution'),

    path('signin/signup/', views.signup, name='main_signup'),
    path('signin/', views.signin, name='main_signin'),
    path('verifyCode/', views.verifyCode, name='main_verifyCode'),
    path('verifyCode/verify/', views.verify, name='main_verify'),

    path('join', views.join, name='main_join'),
    path('signin/signin/login', views.login, name='main_login'),
    path('logout/', views.logout, name='main_logout'),

    path('search_title/', views.search_title, name='serch_title'),
]