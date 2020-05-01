from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Post,Frequest,Fgroup2

def index(request):
    return render(request,'home.html')


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
            user=form.get_user()
            login(request,user)
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
        form = forms.CreatePost(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.author=request.user
            instance.created_by= request.user.username
            instance.booked = False
            instance.save()
            queryset = Post.objects.filter(
                time__hour__range=(instance.time.hour-1,instance.time.hour+1),
                date=instance.date,
                destination=instance.destination,
                passengers__range=(1,4-instance.passengers)
            ).exclude(created_by__iexact =instance.created_by)
            queryset1 = Fgroup2.objects.filter(
                time1__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
                date=instance.date,
                destination=instance.destination,
                total_passengers__range=(1, 4 - instance.passengers)
            ).exclude(Q(created_by1__iexact=instance.created_by) & Q(created_by2__iexact=instance.created_by))
            context={
                "passenger_list": queryset,
                "groups_list":queryset1,
                "title":"Search Results"
            }
            return render(request,'match.html',context)
    else:
        form = forms.CreatePost()
    return render(request, 'post.html', {'form': form})

@login_required(login_url="/cabs/login/")
def booking_view(request):
    queryset= Post.objects.filter(
        created_by__iexact=request.user.username
    )
    context = {
        "booking_list": queryset,
        "title": "Your bookings"
    }
    return render(request, 'bookings.html', context)

@login_required(login_url="/cabs/login/")
def cancel_view(request,id):
    obj=get_object_or_404(Post,id=id)
    obj.delete()
    return redirect('cabs:bookings')

@login_required(login_url="/cabs/login/")
def notification_view(request):
    i = Post.objects.filter(
        created_by__iexact=request.user.username
    )
    query=[]
    for instance in i:
        queryset=Post.objects.filter(
            time__hour__range=(instance.time.hour-1,instance.time.hour+1),
            date=instance.date,
            destination=instance.destination,
            passengers__range=(1, 4 - instance.passengers)
        ).exclude(created_by__iexact=instance.created_by)
        query+=queryset
    query1 = []
    for instance in i:
        queryset =  Fgroup2.objects.filter(
                time1__hour__range=(instance.time.hour - 1, instance.time.hour + 1),
                date=instance.date,
                destination=instance.destination,
                total_passengers__range=(1, 4 - instance.passengers)
            ).exclude(Q(created_by1__iexact=instance.created_by) & Q(created_by2__iexact=instance.created_by))
        query1 += queryset
    context = {
        "passenger_list": query,
        "groups_list": query1,
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
def request_view(request,name1,name2,id):
    obj=Frequest(by=name1,to=name2,accepted=False,booking_id=id)
    queryset = Frequest.objects.filter(
        by__iexact=name1,
        to__iexact=name2,
    )
    if not queryset:
        obj.save()
    return redirect('cabs:notifications')

@login_required(login_url="/cabs/login/")
def requestpage_view(request):
    queryset = Frequest.objects.filter(
        to=request.user.username
    )
    context = {
        "request_list": queryset,
        "title": "Booking requests"
    }
    return render(request, 'requests.html', context)

@login_required(login_url="/cabs/login/")
def Rcancel_view(request,id):
    obj=get_object_or_404(Frequest,id=id)
    obj.delete()
    return redirect('cabs:requestpage')

@login_required(login_url="/cabs/login/")
def Fgroup2_view(request,bid,name1,name2,rid):
    obj1 = get_object_or_404(Post, id=bid)
    obj2 = get_object_or_404(Post,created_by=name1,time__hour__range=(obj1.time.hour-1,obj1.time.hour+1))
    obj3 = get_object_or_404(Frequest, id=rid)
    obj4 = Fgroup2( created_by1=name1,created_by2=name2,
                    passengers1=obj1.passengers, passengers2=obj2.passengers,
                    time1=obj1.time,time2=obj2.time,gender1=obj1.gender,gender2=obj2.gender,
                    pickup_from1=obj1.pickup_from,pickup_from2=obj2.pickup_from,
                    date=obj1.date,destination=obj1.destination,total_passengers=obj1.passengers+obj2.passengers)
    obj4.save()
    obj1.delete()
    obj2.delete()
    obj3.delete()
    return redirect('cabs:requestpage')

@login_required(login_url="/cabs/login/")
def groups_view(request):
    queryset = Fgroup2.objects.filter(
        Q(created_by1__iexact=request.user.username)|Q(created_by2__iexact=request.user.username)
    )
    context = {
        "groups_list": queryset,
        "title": "Your groups"
    }
    return render(request, 'groups.html', context)

@login_required(login_url="/cabs/login/")
def Gcancel_view(request,id):
    obj = get_object_or_404(Fgroup2, id=id)
    obj.delete()
    return redirect('cabs:groups')



