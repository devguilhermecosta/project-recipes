from django.urls import path
from authors import views

app_name: str = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', view=views.login_view, name='login'),
    path('login/create/', view=views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recipe/<int:id>/edit/',
         views.DashboardRecipe.as_view(),
         name='dashboard_recipe_edit'),
    path('dashboard/recipe/delete/',
         views.dashboard_delete_recipe,
         name='delete_recipe',
         ),
    path('dashboard/new/recipe',
         views.DashboardRecipe.as_view(),
         name='new_recipe',
         ),
    path('profile/<int:id>/',
         views.ProfileView.as_view(),
         name='profile',
         ),
]
