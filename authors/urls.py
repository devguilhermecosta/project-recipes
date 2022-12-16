from django.urls import path
from authors import views

app_name: str = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
]
