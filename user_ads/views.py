from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from .models import RealEstate, City, Region, RealEstatePicture, RealEstateLike, Brand
from .models import SecondHand, SecondHandPicture, SecondHandLike, SecondHandSubCategory, SecondHandType
from .forms import RealEstate_SearchForm, RealEstate_PostingForm
from .forms import SecondHand_SearchForm, SecondHand_PostingForm
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect
# Fuzzy string matching with fuzzywuzzy (MIT License)
# https://github.com/seatgeek/fuzzywuzzy
from fuzzywuzzy import process # Find the most likely city name based on the user's input
from django.contrib import messages
from django.views import View



@login_required
def real_estate_post(request):

    # Check if the user has already posted 3 ads
    user_ads_count = RealEstate.objects.filter(author=request.user).count()
    if user_ads_count >= 3 and not request.user.is_staff:
        messages.error(request, "משתמשים רגילים יכולים לפרסם עד 3 מודעות בלבד.")
        # Redirect the user to the same page where they clicked the button
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('real_estate')
    
    city_list = City.objects.all().order_by('name')
    if request.method == 'POST':
        form = RealEstate_PostingForm(request.POST, request.FILES)
        #form = RealEstate_PostingForm(request.POST or None, request.FILES or None, user=request.user)

        if form.is_valid():
            real_estate = form.save(commit=False)
            real_estate.author = request.user  # set author to current user
            real_estate.save()
            
            # handle pictures upload and link them to the real_estate object
            for picture in request.FILES.getlist('pictures'):
                RealEstatePicture.objects.create(ad=real_estate, picture=picture)

            return redirect('real_estate')
    else:
        form = RealEstate_PostingForm()
    context = { 'form': form,
                'city_list': city_list, 
               }
    return render(request, 'user_ads/post_new_ad/real_estate_post.html', context)

# @cache_page(settings.CACHE_TTL, key_prefix='real_estate_{user_id}')
@cache_page(settings.CACHE_TTL)
@csrf_protect
def real_estate(request):
    city_list = City.objects.all().order_by('name')
    if request.method == 'POST':
        form = RealEstate_SearchForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            deal_type = form.cleaned_data['deal_type']
            city = form.cleaned_data['city']
            max_cost = form.cleaned_data['max_cost']
            without_intermediaries = form.cleaned_data['without_intermediaries']
            with_photo = form.cleaned_data['with_image']
            min_rooms = form.cleaned_data['min_rooms']
            max_rooms = form.cleaned_data['max_rooms']
            is_new = form.cleaned_data['is_new']
            renovated = form.cleaned_data['renovated']
            furnished = form.cleaned_data['furnished']
            balcony = form.cleaned_data['balcony']
            bunker = form.cleaned_data['bunker']
            storage = form.cleaned_data['storage']
            conditioner = form.cleaned_data['conditioner']
            elevator = form.cleaned_data['elevator']
            parking = form.cleaned_data['parking']
            disabled_access = form.cleaned_data['disabled_access']
            exclusive = form.cleaned_data['exclusive']

            ads = RealEstate.objects.all().order_by('-id') #need add filter ads by date for improved performance (actual ads only)

            # filters
            if category:
                ads = ads.filter(category__name=category)
            if deal_type:
                ads = ads.filter(deal_type__name=deal_type)
            if city:
                # find the most likely city name based on the provided user's input
                city_names = [city_obj.name for city_obj in City.objects.all()]

                if city in city_names:
                    ads = ads.filter(city__name=city)
                else:
                    likely_city = process.extractOne(city, city_names)[0]
                    ads = ads.filter(city__name=likely_city)

            if max_cost != None:
                #ads = ads.filter(cost__in=range(0,max_cost+1))
                #ads = ads.filter(date__range=["2011-01-01", "2011-01-31"])
                ads = ads.filter(cost__lte=max_cost)
            if max_rooms < 6:
                ads = ads.filter(rooms__lte=max_rooms)
            if True:  # max_rooms < 6:
                ads = ads.filter(rooms__gte=min_rooms)
            if is_new:
                ads = ads.filter(is_new=True)
            if renovated:
                ads = ads.filter(renovated=True)
            if furnished:
                ads = ads.filter(furnished=True)
            if balcony:
                ads = ads.filter(balcony=True)
            if bunker:
                ads = ads.filter(bunker=True)
            if storage:
                ads = ads.filter(storage=True)
            if conditioner:
                ads = ads.filter(conditioner=True)
            if elevator:
                ads = ads.filter(elevator=True)
            if parking:
                ads = ads.filter(parking=True)
            if disabled_access:
                ads = ads.filter(disabled_access=True)
            if exclusive:
                ads = ads.filter(exclusive=True)

            # more filters
            if without_intermediaries:
                ads = ads.exclude(without_intermediaries=False)
            if with_photo:
                ads = ads.exclude(picture="default_realestate.jpg")
            # make as auto for sicling by parameters of form with all passible combinations

        else:
            form = RealEstate_SearchForm()
            ads = RealEstate.objects.all().order_by('-id')

    else:
        form = RealEstate_SearchForm()
        ads = RealEstate.objects.all().order_by('-id')
    
    # pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(ads, 20)  # Show 50 ads per page

    try:
        ads = paginator.get_page(page)
    except (PageNotAnInteger, EmptyPage):
        ads = paginator.get_page(1)
        
    context = { 'form': form, 'ads': ads,
                'city_list': city_list, 
                'MEDIA_URL': settings.MEDIA_URL
               }
    return render(request, 'user_ads/real_estate.html', context)

