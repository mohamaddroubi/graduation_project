from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from recommend.models import Item
from django.contrib import admin


class UserRegisterForm(UserCreationForm):

	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):

	phone = PhoneNumberField(required=False)
	birthday = forms.DateField(required=True, widget=forms.SelectDateWidget(empty_label=("Year", "Month", "Day"), years=list(range(1960, 2020, 1))))
	gender = forms.ChoiceField(choices=Item.GENDER, widget=forms.RadioSelect())
	user_style = forms.ChoiceField(choices=Item.OCASSIONS,
	 label='Please choose the kind of outfit that most describes your character',
	 widget=forms.RadioSelect())
	user_class = forms.ChoiceField(choices=Profile.USER_CLASS,
		label='Approximately, How much are you willing to pay for a basic polo shirt?',
		widget=forms.RadioSelect())
	user_brands = forms.MultipleChoiceField(label="Choose your most favorite brands", 
		widget=forms.CheckboxSelectMultiple(),
		choices=Item.BRANDS,
		)

	class Meta:
		model = Profile
		fields = ['phone', 'birthday', 'gender', 'user_style', 'user_class', 'user_brands']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['email']


class ProfileAdminForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(ProfileAdminForm, self).__init__(*args, **kwargs)
		self.fields['user_brands'].widget = forms.CheckboxSelectMultiple(choices=Item.BRANDS)

class ProfileUpdateForm(forms.ModelForm):

	phone = PhoneNumberField(required=False)
	birthday = forms.DateField(required=False, widget=forms.SelectDateWidget(empty_label=("Year", "Month", "Day"), years=list(range(1960, 2020, 1))))
	gender = forms.ChoiceField(choices=Item.GENDER, widget=forms.RadioSelect())
	user_style = forms.ChoiceField(choices=Item.OCASSIONS,
	 label='Please choose the kind of outfit that most describes your character',
	 widget=forms.RadioSelect())
	#user_class = forms.ChoiceField(choices=(('Upper', 'More than $50'), ('U_mid', '$40 - $50'), ('L_mid', '$20 - $40'), ('Lower', 'Less than $20')),
	#	label='Approximately, How much are you willing to pay for a basic polo shirt?',
	#	widget=forms.RadioSelect())
	user_brands = forms.MultipleChoiceField(label="Choose your most favorite brands", 
		widget=forms.CheckboxSelectMultiple(),
		choices=Item.BRANDS,
		)

	class Meta:
		model = Profile
		fields = ['phone', 'birthday', 'gender', 'user_style', 'user_brands']

