from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from slugify import slugify
from django.urls import reverse


# Create your models here.

class Item(models.Model):

	BRANDS_LIST = [
		'Zara',
		'Gap',
		"Levi Strauss & Co. (Levi's)",
		'Mango',
		'Monsoon',
		'Pull & Bear',
		'Bershka',
		'American Eagle (AE)',
		'Forever 21',
		'Stradivarious',
		'Parfois',
		'British Home Stores (BHS)',
		'United States Polo Assn.',
		'Adidas',
		'Tommy Hilfiger',
		'BOGGI',
		'HACKETT',
		'Massimo Dutti',
		'Punt Roma',
		'H&M',
		'Next',
		'Nike'
		]

	BRANDS = (
		('Zara', 'Zara'),
		('Gap', 'Gap'),
		("Levi Strauss & Co. (Levi's)", "Levi Strauss & Co. (Levi's)"),
		('Mango', 'Mango'),
		('Monsoon', 'Monsoon'),
		('Pull & Bear', 'Pull & Bear'),
		('Bershka', 'Bershka'),
		('American Eagle (AE)', 'American Eagle (AE)'),
		('Forever 21', 'Forever 21'),
		('Stradivarious', 'Stradivarious'),
		('Parfois', 'Parfois'),
		('British Home Stores (BHS)', 'British Home Stores (BHS)'),
		('United States Polo Assn.', 'United States Polo Assn.'),
		('Adidas', 'Adidas'),
		('Tommy Hilfiger', 'Tommy Hilfiger'),
		('BOGGI', 'BOGGI'),
		('HACKETT', 'HACKETT'),
		('Massimo Dutti', 'Massimo Dutti'),
		('Punt Roma', 'Punt Roma'),
		('H&M', 'H&M'),
		('next', 'Next'),
		('Nike', 'Nike')
		)

	OCASSIONS = (
		('Formal', 'Formal'),
		('Semi-Formal', 'Semi-Formal'),
		('Casual', 'Casual')
		)
	CATEGORIES = (
		('Top', 'Top'),
		('Bottom', 'Bottom'),
		('FullBody', 'Full Body'),
		('Shoes', 'Shoes')
		)
	GENDER = (
		('Male', 'Male'),
		('Female', 'Female')
		)
	
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=200, null=True, blank=True)
	brand = models.CharField(choices=BRANDS, max_length=100)
	gender = models.CharField(choices=GENDER, max_length=7) 
	description = models.TextField()
	color = models.CharField(max_length=200, blank=True)
	price = models.IntegerField(blank=True, null=True)
	category = models.CharField(max_length=100, choices=CATEGORIES)
	item_type = models.CharField(max_length=100, blank=True)
	style = models.CharField(max_length=200, blank=True)
	sleeve = models.CharField(max_length=200, blank=True, null=True)
	neck = models.CharField(max_length=100, blank=True, null=True)
	waist = models.CharField(max_length=100, blank=True, null=True)
	ocassion = models.CharField(max_length=50, choices=OCASSIONS, null=True)
	image_url = models.URLField(null=True, max_length=500, unique=True)
	website_url = models.URLField(null=True, max_length=500)
	users_interseted = models.ManyToManyField(User, blank=True, related_name="interested", related_query_name="users_interested")
	user_ratings = models.ManyToManyField(User, blank=True, through='ItemRating')

	def __str__(self):
		return self.title

	def all_users_interested(self):
		return self.users_interseted.count()

	def get_absolute_url(self):
		return reverse("item_detail", args=[self.id, self.slug])

	def save(self):
		super().save()
		self.slug = slugify(self.title)


class ItemRating(models.Model):
	RATINGS = (
		(1, 'Very Poor'),
		(2, 'Poor'),
		(3, 'Neutral'),
		(4, 'Good'),
		(5, 'Very Good')
		)

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.IntegerField(choices=RATINGS, blank=True, null=True)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)



