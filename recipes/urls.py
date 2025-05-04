from django.urls import path
from .views import home
from .views import RecipeListView, RecipeDetailView
from . import views


app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),
    path('list/', RecipeListView.as_view(), name='list'),
    path('list/<int:pk>/', RecipeDetailView.as_view(), name='detail'),
    path('add/', views.add_recipe, name='add'),
    path('analytics/', views.analytics, name='analytics'),
    path('about/', views.about, name='about'),
    path('list/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='delete'),

]
