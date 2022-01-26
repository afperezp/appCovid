from django import forms

class ImageForm(forms.Form):
    first_name= forms.CharField(max_length=100)
    passport_field = forms.ImageField()
    
