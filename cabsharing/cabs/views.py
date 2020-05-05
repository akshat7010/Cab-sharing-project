from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Post, Frequest, Fgroup2, Grequest2, Fgroup3, Grequest3, Fgroup4


def index(request):
    queryset1 = Frequest.objects.filter(
        to=request.user.username
    )
    queryset2 = Grequest2.objects.filter(
        Q(to1=request.user.username) | Q(to2=request.user.username)
    )
    queryset4 = Grequest3.objects.filter(
        Q(to1=request.user.username) | Q(to2=request.user.username)| Q(to3=request.user.username)
    )
    i = Post.objects.filter(
        created_by__iexact=request.user.username
    )
    query = []
    for instance in i:
        queryset3 = Post.objects.filter(
            time__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
            date=instance.date,
            destination=instance.destination,
            passengers__range=(1, 4 - instance.passengers)
        ).exclude(created_by__iexact=instance.created_by)
        query += queryset3
    query1 = []
    for instance in i:
        queryset3 = Fgroup2.objects.filter(
            time1__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
            date=instance.date,
            destination=instance.destination,
            total_passengers__range=(1, 4 - instance.passengers)
        ).exclude(Q(created_by1__iexact=instance.created_by) & Q(created_by2__iexact=instance.created_by))
        query1 += queryset3
    query2 = []
    for instance in i:
        queryset3 = Fgroup3.objects.filter(
            time1__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
            date=instance.date,
            destination=instance.destination,
            total_passengers__range=(1, 4 - instance.passengers)
        ).exclude(Q(created_by1__iexact=instance.created_by) & Q(created_by2__iexact=instance.created_by)
                  & Q(created_by3__iexact=instance.created_by))
        query2 += queryset3
    context = {
        "num": len(queryset1) + len(queryset2)+len(queryset4),
        "nnum": len(query1) + len(query)+ len(query2),
    }
    return render(request, 'home.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('cabs:main')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('cabs:main')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('cabs:main')


@login_required(login_url="/cabs/login/")
def post_view(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.created_by = request.user.username
            instance.booked = False
            instance.save()
            queryset = Post.objects.filter(
                time__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
                date=instance.date,
                destination=instance.destination,
                passengers__range=(1, 4 - instance.passengers)
            ).exclude(created_by__iexact=instance.created_by)
            queryset1 = Fgroup2.objects.filter(
                time1__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
                date=instance.date,
                destination=instance.destination,
                total_passengers__range=(1, 4 - instance.passengers)
            ).exclude(Q(created_by1__iexact=instance.created_by) & Q(created_by2__iexact=instance.created_by))
            queryset2 = Fgroup3.objects.filter(
                time1__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
                date=instance.date,
                destination=instance.destination,
                total_passengers__range=(1, 4 - instance.passengers)
            ).exclude(Q(created_by1__iexact=instance.created_by) & Q(created_by2__iexact=instance.created_by)
                      & Q(created_by3__iexact=instance.created_by))
            context = {
                "passenger_list": queryset,
                "groups_list": queryset1,
                "groups3_list": queryset2,
                "title": "Search Results"
            }
            return render(request, 'match.html', context)
    else:
        form = forms.CreatePost()
    return render(request, 'post.html', {'form': form})


@login_required(login_url="/cabs/login/")
def booking_view(request):
    queryset = Post.objects.filter(
        created_by__iexact=request.user.username
    )
    context = {
        "booking_list": queryset,
        "title": "Your bookings"
    }
    return render(request, 'bookings.html', context)


@login_required(login_url="/cabs/login/")
def cancel_view(request, id):
    obj = get_object_or_404(Post, id=id)
    obj.delete()
    return redirect('cabs:bookings')


@login_required(login_url="/cabs/login/")
def notification_view(request):
    i = Post.objects.filter(
        created_by__iexact=request.user.username
    )
    query = []
    for instance in i:
        queryset = Post.objects.filter(
            time__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
            date=instance.date,
            destination=instance.destination,
            passengers__range=(1, 4 - instance.passengers)
        ).exclude(created_by__iexact=instance.created_by)
        query += queryset
    query1 = []
    for instance in i:
        queryset = Fgroup2.objects.filter(
            time1__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
            date=instance.date,
            destination=instance.destination,
            total_passengers__range=(1, 4 - instance.passengers)
        ).exclude(Q(created_by1__iexact=instance.created_by) & Q(created_by2__iexact=instance.created_by))
        query1 += queryset
    query2 = []
    for instance in i:
        queryset = Fgroup3.objects.filter(
            time1__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
            date=instance.date,
            destination=instance.destination,
            total_passengers__range=(1, 4 - instance.passengers)
        ).exclude(Q(created_by1__iexact=instance.created_by) & Q(created_by2__iexact=instance.created_by)
                  & Q(created_by3__iexact=instance.created_by))
        query2 += queryset
    context = {
        "passenger_list": query,
        "groups_list": query1,
        "groups3_list": query2,
        "title": "Notifications"
    }
    return render(request, 'match.html', context)


def aboutus_view(request):
    return render(request, 'aboutus.html')


def feedback_view(request):
    if request.method == 'POST':
        form = forms.FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, 'thankyou.html')
    else:
        form = forms.FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})


