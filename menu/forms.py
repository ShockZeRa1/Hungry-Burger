from django import forms

class CustomisationForm(forms.Form):
    quantity= forms.IntegerField(min_value=1, initial=1)
    
    
