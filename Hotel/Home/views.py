from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from . models import Amenities, Hotel,HotelBookimg
from django.db.models import Q
# Create your views here.
def home(request):
    amenities_obj = Amenities.objects.all()
    hotel_obj = Hotel.objects.all()

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    aminity = request.GET.getlist('amenitys')
    print(aminity)
    if sort_by:
        if sort_by == 'ASC':
            hotel_obj = hotel_obj.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotel_obj = hotel_obj.order_by('-hotel_price')
    if search:
        hotel_obj = hotel_obj.filter(Q(hotel_name__icontains = search)|
        Q(desc__icontains = search))

    if len(aminity):
        hotel_obj = hotel_obj.filter(amenities__amenity_name__in = aminity).distinct()
    context = {
        "amenities_obj":amenities_obj,"hotel_obj":hotel_obj,'sort_by':sort_by,'search':search, 'aminity':aminity
    }
    return render(request,'home.html', context)

def login_page(request):
    if request.method=="POST":
        username =request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username )

        if not user_obj.exists():
            messages.warning(request,"Account not found")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user_obje = authenticate(username = username , password = password)
        if not user_obje:
            messages.warning(request,"Invalid Username or Password")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        login(request, user_obje)
        return redirect('/') 
       


    return render(request,'login.html')


def regester_page(request):
    if request.method=="POST":
        email =request.POST.get('email')
        username =request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request,"Username already exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()
        return redirect('/')




    return render(request,'regester.html')


def hotel_detail(request,uid):

    if request.method=="POST":
        checkin = request.POST.get('checkin')
        checkout =  request.POST.get('checkout')
        hotel = Hotel.objects.get(uid = uid)
        if not chech_booking( checkin , checkout , uid , hotel.room_count ):
            messages.warning(request,"Room not avilabe in these date")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        HotelBookimg.objects.create(hotel = hotel, user = request.user, start_date = checkin , end_date = checkout ,booking_type = 'Pre Paid')
        messages.warning(request,"Room are booked")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    hotel_obj = Hotel.objects.get(uid = uid)

    return render(request, "hotel-detail.html",{'hotel':hotel_obj})
    
def logout_user(request):
    logout(request)
    return redirect("/")

def chech_booking(start_date , end_date , uid , room_count ):
    sq= HotelBookimg.objects.filter(
        start_date__lte = start_date,
        end_date_gte =  end_date ,
        hotel__uid = uid
    ) 

    if len(sq) >= room_count:
        return False

    return True