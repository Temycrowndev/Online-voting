

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Candidate, Vote, Position
from django.contrib.admin.views.decorators import staff_member_required
from .forms import VoteForm
from django.contrib.auth.models import Group






def home_view(request):
    return render(request, 'voting/home.html')


@login_required
def dashboard_view(request):
    user = request.user

    if user.is_superuser or user.is_staff:
        return render(request, 'voting/admin_dashboard.html')

    elif user.groups.filter(name='Candidates').exists():
        return render(request, 'voting/candidate_dashboard.html')

    elif user.groups.filter(name='Voters').exists():
        return render(request, 'voting/voter_dashboard.html')

    else:
        messages.error(request, "You are not assigned to any role group. Contact admin.")
        logout(request)
        return redirect('login')


from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically add to Voters group
            voters_group = Group.objects.get(name='Voters')
            user.groups.add(voters_group)
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'voting/register.html', {'form': form})






def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "You have logged in successfully")
            return redirect("dashboard")  # This will be handled by dashboard_view

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'voting/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out successful!")
    return redirect('login')





@login_required
def vote_view(request):
    if not request.user.groups.filter(name='Voters').exists():
        messages.error(request, "Only voters can access this page.")
        return redirect('dashboard')

    positions = Position.objects.all()
    if request.method == 'POST':
        for position in positions:
            selected_candidate_id = request.POST.get(f'position_{position.id}')

            if selected_candidate_id:
                candidate = Candidate.objects.get(id=selected_candidate_id)
                # Check if this user already voted for this position
                already_voted = Vote.objects.filter(voter=request.user, candidate__position=position).exists()
                if already_voted:
                    messages.warning(request, f"You already voted for {position.name}.")
                else:
                    Vote.objects.create(voter=request.user, candidate=candidate)
                    messages.success(request, f"Vote cast for {position.name}.")
        return redirect('dashboard')

    return render(request, 'voting/vote.html', {'positions': positions})


@login_required()
def results_view(request):
    positions = Position.objects.all()
    combined_results = []

    for position in positions:
        candidates = Candidate.objects.filter(position=position)
        for candidate in candidates:
            combined_results.append({
                'position': position.name,
                'name': candidate.user.get_full_name() or candidate.user.username,
                'votes': Vote.objects.filter(candidate=candidate).count()
            })

    return render(request, 'voting/results.html', {'results': combined_results})




from django.contrib.auth.decorators import user_passes_test

def is_admin_or_candidate(user):
    return user.is_superuser or user.groups.filter(name='Candidates').exists()