@login_required
def real_estate_detail(request, pk):
    real_estate = get_object_or_404(RealEstate, pk=pk)
    return render(request, 'user_ads/real_estate_detail.html', {'ads': [real_estate]})


@login_required
def real_estate_delete(request, pk):
    real_estate = get_object_or_404(RealEstate, pk=pk, author=request.user)
    if request.method == 'POST':
        real_estate.delete()
    return redirect('user_profile')

@login_required
def liked_real_estate_ids_json(request):
    cache_key = 'liked_real_estate_ids_json_{}'.format(request.user.id if request.user.is_authenticated else 'anonymous')
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse(cached_data)
        
    if request.user.is_authenticated:
        liked_real_estate_ids = RealEstateLike.objects.filter(user=request.user).values_list('ad_id', flat=True)
    else:
        liked_real_estate_ids = []

    data = {'liked_real_estate_ids': list(liked_real_estate_ids)}

    # Cache the data
    cache.set(cache_key, data, settings.CACHE_TTL)

    return JsonResponse(data)

@login_required
def real_estate_like(request, real_estate_id):
    if request.method == 'POST':
        # print('real_estate_like')
        real_estate = get_object_or_404(RealEstate, id=real_estate_id)
        like, created = RealEstateLike.objects.get_or_create(user=request.user, ad=real_estate)
        if not created:
            like.delete()

        # Delete the cached data
        cache_key = 'liked_real_estate_ids_json_{}'.format(request.user.id)
        cache.delete(cache_key)

        # Call liked_json to update the cache
        liked_real_estate_ids_json(request)
        
        return JsonResponse({'created': created})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@cache_page(settings.CACHE_TTL)
def secondhand(request):
    category = None
    sub_category = None
    type_ = None
    region_list = Region.objects.all().order_by('name')

    form = SecondHand_SearchForm(request.GET)

    if form.is_valid():
        category = form.cleaned_data['category']
        sub_category = form.cleaned_data['sub_category']
        type_ = form.cleaned_data['type']
        region = form.cleaned_data['region']
        min_price = form.cleaned_data['min_price']
        max_price = form.cleaned_data['max_price']
        with_photo = form.cleaned_data['with_image']
        # exclusive = form.cleaned_data['exclusive']

        if sub_category and sub_category.category != category:
            sub_category = None
            form.fields['sub_category'].queryset = SecondHandSubCategory.objects.none()
        
        if type_ and type_.sub_category != sub_category:
            type_ = None
            form.fields['type'].queryset = SecondHandType.objects.none()
        
        if category:
            form.fields['sub_category'].queryset = SecondHandSubCategory.objects.filter(category=category.id)
        
        if sub_category:
            form.fields['type'].queryset = SecondHandType.objects.filter(sub_category=sub_category.id)
    
    ads = SecondHand.objects.all().order_by('-id')

    # filters
    if category:
        ads = ads.filter(category=category)
    if sub_category:
        ads = ads.filter(sub_category=sub_category)
    if type_:
        ads = ads.filter(type=type_)
    if min_price:
            ads = ads.filter(cost__gte=min_price)
    if max_price:
        ads = ads.filter(cost__lte=max_price)
    if region:
        ads = ads.filter(city__region=region)
    
    if with_photo:
        pass # TODO
    # if exclusive:
    #     ads = ads.filter(exclusive=True)
    
    # pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(ads, 20)  # Show 50 ads per page

    try:
        ads = paginator.get_page(page)
    except (PageNotAnInteger, EmptyPage):
        ads = paginator.get_page(1)

    context = { 'form': form, 'ads': ads,
                'region_list': region_list, }
    return render(request, 'user_ads/secondhand/secondhand.html', context)

