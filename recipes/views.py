from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from .forms import RecipeSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from .utils import get_chart



# Create your views here.
def home(request):
    return render(request, 'recipes/recipes_home.html')

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

        queryset = self.get_queryset()
        if queryset.exists() and form.is_valid():
            df = pd.DataFrame(list(queryset.values('id', 'name', 'ingredients', 'cooking_time')))
            
            # Copy plain names for use as labels before modifying 'name' column
            labels = df['name'].copy()

            # Make name column a clickable link to the detail page
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
            context['table'] = None
            context['chart'] = None

        return context



class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
