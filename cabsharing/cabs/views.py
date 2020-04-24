from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Post,Frequest

def index(request):
    return render(request,'base.html')


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
            context={
                "passenger_list": queryset,
                "title":"Search Results"
            }
            return render(request,'match.html',context)
    else:
        form = forms.CreatePost()
    return render(request, 'post.html', {'form': form})


def booking_view(request):
    queryset= Post.objects.filter(
        created_by__iexact=request.user.username
    )
    context = {
        "booking_list": queryset,
        "title": "Your bookings"
    }
    return render(request, 'bookings.html', context)


def cancel_view(request,id):
    obj=get_object_or_404(Post,id=id)
    obj.delete()
    return redirect('cabs:bookings')


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
            passengers__range=(1, 3 - instance.passengers)
        ).exclude(created_by__iexact=instance.created_by)
        query+=queryset
    context = {
        "passenger_list": query,
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


def request_view(request,name1,name2,id):
    obj=Frequest(by=name1,to=name2,accepted=False,booking_id=id)
    queryset = Frequest.objects.filter(
        by__iexact=name1,
        to__iexact=name2,
    )
    if not queryset:
        obj.save()
    return redirect('cabs:notifications')



