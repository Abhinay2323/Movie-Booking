from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login,logout,authenticate
from .forms import UserForm,UserchangeForm,UserprofilechangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
import requests,json
from django.core.mail import EmailMessage
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
import time



class MovieListView(ListView):
    model = movie
    template_name = 'index.html'
    context_object_name = 'movie'

class MovieDetailView(DetailView):
    model = movie
    template_name = 'Movie_page.html'
    context_object_name = 'movie'

#------------------------------------------------------------------------------------------------------------------------
def main_page(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    return render(request, 'LoginHome.html')

#------------------------------------------------------------------------------------------------------------------------

def about_page(request):
    return render(request, 'about.html')


def movies_events(request):
    return render(request, 'movies_events.html')

def contact(request):
    return render(request, 'contact.html')


def user_logout(request):
    logout(request)
    return redirect(reverse('main_page'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            messages.error(request, 'username or password is not correct')
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})


def signup(request):
    registered=False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid()and user_form.cleaned_data['password'] == user_form.cleaned_data['confirm_password']:
            user = user_form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            user.save()
            registered=True
            current_site = get_current_site(request)
            domain = current_site.domain
            print(domain)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            name = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            print(name)
            print(password)
            response = requests.get(
                "http://api.quickemailverification.com/v1/verify?email=" + to_email + "&apikey=15aef1e3ebf4f0e3357b6aab94bb77833e639fc261b2d32903e1895bd330")
            result = response.json()

            if (result['did_you_mean'] == '' and result['result'] == "valid"):

                mail_subject = 'Activate your blog account.'
                to_email = user_form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return render(request, 'emailsent.html', {})

            else:
                try:
                    u = User.objects.get(username=name)
                    u.delete()
                except User.DoesNotExist:
                    return HttpResponse('The email given is invalid please check it ')
                except Exception as e:
                    return render(request, 'signup.html', {'user_form': user_form})
                return HttpResponse('The email given is invalid please check it ')
        elif user_form.data['password'] != user_form.data['confirm_password']:
            user_form.add_error('confirm_password', 'The passwords do not match')

    else:
        user_form = UserForm()
    return render(request, 'signup.html', {'user_form': user_form, 'registered': registered})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request,user)
        return HttpResponseRedirect(reverse('home'))

    else:
        return HttpResponse('Activation link is invalid!')

#------------------------------------------------------------------------------------------------------------------------


@csrf_exempt
class IndexView(DetailView):
    model = User
    template_name = 'LoginHome.html'


@login_required
def home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'LoginHome.html', context=context)




@login_required
def viewprofile(request):
    args = {'user': request.user}
    return render(request, 'viewprofile.html', args)


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserchangeForm(request.POST, instance=request.user)
        user_profile_form=UserprofilechangeForm(request.POST,instance=profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()

            messages.success(
                request, ('Your profile was successfully updated!'))

            return redirect('viewprofile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserchangeForm(instance=request.user)
        user_profile_form=UserprofilechangeForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,'user_profile_form':user_profile_form

    })


@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Imp
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('viewprofile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

#------------------------------------------------------------------------------------------------------------------------


def home2(request):
    city='Visakhapatnam'
    theatre_city = theatre.objects.filter(city=city).order_by('now_playing').values('now_playing').distinct()
    movie_list=[]
    for each in theatre_city:
        movie_list.append(movie.objects.get(pk=each['now_playing']))
    top_five=5
    new_releases=[None,None,None,None,None]
    most_popular=[None,None,None,None,None]

    for i in range(len(movie_list)):
        if i<top_five:
            new_releases[i]=movie_list[i]
            most_popular[i]=movie_list[i]
        else:
            for j in range(top_five):
                if (float(movie_list[i].imdb_movie_rating)>float(most_popular[j].imdb_movie_rating)):
                    most_popular[j]=movie_list[i]
                if(int(time.mktime(movie_list[i].movie_release_date.timetuple()) * 1000) < int(time.mktime(new_releases[j].movie_release_date.timetuple()) * 1000)):
                    new_releases[j] = movie_list[i]
    context={'city':city,'new_releases':new_releases,'most_popular':most_popular}
    print(most_popular[0].movie_poster_1)
    return render(request,'fake_login_home.html',context)