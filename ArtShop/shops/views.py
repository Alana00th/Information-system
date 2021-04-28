from django.shortcuts import render
# from .forms import SubscriberForm
from quests.models import *

def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    return render(request, 'landing/home.html', locals())