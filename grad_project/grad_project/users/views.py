from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegisterForm, UserProfileForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Profile
from django.contrib.auth.models import User
from recommend.models import Item
from django.urls import reverse
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import *
from datetime import datetime, time, date

# Create your views here.

client = RecombeeClient('university-of-jordan-dev',
                        'sMGOTwMPzOPM3l6Tmxs8jXZ2WeCskPR9dnzKrdBczJHy1vdRFQs9HldcLPC8W63N')

@transaction.atomic
def register(request):
	if request.method == 'POST':
		user_form = UserRegisterForm(request.POST)
		if user_form.is_valid():
			user_form.save()
			username = user_form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}! You can now login')
			
			user_id = str(User.objects.filter(username=username).first().id)
			req = AddUser(user_id)
			#req.timeout = 10000
			client.send(req)

			return redirect('login')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		user_form = UserRegisterForm()
		
	return render(request, 'users/register.html', {'u_form': user_form})

@login_required
@transaction.atomic
def update_profile(request):
	if request.method=='POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Account updated for {request.user.username}!')
			#timedate = datetime.combine(p_form.cleaned_data.get('bithday'), time.min)
			#timestamp = datetime.timestamp(timedate)
			values = {
				"Class": p_form.cleaned_data.get('user_class'),
				"Fav_Brands": p_form.cleaned_data.get('user_brands'),
				#"Date_of_Birth": timestamp,
				"Type": p_form.cleaned_data.get('user_style'),
				"Gender": p_form.cleaned_data.get('gender')
			}

			user_id = str(User.objects.filter(username=request.user.username).first().id)
			req = SetUserValues(user_id, values, cascade_create=True)
			req.timeout = 10000
			
			client.send(req)
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	#created = Profile.objects.get_or_create(user=request.user)
	return render(request, 'users/update_profile.html', context)

@login_required
@transaction.atomic
def update_profile_initial(request):
	if request.method=='POST':
		#u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = UserProfileForm(request.POST, instance=request.user.profile)
		if p_form.is_valid():
			#u_form.save()
			p_form.save()
			messages.success(request, f'Profile updated for {request.user.username}!')
			#timedate = datetime.combine(p_form.cleaned_data.get('bithday'), time.min)
			#timestamp = datetime.timestamp(timedate)
			values = {
				"Class": p_form.cleaned_data.get('user_class'),
				"Fav_Brands": p_form.cleaned_data.get('user_brands'),
				#"Date_of_Birth": timestamp,
				"Type": p_form.cleaned_data.get('user_style'),
				"Gender": p_form.cleaned_data.get('gender')
			}
			user_id = str(User.objects.filter(username=request.user.username).first().id)
			req = SetUserValues(user_id, values, cascade_create=True)
			req.timeout = 100000
			#user_id = str(User.objects.filter(username=request.user.username).first().id)
			client.send(req)
			return redirect('profile')
	else:
		#u_form = UserUpdateForm(instance=request.user)
		p_form = UserProfileForm(instance=request.user.profile)

	context = {
		#'u_form': u_form,
		'p_form': p_form
	}

	#created = Profile.objects.get_or_create(user=request.user)
	return render(request, 'users/update_profile.html', context)

@login_required
def profile(request):
	#items_interested = Item.objects.filter(users_interested.username==request.user.username)
	user_id = str(User.objects.filter(username=request.user.username).first().id)
	req = ListUserPurchases(user_id)
	req.timeout = 10000
	user_purchases = client.send(req)
	items = []
	for i in user_purchases:
		itemId = i['itemId']
		f = f"'itemId'==\"{itemId}\""
		req = ListItems(filter=f, return_properties=True, included_properties=['Description'])
		req.timeout = 10000
		items.extend(client.send(req))
	#items = request.user.interested.all()

	item_titles = []
	for i in items:
		item_titles.append(i['Description'].replace(".", ':').split(":")[0])

	slugs_items = []
	for i in item_titles:
		slugs_items.append(i.replace(" ", "-").upper())

	for i in range(len(items)):
		items[i]['slug'] = slugs_items[i]
		items[i]['title'] = item_titles[i]

	
	brands = request.user.profile.user_brands.replace("]", "").replace("[", "").replace("\'", "").replace('\"',"").replace(" ","").split(",")
	
	brands_list = []
	for i in  Item.BRANDS:
		if i[0] in brands:
			brands_list.append(i[1])

	
	context = {
		'items': items,
		'brands': brands_list
	}
	#created = Profile.objects.get_or_create(user=request.user)
	return render(request, 'users/profile.html', context)

def interested(request, slug, recommId):

    user_id = str(User.objects.filter(username=request.user.username).first().id)
    itemId = request.POST.get('item_id')
    # f = f"'itemId'==\"{itemId}\""
    # item = client.send(ListItems(filter=f, return_properties=True))
    # item = get_object_or_404(Item, id=request.POST.get('item_id'))
    is_interested = False
    user_purchases = client.send(ListUserPurchases(user_id))
    for item in user_purchases:
        if item['itemId'] == itemId:
            is_interested = True

    if is_interested:
        req = DeletePurchase(user_id, itemId)
        req.timeout = 10000
        client.send(req)
        is_interested = False

    else:
        if recommId != "none":
            req = AddPurchase(user_id, itemId, recomm_id=recommId)
            req.timeout = 10000
            client.send(req)
        else:
            req = AddPurchase(user_id, itemId)
            req.timeout = 10000
            client.send(req)
        is_interested = True

    return redirect('item_detail', itemId=itemId, slug=slug, recommId=recommId)

"""

	#items = request.user.interested.filter(id=item.id)
	if items.exists():
		#item.interested.remove(request.user)
		request.user.interested.remove(item)
		is_interested = False
	else:
		request.user.interested.add(item)
		#item.interested.add(request.user)

		is_interested = True
	return HttpResponseRedirect(item.get_absolute_url())
"""

def rate(request, itemId, slug, recommId):
	user_id = str(User.objects.filter(username=request.user.username).first().id)
	rating = float(request.POST.get('rating'))
	if rating > 0:
		rating_recombee = (rating-3)/2
		if recommId != "none":
			client.send(AddRating(user_id, itemId, rating_recombee,  recomm_id=recommId))
		else: 
			client.send(AddRating(user_id, itemId, rating_recombee))
	elif rating == 0:
		client.send(DeleteRating(user_id, itemId))

	return HttpResponseRedirect(reverse("item_detail", args=[itemId, slug, recommId]))

def brand_rate(request, brand):

	user_id = str(User.objects.filter(username=request.user.username).first().id)
	rating = int(request.POST.get('rating'))
	temp_brand = brand

	if brand == "Levi's":
		brand = "Levis"
	elif brand == "Pull & Bear":
		brand = "PullBear"
	elif brand == "AE":
		brand = "AmericanEagle"
	elif brand == "Tommy Hilfiger":
		brand = "TommyHilfiger"
	elif brand == "Puntroma":
		brand = "PuntRoma"
	
	values = {
		brand: rating
	}

	client.send(SetUserValues(user_id, values))

	return HttpResponseRedirect(reverse("brand_items", args=[temp_brand]))