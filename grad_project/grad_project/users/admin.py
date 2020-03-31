from django.contrib import admin
from .models import Profile
from .forms import ProfileAdminForm

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
	form = ProfileAdminForm

admin.site.register(Profile, ProfileAdmin)