def contact_view(request):
    return render(request, 'contact.html')


@login_required(login_url="/cabs/login/")
def request_view(request, name1, name2, id):
    obj = Frequest(by=name1, to=name2, accepted=False, booking_id=id)
    queryset = Frequest.objects.filter(
        by__iexact=name1,
        to__iexact=name2,
    )
    if not queryset:
        obj.save()
    return redirect('cabs:notifications')


@login_required(login_url="/cabs/login/")
def requestpage_view(request):
    queryset1 = Frequest.objects.filter(
        to=request.user.username
    )
    queryset2 = Grequest2.objects.filter(
        Q(to1=request.user.username) | Q(to2=request.user.username)
    )
    queryset3 = Grequest3.objects.filter(
        Q(to1=request.user.username) | Q(to2=request.user.username) | Q(to3=request.user.username)
    )
    context = {
        "request_list": queryset1,
        "Grequest2_list": queryset2,
        "Grequest3_list": queryset3,
        "title": "Booking requests"
    }
    return render(request, 'requests.html', context)


@login_required(login_url="/cabs/login/")
def Rcancel_view(request, id):
    obj = get_object_or_404(Frequest, id=id)
    obj.delete()
    return redirect('cabs:requestpage')


@login_required(login_url="/cabs/login/")
def Fgroup2_view(request, bid, name1, name2, rid):
    obj1 = get_object_or_404(Post, id=bid)
    obj2 = get_object_or_404(Post, created_by=name1, time__hour__range=(obj1.time.hour - 1, obj1.time.hour + 1))
    obj3 = get_object_or_404(Frequest, id=rid)
    obj4 = Fgroup2(created_by1=name2, created_by2=name1,
                   passengers1=obj1.passengers, passengers2=obj2.passengers,
                   time1=obj1.time, time2=obj2.time, gender1=obj1.gender, gender2=obj2.gender,
                   pickup_from1=obj1.pickup_from, pickup_from2=obj2.pickup_from,
                   date=obj1.date, destination=obj1.destination, total_passengers=obj1.passengers + obj2.passengers)
    obj4.save()
    obj1.delete()
    obj2.delete()
    obj3.delete()
    return redirect('cabs:requestpage')


@login_required(login_url="/cabs/login/")
def groups_view(request):
    queryset1 = Fgroup2.objects.filter(
        Q(created_by1__iexact=request.user.username) | Q(created_by2__iexact=request.user.username)
    )
    queryset2 = Fgroup3.objects.filter(
        Q(created_by1__iexact=request.user.username) | Q(created_by2__iexact=request.user.username)
        | Q(created_by3__iexact=request.user.username)
    )
    queryset3 = Fgroup4.objects.filter(
        Q(created_by1__iexact=request.user.username) | Q(created_by2__iexact=request.user.username)
        | Q(created_by3__iexact=request.user.username) | Q(created_by4__iexact=request.user.username)
    )
    context = {
        "groups2_list": queryset1,
        "groups3_list": queryset2,
        "groups4_list": queryset3,
        "title": "Your groups"
    }
    return render(request, 'groups.html', context)


@login_required(login_url="/cabs/login/")
def Gcancel_view(request, id):
    obj = get_object_or_404(Fgroup2, id=id)
    if obj.created_by1 == request.user.username:
        obj1 = Post(passengers=obj.passengers2, created_by=obj.created_by2,
                    pickup_from=obj.pickup_from2, gender=obj.gender2,
                    date=obj.date, time=obj.time2, destination=obj.destination)
    if obj.created_by2 == request.user.username:
        obj1 = Post(passengers=obj.passengers1, created_by=obj.created_by1,
                    pickup_from=obj.pickup_from1, gender=obj.gender1,
                    date=obj.date, time=obj.time1, destination=obj.destination)
    obj1.save()
    obj.delete()
    return redirect('cabs:groups')


