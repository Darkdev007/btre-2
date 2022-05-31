from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from .models import Listing

def listings(request):
    listings = Listing.objects.order_by('-list_Date').filter(is_published=True)
    # paginator = Paginator(listings, 3)
    # page = request.GET.get('page')
    # paged_listings = paginator.get_page(page)
    paginator = Paginator(listings, 3) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'listings': page_obj,
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk = listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html',context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_Date')

    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    #City 
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city ) #exact is case sensitive
    #State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state )
    #Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lt =bedrooms)
    #Price
    if 'price' is request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
    context = {
        'state_choices' : state_choices,
        'bedroom_choices' : bedroom_choices,
        'price_choices' : price_choices,
        'listings' : queryset_list,
    }
    return render(request, 'listings/search.html', context)