@login_required
def secondhand_post(request):

    # Check if the user has already posted 3 ads
    user_ads_count = SecondHand.objects.filter(author=request.user).count()
    if user_ads_count >= 3 and not request.user.is_staff:
        messages.error(request, "משתמשים רגילים יכולים לפרסם עד 3 מודעות בלבד.")
        # Redirect the user to the same page where they clicked the button
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('secondhand')
    
    city_list = City.objects.all().order_by('name')
    brand_list = Brand.objects.all().order_by('name')
    if request.method == 'POST':
        form = SecondHand_PostingForm(request.POST, request.FILES)

        if form.is_valid():
            secondhand = form.save(commit=False)
            secondhand.author = request.user  # set author to current user
            secondhand.save()
            
            # handle pictures upload and link them to the secondhand object
            for picture in request.FILES.getlist('pictures'):
                SecondHandPicture.objects.create(ad=secondhand, picture=picture)

            return redirect('secondhand')
    else:
        form = SecondHand_PostingForm()
    context = { 'form': form,
                'city_list': city_list,
                'brand_list': brand_list,
               }
    return render(request, 'user_ads/post_new_ad/secondhand_post.html', context)

@login_required
def secondhand_detail(request, pk):
    secondhand = get_object_or_404(SecondHand, pk=pk)
    return render(request, 'user_ads/secondhand/secondhand_detail.html', {'ads': [secondhand]})

@login_required
def secondhand_delete(request, pk):
    secondhand = get_object_or_404(SecondHand, pk=pk, author=request.user)
    if request.method == 'POST':
        secondhand.delete()
    return redirect('user_profile')

@login_required
def liked_secondhand_ids_json(request):
    cache_key = 'liked_secondhand_ids_json_{}'.format(request.user.id if request.user.is_authenticated else 'anonymous')
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse(cached_data)
        
    if request.user.is_authenticated:
        liked_secondhand_ids = SecondHandLike.objects.filter(user=request.user).values_list('ad_id', flat=True)
    else:
        liked_secondhand_ids = []

    data = {'liked_secondhand_ids': list(liked_secondhand_ids)}

    # Cache the data
    cache.set(cache_key, data, settings.CACHE_TTL)

    return JsonResponse(data)

@login_required
def secondhand_like(request, secondhand_id):
    print('secondhand_like')
    if request.method == 'POST':
        secondhand = get_object_or_404(SecondHand, id=secondhand_id)
        like, created = SecondHandLike.objects.get_or_create(user=request.user, ad=secondhand)
        if not created:
            like.delete()

        # Delete the cached data
        cache_key = 'liked_secondhand_ids_json_{}'.format(request.user.id)
        cache.delete(cache_key)

        # Call liked_json to update the cache
        liked_secondhand_ids_json(request)
        
        return JsonResponse({'created': created})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def new_ad(request):
    return render(request, 'user_ads/post_new_ad/new_ad.html')

class GetSubcategoriesOfSecondhand(View):
    def get(self, request, *args, **kwargs):
        category_id = self.kwargs.get('category_id')
        sub_categories = SecondHandSubCategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(sub_categories), safe=False)

class GetTypeOfSecondhand(View):
    def get(self, request, *args, **kwargs):
        sub_category_id = self.kwargs.get('sub_category_id')
        types = SecondHandType.objects.filter(sub_category_id=sub_category_id).values('id', 'name')
        return JsonResponse(list(types), safe=False)