@login_required(login_url="/cabs/login/")
def Grequest2_view(request, requester, name1, name2, id):
    obj = Grequest2(by=requester, to1=name1, to2=name2, accepted=False, booking_id=id)
    queryset = Grequest2.objects.filter(
        by__iexact=requester,
        to1__iexact=name1,
        to2__iexact=name2,
    )
    if not queryset:
        obj.save()
    return redirect('cabs:notifications')


@login_required(login_url="/cabs/login/")
def Fgroup3_view(request, bid, name1, name2, name3, rid):
    obj2 = get_object_or_404(Fgroup2, id=bid)
    obj1 = get_object_or_404(Post, created_by=name1, time__hour__range=(obj2.time1.hour - 1, obj2.time1.hour + 1))
    obj3 = get_object_or_404(Grequest2, id=rid)
    obj4 = Fgroup3(created_by1=name1, created_by2=name2, created_by3=name3,
                   passengers1=obj1.passengers, passengers2=obj2.passengers1, passengers3=obj2.passengers2,
                   time1=obj1.time, time2=obj2.time1, time3=obj2.time2,
                   gender1=obj1.gender, gender2=obj2.gender1, gender3=obj2.gender2,
                   pickup_from1=obj1.pickup_from, pickup_from2=obj2.pickup_from1, pickup_from3=obj2.pickup_from2,
                   date=obj1.date, destination=obj1.destination,
                   total_passengers=obj1.passengers + obj2.passengers1 + obj2.passengers2)
    obj4.save()
    obj1.delete()
    obj2.delete()
    obj3.delete()
    return redirect('cabs:requestpage')


@login_required(login_url="/cabs/login/")
def Gcancel3_view(request, id):
    obj1 = get_object_or_404(Fgroup3, id=id)
    if obj1.created_by1 == request.user.username:
        obj2 = Fgroup2(created_by1=obj1.created_by2, created_by2=obj1.created_by3,
                       passengers1=obj1.passengers2, passengers2=obj1.passengers3,
                       time1=obj1.time2, time2=obj1.time3, gender1=obj1.gender2, gender2=obj1.gender3,
                       pickup_from1=obj1.pickup_from2, pickup_from2=obj1.pickup_from3,
                       date=obj1.date, destination=obj1.destination,
                       total_passengers=obj1.passengers2 + obj1.passengers3)
    if obj1.created_by2 == request.user.username:
        obj2 = Fgroup2(created_by1=obj1.created_by1, created_by2=obj1.created_by3,
                       passengers1=obj1.passengers1, passengers2=obj1.passengers3,
                       time1=obj1.time1, time2=obj1.time3, gender1=obj1.gender1, gender2=obj1.gender3,
                       pickup_from1=obj1.pickup_from1, pickup_from2=obj1.pickup_from3,
                       date=obj1.date, destination=obj1.destination,
                       total_passengers=obj1.passengers1 + obj1.passengers3)
    if obj1.created_by3 == request.user.username:
        obj2 = Fgroup2(created_by1=obj1.created_by2, created_by2=obj1.created_by1,
                       passengers1=obj1.passengers2, passengers2=obj1.passengers1,
                       time1=obj1.time2, time2=obj1.time1, gender1=obj1.gender2, gender2=obj1.gender1,
                       pickup_from1=obj1.pickup_from2, pickup_from2=obj1.pickup_from1,
                       date=obj1.date, destination=obj1.destination,
                       total_passengers=obj1.passengers2 + obj1.passengers1)
    obj2.save()
    obj1.delete()
    return redirect('cabs:groups')


@login_required(login_url="/cabs/login/")
def Grequest3_view(request, requester, name1, name2, name3, id):
    obj = Grequest3(by=requester, to1=name1, to2=name2, to3=name3, accepted=False, booking_id=id)
    queryset = Grequest3.objects.filter(
        by__iexact=requester,
        to1__iexact=name1,
        to2__iexact=name2,
        to3__iexact=name3,
    )
    if not queryset:
        obj.save()
    return redirect('cabs:notifications')


