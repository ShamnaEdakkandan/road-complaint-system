from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Profile,Complaint


# Create your views here.

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.profile.role = role
        user.profile.save()

        return redirect('/login/')

    return render(request, 'register.html')



def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            if user.profile.role == 'engineer':
                return redirect('/engineer-dashboard/')
            else:
                return redirect('/user-dashboard/')

        return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def forgot_password(request):
    message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        message = 'If that username is registered, password reset instructions have been sent to the associated email address.'

    return render(request, 'forgot_password.html', {'message': message})


def user_dashboard(request):

    total_complaints = Complaint.objects.filter(
        user=request.user
    ).count()

    in_progress = Complaint.objects.filter(
        user=request.user,
        status='progress'
    ).count()

    resolved = Complaint.objects.filter(
        user=request.user,
        status='completed'
    ).count()

    return render(
        request,
        'user_dashboard.html',
        {
            'total_complaints': total_complaints,
            'in_progress': in_progress,
            'resolved': resolved,
        }
    )


def engineer_dashboard(request):

    active_complaints = Complaint.objects.filter(
        assigned_to=request.user
    ).exclude(status='completed')

    resolved_complaints = Complaint.objects.filter(
        assigned_to=request.user,
        status='completed'
    )

    return render(
        request,
        'engineer_dashboard.html',
        {
            'active_complaints': active_complaints,
            'resolved_complaints': resolved_complaints
        }
    )


def add_complaint(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        latitude = request.POST.get('latitude') or None
        longitude = request.POST.get('longitude') or None
        image = request.FILES.get('image')

        Complaint.objects.create(
            user=request.user,
            title=title,
            description=description,
            location=location,
            latitude=latitude,
            longitude=longitude,
            image=image
        )

        return redirect('/user-dashboard/')
    return render(request, 'add_complaint.html')

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        image = request.FILES.get('image')

        Complaint.objects.create(
            user=request.user,
            title=title,
            description=description,
            location=location,
            image=image
        )

        return redirect('/user-dashboard/')

    return render(request, 'add_complaint.html')

def my_complaints(request):

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_complaints.html',
        {'complaints': complaints}
    )

def update_status(request, id):

    complaint = Complaint.objects.get(id=id)

    if request.method == 'POST':

        status = request.POST['status']

        complaint.status = status

        complaint.save()

    return redirect('/engineer-dashboard/')

def logout_view(request):

    logout(request)

    return redirect('/login/')