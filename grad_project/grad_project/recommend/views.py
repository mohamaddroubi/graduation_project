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


def about(request):
	return render(request, 'recommend/about.html')


@login_required
def item_detail(request, itemId, slug, recommId):
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
	
	is_interested = False
	user_purchases = client.send(ListUserPurchases(user_id))

	for i in user_purchases:
		if i['itemId'] == itemId:
			is_interested = True
	

	item_ratings = client.send(ListItemRatings(itemId))
	total_item_rating = 0

	for i in item_ratings:
		total_item_rating += i["rating"]
	if len(item_ratings) > 0:
		total_item_rating = total_item_rating/len(item_ratings)
		rating_stars = total_item_rating*2 + 3
	else:
		rating_stars = 0

	color = ""
	
	for c in item['Color']:
		color = color + c.replace(" ", "") + ", "
	
	color = color[:-2]

	req = RecommendItemsToItem(itemId, user_id, 9, scenario="related-items", cascade_create=True, return_properties=True)
	result = client.send(req)

	related_items = result['recomms']

	titles_rel = [] #titles of related items
	for i in related_items:
		titles_rel.append(i['values']['Description'].replace(".", ':').split(":")[0].upper())

	slugs_rel = [] #slug for related items
	for i in titles_rel:
		slugs_rel.append(i.replace(" ", "-"))

	for i in range(len(related_items)):
		related_items[i]['slug'] = slugs_rel[i]
		related_items[i]['title'] = titles_rel[i]
	
	
	context = {
        'item': item,
        'is_interested': is_interested,
        'all_users_interested': len(client.send(ListItemPurchases(itemId))),
        'title': slug.replace("-", " "),
        'slug': slug,
        'recommId': recommId,
        'rating_stars': rating_stars,
        'itemId': itemId,
		'color': color,
		'related_items': related_items,
		'rel_items_rec_id': result['recommId']
		
    }
	return render(request, 'recommend/item_detail.html', context)

@login_required
def search(request):
    user_id = str(User.objects.filter(username=request.user.username).first().id)
    if (request.method == 'GET'):

        category = request.GET.get('byCat')

        brand = request.GET.get('byBrand')

        occasion = request.GET.get('occasion')

        search = request.GET.get('search')

        url = f"?occasion={occasion}&byBrand={brand}&byCat={category}&search={search}"

        

        search_query = ""
        if not(search==""):
            search_query += search
        if not(brand==""):
            search_query += " "+brand
        if not(category==""):
            search_query += " "+category
        if not(occasion==""):
            search_query += " "+occasion
        
        result = client.send(SearchItems(user_id, search_query, count=50,
         scenario="search", cascade_create=True, return_properties=True, ))

        items = result['recomms']
        recommId = result['recommId']

        item_titles_items = []
        for i in items:
            item_titles_items.append(i['values']['Description'].replace(".", ':').split(":")[0].upper())

        slugs_items = []
        for i in item_titles_items:
            slugs_items.append(i.replace(" ", "-"))

        for i in range(len(items)):
            items[i]['slug'] = slugs_items[i]
            items[i]['title'] = item_titles_items[i]

        paginator = Paginator(items, 10)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)

        context = {
            'items': items,
            'page_obj': page_obj,
            'recommId': recommId,
			'cat': category,
			'brand': brand,
			'occasion': occasion,
			'search': search,
			'url': url
        }

        return render(request, 'recommend/search_results.html', context)

    return render(request, 'recommend/search_result.html')


def brands_list(request):
	#brands = sorted(Item.BRANDS_LIST)
	brands_recombee = Item.BRANDS_2
	paginator = Paginator(brands_recombee, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
	'page_obj': page_obj,
	'brands': brands_recombee,
	
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

	brand_title = brand
	for i in Item.BRANDS_2:
		if brand == i[0]:
			brand_title = i[1]
			break

	context = {
		'page_items': page_items,
		'items': items,
		'brand': brand,
		'brand_title': brand_title,
	}	
	
	return render(request, 'recommend/items.html', context)