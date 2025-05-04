from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from .forms import RecipeSearchForm, RecipeForm
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from .utils import get_chart
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy



# Home page
def home(request):
    return render(request, 'recipes/recipes_home.html')


# All recipes list + search (no chart here anymore)
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        ingredient = self.request.GET.get('ingredient')

        if title:
            queryset = queryset.filter(name__icontains=title)
        if ingredient:
            queryset = queryset.filter(ingredients__icontains=ingredient)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RecipeSearchForm(self.request.GET)
        context['form'] = form
        return context


# Recipe details
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'


# NEW: Analytics page view (shows chart + table)
def analytics(request):
    form = RecipeSearchForm(request.GET)
    context = {'form': form}

    queryset = Recipe.objects.all()

    title = request.GET.get('title')
    ingredient = request.GET.get('ingredient')

    if title:
        queryset = queryset.filter(name__icontains=title)
    if ingredient:
        queryset = queryset.filter(ingredients__icontains=ingredient)

    if queryset.exists() and form.is_valid():
        df = pd.DataFrame(list(queryset.values('id', 'name', 'ingredients', 'cooking_time')))
        labels = df['name'].copy()
        df['name'] = df.apply(
            lambda row: f'<a href="/recipes/list/{row["id"]}/">{row["name"]}</a>', axis=1
        )
        df = df[['name', 'ingredients', 'cooking_time']]
        context['table'] = df.to_html(classes="recipe-table", index=False, escape=False)

        chart_type = form.cleaned_data.get('chart_type')
        if chart_type in ['bar', 'pie', 'line']:
            chart = get_chart(chart_type, df, labels=labels)
            context['chart'] = chart
        else:
            context['chart'] = None
    else:
        context['table'] = None
        context['chart'] = None

    return render(request, 'recipes/analytics.html', context)


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes:list')  # after saving, go to recipe list
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})


def about(request):
    return render(request, 'recipes/about.html')


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipes:list')