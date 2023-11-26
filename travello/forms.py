from django import forms
from .models import Destination
from .models import Detailed_desc

class CountryForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['country', 'img1', 'img2', 'number']  



class PlacesForm(forms.ModelForm):
    class Meta:
        model = Detailed_desc
        fields = ['country', 'days', 'price', 'rating', 'dest_name', 'img1', 'img2', 'desc', 'day1', 'day2', 'day3', 'day4', 'day5', 'day6']