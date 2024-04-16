from django.shortcuts import render, redirect, get_object_or_404
from authapp.models import *
from authapp.forms import *
from django.contrib.auth import authenticate, login, logout
from authapp.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.contrib import messages
from core.decorators import admin_role_required, both_role_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from settings.models import websiteSetting
from django.urls import reverse
from authapp.utils import generate_reset_token_and_send_email
from legals.models import agreementSettings
# Users List
@login_required(login_url='signIn')
@admin_role_required
def usersList(request):
        users = UserProfile.objects.all()
        # Retrieve messages and add them to the context
        messages_data = messages.get_messages(request)
        context = {
            'title': 'Users',
            'users': users,
            'messages' : messages_data
        }
        return render(request, 'crm/main/user/users.html', context)

@login_required(login_url='signIn')
@admin_role_required
def createUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Prevent immediate save
            user.role = form.cleaned_data['role']  # Set role from form
            user.save()  # Save User instance to DB
            messages.success(request, 'User created successfully!')

            # Update or Create a profile for the user
            UserProfile.objects.update_or_create(
                user=user, 
                defaults={
                    'name': form.cleaned_data['name'], 
                    'email': form.cleaned_data['email']
                }
            )

            # Send a welcome email to the user
            web_settings = websiteSetting.objects.first()
            contact_url = request.build_absolute_uri(reverse('contactPageFront'))
            subject = f'Welcome to {web_settings.name}'
            from_email = f'"{web_settings.name}" <{settings.DEFAULT_FROM_EMAIL}>'
            to_email = [form.cleaned_data['email']]
            
            # Load the HTML email template
            html_message = render_to_string('admin/auth/email/welcome.html', {
                'username': form.cleaned_data['username'],
                'settings' : web_settings,
                'contact' : contact_url
            })
            
            email_message = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=from_email,
                to=to_email,
            )
            email_message.content_subtype = 'html'
            email_message.send()

            return redirect('users')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    context = {
        'title': 'Create User',
        'form': form,
    }
    return render(request, 'crm/main/user/create.html', context)

# Edit User
@login_required(login_url='signIn')
@admin_role_required
def editUserProfile(request, slug):
    try:
        profile = UserProfile.objects.get(slug=slug)
        user = profile.user
    except UserProfile.DoesNotExist:
        raise Http404("User profile does not exist")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('editProfile', profile.slug)
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'title': 'Edit User Profile',
        'form': form,
        'profile': profile,
        'user': user,
    }
    return render(request, 'crm/main/user/edit.html', context)

# Change Password
@login_required(login_url='signIn')
def changePassword(request, username):

    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = UserPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('change_password', user)
    else:
        form = UserPasswordChangeForm(user)

    context = {
        'title': 'Change Password',
        'form': form,
        'profile': profile,
        'user': user,
    }
    return render(request, 'crm/main/user/changepassword.html', context)

# User Delete
@login_required(login_url='signIn')
@admin_role_required
def delete_user(request, username):
    user = get_object_or_404(User, username=username)

    # Retrieve the user object or raise 404 exception if not found
    user = get_object_or_404(User, username=username)
    # Delete the user
    user.delete()
    messages.warning(request, 'User deleted!')

    # Redirect to a success page or any desired URL
    return redirect('users')

# User Profile
@login_required(login_url='signIn')
@both_role_required
def userProfile(request):
    user_profile = UserProfile.objects.get(user=request.user)
        
    context = {
        'title' : 'User Profile',
        'profile': user_profile
            }
    return render(request, 'crm/main/user/userProfile.html', context)

# Sign Up/Registration
def SignUp(request):
   a_settings = agreementSettings.objects.first()
   if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('login[password]')
    email = request.POST.get('email')
    if Guser.objects.filter(username__iexact=username):
         messages.warning(request, 'Username already exists')
         return redirect('signUp')
    if Guser.objects.filter(email__iexact=email):
        messages.warning(request, 'Email already exists')
        return redirect('signUp')
    user = Guser.objects.create_user(username = username,  email = email , password=password)
    if user:
        # Send a welcome email to the user
        web_settings = websiteSetting.objects.first()
        login_url = request.build_absolute_uri(reverse('signIn'))
        subject = f'Welcome to {web_settings.name}'
        from_email = f'"{web_settings.name}" <{settings.DEFAULT_FROM_EMAIL}>'
        to_email = [email]
            
        # Load the HTML email template
        html_message = render_to_string('admin/auth/email/welcome.html', {
            'username': username,
            'settings' : web_settings,
            'login' : login_url
            
        })
            
        email_message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=from_email,
            to=to_email,
        )
        email_message.content_subtype = 'html'
        email_message.send()
        return redirect('signIn')         
   return render(request, 'admin/auth/sign-up.html', {'a_settings': a_settings})

# Log In/Sign In
def signIn(request):
    error_message = ''  # Initialize the variable here
    demo_mode = True if 'core.middleware.middleware.DemoModeMiddleware' in settings.MIDDLEWARE else False

    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('login[password]')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'Admin':
                    return redirect('crmHome')
                elif user.role == 'User':
                    return redirect('userDashboard')
            else:
                # Handle invalid login credentials
                error_message = 'Invalid username or password. Try again.'
        else:
            error_message = ''
        
        # Render the login form
        return render(request, 'admin/auth/login.html', {'error_message': error_message, 'demo_mode' : demo_mode})
    else:
        if request.user.role == 'Admin':
            return redirect('crmHome')
        elif request.user.role == 'User':
            return redirect('userDashboard')

# Log Out
@login_required(login_url='signIn')
def logout_view(request):
    logout(request)
    # Redirect the user to a success page or another appropriate page
    return redirect('signIn')

# # # # # # # # # # # # # # # # # #
       # Reset Password #
# # # # # # # # # # # # # # # # # #
def initiate_password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username) 
            generate_reset_token_and_send_email(user, request)
            messages.success(request, 'An email has sent!')
            return redirect('initiate_password_reset') 
        except User.DoesNotExist:
            messages.warning(request, 'Invalid username!')
            return redirect('initiate_password_reset')
    context = {
        'title' : 'Forgot Password'
    }
    return render(request, 'admin/auth/forget-password.html', context)

def reset_password(request, token):
    try:
        password_reset_token = PasswordResetToken.objects.get(token=token)
        if password_reset_token.is_expired():
            messages.warning(request, 'The password reset token has expired. Please initiate the password reset process again.')
            return redirect('password_reset') 

        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 == new_password2:

                user = password_reset_token.user
                user.set_password(new_password1)
                user.save()
                
                update_session_auth_hash(request, user)
                
                password_reset_token.delete()
                messages.success(request, 'Password reset successfully!')
                return redirect('signIn') 
            else:
                messages.warning(request, 'Something went wrong. Please try again.')
                return redirect('reset_password', token=token)
        context = {
            'title' : 'Reset Password'
        }
        return render(request, 'admin/auth/reset.html', context)
    except PasswordResetToken.DoesNotExist:
        messages.warning(request, 'Invalid token. Please ensure you have the correct link.')
        return redirect('initiate_password_reset')
    except Exception as e:
        messages.warning(request, f'An error occurred: {str(e)}')
        return redirect('initiate_password_reset')
    
# ====================Error Page====================
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

def error_500(request):
    return render(request, 'error/error_500.html', status=500)