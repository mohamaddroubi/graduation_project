from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from .models import Item
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from .forms import SearchForm
from django.core.paginator import Paginator
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import *
# Create your views here.

client = RecombeeClient('university-of-jordan-dev',
                        'sMGOTwMPzOPM3l6Tmxs8jXZ2WeCskPR9dnzKrdBczJHy1vdRFQs9HldcLPC8W63N')

@login_required
def recommend(request):
	user_profile=request.user.profile
	if user_profile.gender is None or user_profile.user_style is None or user_profile.user_class is None or user_profile.user_brands is None:
		messages.info(request, 'Please fill out some information for better cusotmized recommendations')
		return redirect('update_profile_initial')

	user_id = str(User.objects.filter(username=request.user.username).first().id)

	req = RecommendItemsToUser(user_id, 20, scenario="homepage", cascade_create=True, return_properties=True, diversity=0.1)
	req.timeout = 100000

	result = client.send(req)

	recomms = result['recomms']

	item_titles_recomms = []
	for i in recomms:
		item_titles_recomms.append(i['values']['Description'].replace(".", ':').split(":")[0].upper())

	slugs_recomms = []
	for i in item_titles_recomms:
		slugs_recomms.append(i.replace(" ", "-"))

	for i in range(len(recomms)):
		recomms[i]['slug'] = slugs_recomms[i]
		recomms[i]['title'] = item_titles_recomms[i]

	paginator = Paginator(recomms, 10)
	page_recomms = paginator.get_page(request.GET.get('page'))

	context = {
		'page_recomms': page_recomms,
		'recomms': recomms,
		'recommId': result["recommId"]
	}	
	
	return render(request, 'recommend/recommend.html', context)

@login_required
def items(request):
	user_profile=request.user.profile
	if user_profile.gender is None or user_profile.user_style is None or user_profile.user_class is None or user_profile.user_brands is None:
		messages.info(request, 'Please fill out some information for better cusotmized recommendations')
		return redirect('update_profile_initial')

	#req = ListItems(return_properties=True)
	
	#req.timeout = 10000
	items = client.send(ListItems(return_properties=True))

	item_titles_items = []
	for i in items:
		item_titles_items.append(i['Description'].replace(".", ':').split(":")[0].upper())

	slugs_items = []
	for i in item_titles_items:
		slugs_items.append(i.replace(" ", "-"))

	for i in range(len(items)):
		items[i]['slug'] = slugs_items[i]
		items[i]['title'] = item_titles_items[i]

	paginator = Paginator(items, 10)
	page = request.GET.get('page', 1)
	page_items = paginator.get_page(page)

	context = {
		'page_items': page_items,
		'items': items,
	}	
	
	return render(request, 'recommend/items.html', context)

@login_required
def search(request):
	search_form = SearchForm(request.GET)
	context = {
	'search_form': search_form,
	}

	return render(request, 'recommend/search.html', context)

"""
@login_required
def home(request, default='Recommended'):
	user_profile=request.user.profile
	if user_profile.gender is None or user_profile.user_style is None or user_profile.user_class is None or user_profile.user_brands is None:
		messages.info(request, 'Please fill out some information for better cusotmized recommendations')
		return redirect('update_profile_initial')
	search_form = SearchForm(request.GET)

	#items = Item.objects.all()

	items = client.send(ListItems(return_properties=True))

	user_id = str(User.objects.filter(username=request.user.username).first().id)

	result = client.send(RecommendItemsToUser(user_id, 20, scenario="homepage", cascade_create=True, return_properties=True, diversity=0.1))

	recomms = result['recomms']


	item_titles_items = []
	for i in items:
		item_titles_items.append(i['Description'].replace(".", ':').split(":")[0])

	item_titles_recomms = []
	for i in recomms:
		item_titles_recomms.append(i['values']['Description'].replace(".", ':').split(":")[0])

	slugs_items = []
	for i in item_titles_items:
		slugs_items.append(i.replace(" ", "-").upper())

	slugs_recomms = []
	for i in item_titles_recomms:
		slugs_recomms.append(i.replace(" ", "-").upper())

	for i in range(len(recomms)):
		recomms[i]['slug'] = slugs_recomms[i]
		recomms[i]['title'] = item_titles_recomms[i]

	for i in range(len(items)):
		items[i]['slug'] = slugs_items[i]
		items[i]['title'] = item_titles_items[i]

	paginator_items = Paginator(items, 5)
	page_items = paginator_items.get_page(request.GET.get('page'))

	paginator_recomms = Paginator(recomms, 5)
	page_recomms = paginator_recomms.get_page(request.GET.get('page'))

	context = {
		'page_items': page_items,
		'page_recomms': page_recomms,
		'items': items,
		'brands': Item.BRANDS,
		'search_form': search_form,
		'default': default,
		'recomms': recomms,
	}	
	
	return render(request, 'recommend/home.html', context)
"""

