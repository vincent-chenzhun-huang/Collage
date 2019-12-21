from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact


def user_login(request):
    if request.method == 'POST':  # If the user is trying to log in
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])  # Use Django's built-in authentication system
            if user is not None:  # if the user exists
                if user.is_active:  # if the user is active, log in the user and send the message
                    login(request, user)
                    return HttpResponse('Authenticated '
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')  # if the user is inactive, return the message
            else:
                return HttpResponse('Invalid login')  # Show the invalid credential
    else:
        form = LoginForm()  # load the login form if the method is GET
    return render(request, 'registration/login.html', {'form': form})  # render the corresponding page with the form
    # attached


@login_required  # make the dashboard login required so that only logged in users can access the content
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    """
    User signup view,
    use Django's built-in registration form
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)  # create a user registration form and validate
        if user_form.is_valid():
            new_user = user_form.save(commit=False)  # if valid, save the form but not to the database
            new_user.set_password(
                user_form.cleaned_data['password']
            )  # set the password for the user
            new_user.save()  # commit the save to the database
            Profile.objects.create(user=new_user)  # Create a new user profile in Profile model
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})  # render the page with the new_user object passed
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    """This form lets users modify their credentials after created"""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_list(request):
    """Get the list of users visible."""
    users = User.objects.filter(is_active=True)  # Only display the list of active users
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    """Get the information passed in the request and create the Contact object to keep track of the follower count"""
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user)
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})
