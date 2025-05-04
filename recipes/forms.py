from django import forms
from .models import Recipe


CHART_CHOICES = (
    ('bar', 'Bar Chart'),
    ('pie', 'Pie Chart'),
    ('line', 'Line Chart'),
)

class RecipeSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        label='Recipe Title',
        widget=forms.TextInput(attrs={'placeholder': 'Enter title'})
    )
    ingredient = forms.CharField(
        required=False,
        label='Ingredient',
        widget=forms.TextInput(attrs={'placeholder': 'Enter ingredient'})
    )

    chart_type = forms.ChoiceField(choices=CHART_CHOICES, required=False)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'description', 'cooking_time', 'pic']