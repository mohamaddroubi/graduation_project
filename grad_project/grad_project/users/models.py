from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from recommend.models import Item
from multiselectfield import MultiSelectField

# Create your models here.

class Profile(models.Model):

	USER_CLASS = (
		('Upper', 'More than $50'),
		('MUpper', '$40 - $50'),
		('MLower', '$20 - $40'),
		('Lower', 'Less than $20')
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = PhoneNumberField(null=True, blank=True)
	birthday = models.DateField(null=True, blank=True)
	gender = models.CharField(blank=True, null=True, choices=Item.GENDER, max_length=7)
	user_style = models.CharField(blank=True, max_length=12, null=True, choices=Item.OCASSIONS)
	user_class = models.CharField(blank=True, max_length=20, null=True, choices=USER_CLASS)
	#user_brands = models.TextField(blank=True, null=True, choices=brands)
	user_brands = models.CharField(null=True, blank=True, max_length=500)
	#user_brands = models.ManyToManyField(Brand)

	def __str__(self):
		return f'{self.user.username} Profile'

	

