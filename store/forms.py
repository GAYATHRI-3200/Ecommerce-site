from django import forms

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'



class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class ContactForm(forms.Form): #new form called contactForm
 	Username = forms.CharField(required=True,max_length=50,help_text='limit 50 chars')
 	UserEmail = forms.EmailField(required=True)
 	Message = forms.CharField(required=True,widget=forms.Textarea)

#class ContactForm(forms.Form):
#	class Meta:
#		model = Contact
#		fields = '__all__' #new form called contactForm
 	