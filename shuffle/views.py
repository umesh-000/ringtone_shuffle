from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from shuffle import models
import logging
import json


logger = logging.getLogger(__name__)
User = get_user_model()


def index(request):
    return redirect('admin_login')

def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Retrieve the checkbox value
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.status == 1 and user.is_superuser:
                auth_login(request, user)
                # Set session expiry based on remember me
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day in seconds
                else:
                    request.session.set_expiry(0)  # Session expires when the browser closes
                messages.success(request, "Login Successfully!")
                return redirect('admin_dashboard')
            elif user.status == 0 and user.is_superuser:
                messages.error(request, "Your account is inactive. Please contact the admin.")
            else:
                messages.error(request, "Only admins can log in.")
        else:
            messages.error(request, "Invalid email or password")

        return redirect('admin_login')

    return render(request, "login.html")



@login_required(login_url='admin_login')
def dashboard(request):
    # Fetch data from models
    total_ringtones = models.Ringtone.objects.count()
    total_Ringtone_Language = models.Ringtone_Language.objects.count()
    admin_count = models.CustomUser.objects.filter(user_type='Admin', is_superuser=True, is_staff=True).count()
    all_users = models.CustomUser.objects.filter(user_type='User', is_superuser=False)
    
    # Get the last 5 users
    last_users = all_users.order_by('-created_at')[:5]
    user_count = all_users.count()

    # Annotate each user with the time since they registered
    for user in last_users:
        user.time_since_registration = timesince(user.created_at) + " ago"

    print(request.user)
    # Prepare context with user data
    context = {
        'total_ringtones': total_ringtones,
        'total_Ringtone_Language': total_Ringtone_Language,
        'admin_count': admin_count,
        'user_count': user_count,
        'users': last_users,
        'current_user': request.user
    }

    return render(request, "admin/dashboard.html", context)


@login_required
def ringtone_lan(request):
    ringtone_languages = models.Ringtone_Language.objects.all()
    total_records = ringtone_languages.count() 
    # Pagination logic
    paginator = Paginator(ringtone_languages, 10)
    page_number = request.GET.get('page')
    ringtone_languages = paginator.get_page(page_number)

    context = {
        'ringtone_languages' :ringtone_languages,
        'total_records': total_records,
        'paginator': paginator,
        'current_user': request.user        
    }
    return render(request,"admin/ringtone_languages_list.html",context)

@login_required
def ringtone_lan_create(request):
    if request.method == 'POST':
        lan_name = request.POST.get('lan_name')
        # status = request.POST.get('status')
       
        if lan_name:
            # Create a new Category instance
            models.Ringtone_Language.objects.create(
                language_name=lan_name,
            )
            messages.success(request, 'Language created successfully!')
            return redirect('ringtone_lan_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    context = {
        'current_user': request.user
    }
    return render(request, 'admin/ringtone_languages_create.html',context)

@login_required
def ringtone_lan_create(request):
    if request.method == 'POST':
        lan_name = request.POST.get('lan_name')
        img = request.FILES.get('language_img')
        if lan_name and img:
            if models.Ringtone_Language.objects.filter(language_name=lan_name).exists():
                messages.error(request, 'This language already exists.')
            else:
                models.Ringtone_Language.objects.create( language_name=lan_name, image=img )
                messages.success(request, 'Language created successfully!')
                return redirect('ringtone_lan_list')
        else:
            messages.error(request, 'Please fill in all required fields and upload an image.')
    context = { 'current_user': request.user }
    return render(request, 'admin/ringtone_languages_create.html', context)

@login_required
def ringtone_lan_edit(request, id):
    ringtone_language = get_object_or_404(models.Ringtone_Language, id=id)
    if request.method == 'POST':
        language_name = request.POST.get('language_name')
        status = request.POST.get('status')
        image = request.FILES.get('language_img')
        ringtone_language.language_name = language_name
        ringtone_language.status = status
        if image:
            ringtone_language.image = image
        ringtone_language.save()
        messages.success(request, 'Language updated successfully!')
        return redirect('ringtone_lan_list')
    context = {
        'current_user': request.user,
        'ringtone_language': ringtone_language,
    }
    return render(request, 'admin/ringtone_languages_edit.html', context)



