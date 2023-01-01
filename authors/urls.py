from django.urls import path
from authors import views

app_name: str = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', view=views.login_view, name='login'),
    path('login/create/', view=views.login_create, name='login_create'),
]
