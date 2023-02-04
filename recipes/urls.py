from django.urls import path
from recipes import views

app_name: str = 'recipes'

urlpatterns = [
    path('', views.RecipeHomeBase.as_view(), name='home'),
    path('recipe/search/', views.RecipeSearch.as_view(), name='search'),
    path('recipe/<int:pk>/', views.RecipeDetailsView.as_view(), name='recipe'),
    path('recipe/category/<int:category_id>/',
         views.RecipeCategory.as_view(),
         name='category',
         ),
    path('recipes/api/v1/',
         views.RecipeListViewApi.as_view(),
         name='recipe_api',
         ),
    path('recipes/api/v1/<int:pk>/',
         views.RecipeListViewDetailsApi.as_view(),
         name='recipe_details_api',
         ),
    path('recipes/theory/', views.theory, name='theory')
]