@login_required
def ringtone_lan_delete(request, id):
    if request.method == 'POST':
        try:
            ringtone_language = get_object_or_404(models.Ringtone_Language, id=id)
            ringtone_language.delete()
            logger.info(f"Deleted Ringtone Language {id}")
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            logger.error(f"Error deleting language {id}: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)})
    logger.warning("Invalid request method for ringtone language")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
@csrf_exempt
def update_status(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_status = data.get('status')
        try:
            ringtone_language = models.Ringtone_Language.objects.get(id=id)
            ringtone_language.status = new_status
            ringtone_language.save()
            return JsonResponse({'message': 'Status updated successfully!'})
        except models.Category.DoesNotExist:
            return JsonResponse({'message': 'Language not found!'}, status=404)

    return JsonResponse({'message': 'Invalid request method!'}, status=405)




@login_required
def ringtones(request):
    ringtones_list = models.Ringtone.objects.all() 
    total_records = ringtones_list.count()
    
    # Pagination logic
    paginator = Paginator(ringtones_list, 10)
    page_number = request.GET.get('page')
    ringtones = paginator.get_page(page_number)

    context = {
        'ringtones': ringtones,
        'total_records': total_records,
        'paginator': paginator,
        'current_user': request.user
    }
    return render(request, 'admin/ringtones_list.html', context)

@login_required
def get_cities_by_state(request):
    state_id = request.GET.get('state_id')
    print(state_id)
    cities = models.City.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse({'cities': list(cities)})

@login_required
def create_ringtone(request):
    if request.method == 'GET':
        states = models.State.objects.all()
        ringtone_languages = models.Ringtone_Language.objects.all()

        context = {
            'states': states,
            'ringtone_languages': ringtone_languages,
            'current_user': request.user
        }
        return render(request, 'admin/ringtones_create.html', context)

    elif request.method == 'POST':
        is_all_india = request.POST.get('is_all_india') == 'on'
        state_id = request.POST.get('state')
        city_id = request.POST.get('city')
        language_name_id = request.POST.get('language_name')
        ringtone_title = request.POST.get('ringtone_title')
        # audio_type = request.POST.get('audio_type')
        audio_type = "file"
        is_hyped = request.POST.get('is_hyped') == 'on'
        
        # Ensure play_times is converted to an integer, defaulting to 0 if not provided
        try:
            play_times = int(request.POST.get('play_times', 0))
        except ValueError:
            play_times = 0
        
        ringtone_year_from = request.POST.get('ringtone_year_from')
        ringtone_year_to = request.POST.get('ringtone_year_to')

        # Handle file upload or URL based on the selected audio type
        ringtone_file = request.FILES.get('ringtone_file') if audio_type == 'file' else None
        ringtone_url = request.POST.get('ringtone_url') if audio_type == 'url' else None

        # Get the Ringtone_Language instance
        try:
            ringtone_language = models.Ringtone_Language.objects.get(id=language_name_id)
        except models.Ringtone_Language.DoesNotExist:
            messages.error(request, 'Selected language does not exist.')
            return redirect('ringtones_create')

        # Create a new ringtone instance
        ringtone = models.Ringtone(
            is_all=is_all_india,
            state_id=state_id,
            city_id=city_id,
            ringtone_language=ringtone_language,  # Use the instance, not the ID
            ringtone_title=ringtone_title,
            audio_type=audio_type,
            is_hyped=is_hyped,
            play_times=play_times,
            ringtone_year_start=ringtone_year_from,
            ringtone_year_end=ringtone_year_to,
        )

        if ringtone_file:
            ringtone.ringtone_file = ringtone_file
        if ringtone_url:
            ringtone.ringtone_url = ringtone_url

        ringtone.save()
        messages.success(request, 'Ringtone created successfully!')
        return redirect('ringtones_list')

@login_required
def ringtones_edit(request, id):
    ringtone = get_object_or_404(models.Ringtone, id=id)
    states = models.State.objects.all()
    ringtone_languages = models.Ringtone_Language.objects.all()
    context = {
        'states': states,
        'ringtone_languages': ringtone_languages,
        'ringtone': ringtone,
        'current_user': request.user
    }

    if request.method == 'GET':
        return render(request, 'admin/ringtones_edit.html', context)

    elif request.method == 'POST':
        logger.debug("POST data: %s", request.POST)
        logger.debug("FILES data: %s", request.FILES)
        # Retrieve form data
        is_all_india = request.POST.get('is_all_india') == 'on'
        state_id = request.POST.get('state')
        city_id = request.POST.get('city')
        language_name = request.POST.get('language_name')
        ringtone_year_from = request.POST.get('ringtone_year_from')
        ringtone_year_to = request.POST.get('ringtone_year_to')
        ringtone_title = request.POST.get('ringtone_title')
        audio_type = "file"
        # audio_type = request.POST.get('audio_type')
        is_hyped = request.POST.get('is_hyped') == 'on'
        play_times = request.POST.get('play_times', 1)

        ringtone_file = request.FILES.get('ringtone_file') if audio_type == 'file' else None
        ringtone_url = request.POST.get('ringtone_url') if audio_type == 'url' else None
        
        # Update the ringtone instance
        ringtone.is_all = is_all_india
        
        if not is_all_india:
            if state_id:
                ringtone.state = get_object_or_404(models.State, id=state_id)
            if city_id:
                ringtone.city = get_object_or_404(models.City, id=city_id)
        else:
            ringtone.state = None
            ringtone.city = None

        if language_name:
            ringtone.ringtone_language = get_object_or_404(models.Ringtone_Language, id=language_name)

        ringtone.ringtone_title = ringtone_title
        ringtone.ringtone_year_start = ringtone_year_from
        ringtone.ringtone_year_end = ringtone_year_to
        ringtone.is_hyped = is_hyped
        ringtone.play_times = play_times or 0

        if ringtone_file:
            fs = FileSystemStorage()
            filename = fs.save(ringtone_file.name, ringtone_file)
            ringtone.ringtone_file = filename
        
        # If using a URL, update it accordingly
        if audio_type == 'url':
            ringtone.ringtone_url = ringtone_url

        try:
            ringtone.save()
            messages.success(request, 'Ringtone updated successfully!')
            return redirect('ringtones_list')
        except Exception as e:
            messages.error(request, f'Error updating ringtone: {e}')
            return redirect('ringtones_edit', id=id)

    return render(request, 'admin/ringtones_edit.html', context)



@login_required
def ringtones_delete(request, id):
    if request.method == 'POST':
        try:
            ringtone = get_object_or_404(models.Ringtone, id=id)
            ringtone.delete()
            logger.info(f"Deleted ringtone {id}")
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            logger.error(f"Error deleting ringtone {id}: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)})
    logger.warning("Invalid request method for delete ringtone")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
@csrf_exempt
def ringtone_update_status(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_status = data.get('status')
        try:
            ringtone = models.Ringtone.objects.get(id=id)
            ringtone.status = new_status
            ringtone.save()
            return JsonResponse({'message': 'Status updated successfully!'})
        except models.Ringtone.DoesNotExist:
            return JsonResponse({'message': 'Ringtone not found!'}, status=404)

    return JsonResponse({'message': 'Invalid request method!'}, status=405)


@login_required
def notification_create(request):
    if request.method == 'GET':
        context ={
            'current_user': request.user
        }
        return render(request, 'admin/notification_create.html',context)

    elif request.method == 'POST':
        # Get the notification title and message from the form
        notification_title = request.POST.get('notification_title')
        notification_msg = request.POST.get('notification_msg')
        
        # Get the uploaded image file
        image = request.FILES.get('image')

        print(notification_title,notification_msg,image)

        if notification_title:
            if image:
                fs = FileSystemStorage()
                image_name = fs.save(image.name, image)
            else:
                image_name = None

        # Create a new Notification instance
        notification = models.Notification(
            # user=request.user,  # Associate the notification with the logged-in user
            notification_title=notification_title,
            notification_msg=notification_msg,
            image=image_name
        )

        try:
            notification.save()
            messages.success(request, 'Notification created successfully!')
            return redirect('notification_create')
        except Exception as e:
            messages.error(request, f'Error creating notification: {e}')
            return redirect('notification_create')
    return render(request, 'admin/create_notification.html',context)


def users(request):
    users_list = User.objects.filter(is_superuser=False).order_by('-created_at')
    total_users = users_list.count()
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users_list = paginator.get_page(page_number)
    context = {
        'users': users_list,
        'total_users': total_users,
        'paginator': paginator,
        'current_user': request.user
    }
    
    return render(request, 'admin/users_list.html', context)

@login_required
def create_users(request):
    if request.method == 'GET':
        context = {
            'current_user': request.user
        }
        return render(request, 'admin/users_create.html', context)

    elif request.method == 'POST':
        # Extract form data
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        user_phone = request.POST.get('user_phone')
        user_dob = request.POST.get('user_dob')
        user_gender = request.POST.get('user_gender')
        password = request.POST.get('password')
        profile_img = request.FILES.get('profile_img')
        user_type = 'User'
        
        # Save the image if uploaded
        profile_img_name = None
        if profile_img:
            fs = FileSystemStorage()
            profile_img_name = fs.save(profile_img.name, profile_img)
        
        # Create user
        try:
            user = models.CustomUser.objects.create_user(
                email=email,
                user_name=user_name,
                user_phone=user_phone,
                user_gender=user_gender,
                user_dob = user_dob,
                password=password,
                profile_img=profile_img_name,
                user_type=user_type
            )
            messages.success(request, 'User created successfully!')
            return redirect('users_list')
        except Exception as e:
            messages.error(request, f'Error creating user: {e}')
            return redirect('users_create')

    return render(request, 'admin/users_create.html', context)


@login_required
def users_edit(request, id):
    user = get_object_or_404(models.CustomUser, id=id)

    if request.method == 'GET':
        context = {
            'user': user,
            'current_user': request.user
        }
        return render(request, 'admin/users_edit.html', context)

    elif request.method == 'POST':
        user_phone = request.POST.get('user_phone')
        user_dob = request.POST.get('user_dob')
        user_gender = request.POST.get('user_gender')
        password = request.POST.get('password')
        status = request.POST.get('status')
        profile_img = request.FILES.get('profile_img')

        # Update profile image if uploaded
        if profile_img:
            fs = FileSystemStorage()
            profile_img_name = fs.save(profile_img.name, profile_img)
            user.profile_img = profile_img_name

        # Update the user's fields
        user.user_phone = user_phone
        user.user_gender = user_gender
        user.user_dob = user_dob
        user.status = status

        # Only update the password if provided
        if password:
            user.set_password(password)

        try:
            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('users_list')
        except Exception as e:
            messages.error(request, f'Error updating user: {e}')
            return redirect('users_edit', id=user.id)
    return render(request, 'admin/users_edit.html', context)

@login_required
def users_delete(request, id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(models.CustomUser, id=id)
            user.delete()
            logger.info(f"Deleted user {id}")
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            logger.error(f"Error deleting user {id}: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)})
    logger.warning("Invalid request method for delete user")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
def admins(request):
    admin_list = models.CustomUser.objects.filter( user_type='Admin', is_superuser=True, is_staff=True ).order_by('user_name')
    total_admins = admin_list.count()
    paginator = Paginator(admin_list, 10)
    page_number = request.GET.get('page')
    admin_list = paginator.get_page(page_number)
    context = {
        'admins': admin_list,
        'total_admins': total_admins,
        'paginator': paginator,
        'current_user': request.user
    }
    return render(request, 'admin/admin_list.html', context)

@login_required
def admins_create(request):
    if request.method == 'GET':
        context = {
            'current_user': request.user
        }
        return render(request, 'admin/admin_create.html', context)

    elif request.method == 'POST':
        # Extract form data
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        
        user_type = 'Admin'
        password = request.POST.get('password')
        profile_img = request.FILES.get('profile_img')
        
        # Save the image if uploaded
        profile_img_name = None
        if profile_img:
            fs = FileSystemStorage()
            profile_img_name = fs.save(profile_img.name, profile_img)
        
        # Create admin
        try:
            admin = models.CustomUser.objects.create_user(
                email=email,
                user_name=user_name,
                password=password,
                profile_img=profile_img_name,
                user_type=user_type,
                is_staff = True,
                is_superuser = True
            )
            messages.success(request, 'Admin created successfully!')
            return redirect('admins_list')
        except Exception as e:
            messages.error(request, f'Error creating user: {e}')
            return redirect('admins_create')

    return render(request, 'admin/admin_create.html',context)

@login_required
def admins_edit(request, id):
    admin = get_object_or_404(models.CustomUser, id=id)

    if request.method == 'GET':
        context = {
            'admin': admin,
            'current_user': request.user
        }
        return render(request, 'admin/admin_edit.html', context)

    elif request.method == 'POST':
        user_phone = request.POST.get('user_phone')
        user_gender = request.POST.get('user_gender')
        password = request.POST.get('password')
        status = request.POST.get('status')
        profile_img = request.FILES.get('profile_img')

        # Update profile image if uploaded
        if profile_img:
            fs = FileSystemStorage()
            profile_img_name = fs.save(profile_img.name, profile_img)
            admin.profile_img = profile_img_name

        admin.status = status

        # Only update the password if provided
        if password:
            admin.set_password(password)
        if user_phone:
            admin.user_phone = user_phone
        if user_gender:
            admin.user_gender = user_gender

        try:
            admin.save()
            messages.success(request, 'Admin updated successfully!')
            return redirect('admins_list')
        except Exception as e:
            messages.error(request, f'Error updating user: {e}')
            return redirect('admin_edit', id=admin.id)
    return render(request, 'admin/admin_edit.html', context)


# @login_required
# def admins_delete(request, id):
#     if request.method == 'POST':
#         try:
#             user = get_object_or_404(models.CustomUser, id=id)
#             user.delete()
#             logger.info(f"Deleted user {id}")
#             return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
#         except Exception as e:
#             logger.error(f"Error deleting user {id}: {str(e)}")
#             return JsonResponse({'success': False, 'message': str(e)})
#     logger.warning("Invalid request method for delete user")
#     return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def change_password(request, id):
    admin = get_object_or_404(models.CustomUser, id=id)
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the old password is correct
        if not admin.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            # Set the new password
            admin.set_password(new_password)
            admin.save()
            messages.success(request, 'Password changed successfully.')

            # Update session to keep the user logged in
            update_session_auth_hash(request, admin)

            return redirect('dashboard')  # Redirect to the dashboard or another page after success

    context = {
        'admin': admin,
        'current_user': request.user
    }
    return render(request, 'admin/change_password.html', context)


def reports(request):
    users_list = User.objects.filter(is_superuser=False).order_by('-created_at')
    total_users = users_list.count()
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users_list = paginator.get_page(page_number)
    context = {
        'users': users_list,
        'total_users': total_users,
        'paginator': paginator,
        'current_user': request.user
    }
    
    return render(request, 'admin/reprots_list.html', context)