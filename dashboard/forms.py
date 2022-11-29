from dataclasses import field
from pyexpat import model
from random import choices
from sqlite3 import Date
from statistics import mode
from tkinter import Widget
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class Notesform(forms.ModelForm):
    class Meta:
        model=Note
        fields=['title','description'] 
class DateInput(forms.DateInput):
    input_type='date'            
class Homeform(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','title','description','due','is_finished'] 



class DashboardForm(forms.Form):
    text=forms.CharField(max_length=100,label="Enter your Search")
class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_finished']    
class ConversionForm(forms.Form):
    CHOICES=[('length','Length'),('mass','Mass')]
    measurement=forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)
class ConversionlengthForm(forms.Form):
    CHOICES=[('yard','Yard'),('foot','Foot')]
    input=forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the number'}
    ))    
    measure1=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    measure2=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
class ConversionMassForm(forms.Form):
    CHOICES=[('pound','Pound'),('kilogram','Kilogram')]
    input=forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the number'}
    ))    
    measure1=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    measure2=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    ) 
class UserReisteraionForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']