@login_required(login_url="/cabs/login/")
def Fgroup4_view(request, bid, name1, name2, name3, name4, rid):
    obj2 = get_object_or_404(Fgroup3, id=bid)
    obj1 = get_object_or_404(Post, created_by=name1, time__hour__range=(obj2.time1.hour - 1, obj2.time1.hour + 1))
    obj3 = get_object_or_404(Grequest3, id=rid)
    obj4 = Fgroup4(created_by1=name1, created_by2=name2, created_by3=name3, created_by4=name4,
                   passengers1=obj1.passengers, passengers2=obj2.passengers1, passengers3=obj2.passengers2,
                   passengers4=obj2.passengers3,
                   time1=obj1.time, time2=obj2.time1, time3=obj2.time2, time4=obj2.time3,
                   gender1=obj1.gender, gender2=obj2.gender1, gender3=obj2.gender2, gender4=obj2.gender3,
                   pickup_from1=obj1.pickup_from, pickup_from2=obj2.pickup_from1, pickup_from3=obj2.pickup_from2,
                   pickup_from4=obj2.pickup_from3,
                   date=obj1.date, destination=obj1.destination,
                   total_passengers=obj1.passengers + obj2.passengers1 + obj2.passengers2 + obj2.passengers3)
    obj4.save()
    obj1.delete()
    obj2.delete()
    obj3.delete()
    return redirect('cabs:requestpage')


@login_required(login_url="/cabs/login/")
def Gcancel4_view(request, id):
    obj1 = get_object_or_404(Fgroup4, id=id)
    if obj1.created_by1 == request.user.username:
        obj2 = Fgroup3(created_by1=obj1.created_by2, created_by2=obj1.created_by3, created_by3=obj1.created_by4,
                       passengers1=obj1.passengers2, passengers2=obj1.passengers3, passengers3=obj1.passengers4,
                       time1=obj1.time2, time2=obj1.time3, time3=obj1.time4,
                       gender1=obj1.gender2, gender2=obj1.gender3, gender3=obj1.gender4,
                       pickup_from1=obj1.pickup_from2, pickup_from2=obj1.pickup_from3, pickup_from3=obj1.pickup_from4,
                       date=obj1.date, destination=obj1.destination,
                       total_passengers=obj1.passengers2 + obj1.passengers3 + obj1.passengers4)
    if obj1.created_by2 == request.user.username:
        obj2 = Fgroup3(created_by1=obj1.created_by1, created_by2=obj1.created_by3, created_by3=obj1.created_by4,
                       passengers1=obj1.passengers1, passengers2=obj1.passengers3, passengers3=obj1.passengers4,
                       time1=obj1.time1, time2=obj1.time3, time3=obj1.time4,
                       gender1=obj1.gender1, gender2=obj1.gender3, gender3=obj1.gender4,
                       pickup_from1=obj1.pickup_from1, pickup_from2=obj1.pickup_from3, pickup_from3=obj1.pickup_from4,
                       date=obj1.date, destination=obj1.destination,
                       total_passengers=obj1.passengers1 + obj1.passengers3 + obj1.passengers4)

    if obj1.created_by3 == request.user.username:
        obj2 = Fgroup3(created_by1=obj1.created_by2, created_by2=obj1.created_by1, created_by3=obj1.created_by4,
                       passengers1=obj1.passengers2, passengers2=obj1.passengers1, passengers3=obj1.passengers4,
                       time1=obj1.time2, time2=obj1.time1, time3=obj1.time4,
                       gender1=obj1.gender2, gender2=obj1.gender1, gender3=obj1.gender4,
                       pickup_from1=obj1.pickup_from2, pickup_from2=obj1.pickup_from1, pickup_from3=obj1.pickup_from4,
                       date=obj1.date, destination=obj1.destination,
                       total_passengers=obj1.passengers2 + obj1.passengers1 + obj1.passengers4)
    if obj1.created_by4 == request.user.username:
        obj2 = Fgroup3(created_by1=obj1.created_by2, created_by2=obj1.created_by3, created_by3=obj1.created_by1,
                       passengers1=obj1.passengers2, passengers2=obj1.passengers3, passengers3=obj1.passengers1,
                       time1=obj1.time2, time2=obj1.time3, time3=obj1.time1,
                       gender1=obj1.gender2, gender2=obj1.gender3, gender3=obj1.gender1,
                       pickup_from1=obj1.pickup_from2, pickup_from2=obj1.pickup_from3, pickup_from3=obj1.pickup_from1,
                       date=obj1.date, destination=obj1.destination,
                       total_passengers=obj1.passengers2 + obj1.passengers3 + obj1.passengers1)

    obj2.save()
    obj1.delete()
    return redirect('cabs:groups')
