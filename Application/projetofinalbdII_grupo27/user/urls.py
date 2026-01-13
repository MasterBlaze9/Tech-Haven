from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.show_users, name='list_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.signout, name='logout')
]
