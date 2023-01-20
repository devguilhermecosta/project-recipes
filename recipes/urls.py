from django.urls import path
from recipes import views

app_name: str = 'recipes'

urlpatterns = [
    path('', views.RecipeHomeBase.as_view(), name='home'),
    path('recipe/search/', views.search, name='search'),
    path('recipe/<int:id>/', views.RecipeDetailsView.as_view(), name='recipe'),
    path('recipe/category/<int:id>/', views.category, name='category'),
]