def about(request):
	return render(request, 'recommend/about.html')


@login_required
def item_detail(request, itemId, slug, recommId="none"):
	#item = request.item
	#item = get_object_or_404(Item, id=id, slug=slug)
	user_id = str(User.objects.filter(username=request.user.username).first().id)
	f = f"'itemId'==\"{itemId}\""
	req = ListItems(filter=f, return_properties=True)
	req.timeout = 10000
	item = client.send(req)[0]

	if(recommId != "none"):
		req = AddDetailView(user_id, itemId, recomm_id=recommId)
		req.timeout = 10000
		client.send(req)
	else:
		req = AddDetailView(user_id, itemId)
		req.timeout = 10000
		client.send(req)
	#title=item.title
	#num = Item.objects.filter(id=request.user.id)
	req = ListUserPurchases(user_id)
	req.timeout = 10000
	result = client.send(req)

	#items = request.user.interested.filter(id=item.id)
	is_interested = False
	#if items.exists():
	for item in result:
		if itemId == item['itemId']:
			is_interested = True
			break

	req = ListItemPurchases(itemId)
	#req.timeout = 10000

	item_ratings = client.send(ListItemRatings(itemId))
	total_item_rating = 0

	for i in item_ratings:
		total_item_rating += i["rating"]
	if len(item_ratings) > 0:
		total_item_rating = total_item_rating/len(item_ratings)
		rating_stars = total_item_rating*2 + 3
	else:
		rating_stars = 0

	context = {
		'item': item,
		'is_interested': is_interested,
		#'all_users_interested': item.all_users_interested(),
		'all_users_interested': len(client.send(req)),
		'title': slug.replace("-"," "),
		'slug': slug,
		'recommId': recommId,
		'rating_stars': rating_stars,
		'item_id': itemId
	}
	return render(request, 'recommend/item_detail.html', context)

@login_required
def search_result(request):
	user_id = str(User.objects.filter(username=request.user.username).first().id)
	if(request.method == 'GET'):

		category = request.GET.get('byCat')
		brand = request.GET.get('byBrand')
		search_query = f"'Category'==\"{category}\" or 'Brand'==\"{brand}\"" 
		items = client.send(ListItems(filter=search_query, return_properties=True, count=50))

		item_titles_items = []
		for i in items:
			item_titles_items.append(i['Description'].replace(".", ':').split(":")[0].upper())

		slugs_items = []
		for i in item_titles_items:
			slugs_items.append(i.replace(" ", "-"))

		for i in range(len(items)):
			items[i]['slug'] = slugs_items[i]
			items[i]['title'] = item_titles_items[i]

		paginator = Paginator(items, 10)
		page = request.GET.get('page')
		page_obj = paginator.get_page(page)

		context = {
		'items': items,
		'page_obj': page_obj,
		}

		return render(request, 'recommend/search_results.html', context)

	return render(request, 'recommend/search_result.html')

""""
class SearchResults(ListView):
	paginate_by = 5
	model = Item
	template_name = 'recommend/search_results.html'

	def get_queryset(self):
		if self.request.method == 'GET' and 'byCat' in self.request.GET and 'byBrand' in self.request.GET:
			category = self.request.GET.get('byCat')
			brand = self.request.GET.get('byBrand')
			item_list = Item.objects.filter(
				Q(category=category)|Q(brand=brand)
				)
			return item_list
		else:
			return ['wrong get request']
"""

def brands_list(request):
	brands = sorted(Item.BRANDS_LIST)
	paginator = Paginator(brands, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
	'page_obj': page_obj,
	'brands': brands
	}
	return render(request, 'recommend/brands_list.html', context)

def brand_items(request, brand): 
	f = f"'Brand'==\"{brand}\""
	items = client.send(ListItems(filter=f, return_properties=True))

	item_titles_items = []
	for i in items:
		item_titles_items.append(i['Description'].replace(".", ':').split(":")[0].upper())

	slugs_items = []
	for i in item_titles_items:
		slugs_items.append(i.replace(" ", "-"))

	for i in range(len(items)):
		items[i]['slug'] = slugs_items[i]
		items[i]['title'] = item_titles_items[i]

	paginator = Paginator(items, 10)
	page = request.GET.get('page', 1)
	page_items = paginator.get_page(page)

	context = {
		'page_items': page_items,
		'items': items,
		'brand': brand
	}	
	
	return render(request, 'recommend/items.html', context)