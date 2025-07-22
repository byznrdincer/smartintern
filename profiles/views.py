from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Skill, Company, Position
from .forms import ProfileForm, ProjectForm, CertificationForm, CompanyForm, PositionForm

def calculate_completion_percent(profile):
    percent = 0
    if profile.bio:
        percent += 30
    if profile.location:
        percent += 30
    if profile.skills.exists():
        percent += 40
    return percent

def calculate_company_completion(company):
    percent = 0
    if company.about:
        percent += 30
    if company.location:
        percent += 30
    if company.positions.exists():
        percent += 40
    return percent

@login_required
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    years = list(range(2024, 2034))

    profile_form = ProfileForm(instance=profile)
    project_form = ProjectForm()
    certification_form = CertificationForm()

    if request.method == "POST":

        if 'profile_submit' in request.POST:
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()

                full_name = request.POST.get("full_name", "").strip()
                email = request.POST.get("email", "").strip()

                if full_name:
                    names = full_name.split()
                    user.first_name = names[0]
                    user.last_name = " ".join(names[1:]) if len(names) > 1 else ""
                if email:
                    user.email = email
                user.save()

                return redirect('profile_detail', username=username)

        elif 'project_submit' in request.POST:
            project_form = ProjectForm(request.POST)
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.profile = profile
                project.save()
                return redirect('profile_detail', username=username)

        elif 'certification_submit' in request.POST:
            certification_form = CertificationForm(request.POST)
            if certification_form.is_valid():
                cert = certification_form.save(commit=False)
                cert.profile = profile
                cert.save()
                return redirect('profile_detail', username=username)

        elif 'social_submit' in request.POST:
            profile.github = request.POST.get('github', '')
            profile.linkedin = request.POST.get('linkedin', '')
            profile.website = request.POST.get('website', '')
            profile.legacy_website = request.POST.get('legacy_website', '')
            profile.save()
            return redirect('profile_detail', username=username)

        elif 'internship_submit' in request.POST:
            profile.internship_type = request.POST.get('internship_type', '')
            profile.preferred_locations = request.POST.get('preferred_locations', '')
            profile.open_to_relocate = 'open_to_relocate' in request.POST
            profile.save()
            return redirect('profile_detail', username=username)

        elif 'skills_submit' in request.POST:
            skills_ids = request.POST.getlist('skills')
            profile.skills.set(skills_ids)
            return redirect('profile_detail', username=username)

    full_name = user.get_full_name()

    context = {
        'profile_user': user,
        'profile': profile,
        'full_name': full_name,
        'form': profile_form,
        'project_form': project_form,
        'certification_form': certification_form,
        'years': years,
        'projects': profile.projects.all(),
        'certifications': profile.certifications.all(),
        'skills_count': profile.skills.count(),
        'projects_count': profile.projects.count(),
        'certifications_count': profile.certifications.count(),
        'profile_views': 0,
        'completion_percent': calculate_completion_percent(profile),
        'all_skills': Skill.objects.all(),
        'skills': profile.skills.all(),
    }
    return render(request, 'profiles/profile_detail.html', context)

@login_required
def company_profile(request, slug):
    company = get_object_or_404(Company, slug=slug)

    company_form = CompanyForm(instance=company)
    position_form = PositionForm()

    if request.method == "POST":

        if 'company_info_submit' in request.POST:
            company_form = CompanyForm(request.POST, instance=company)
            if company_form.is_valid():
                company_form.save()
                return redirect('company_profile', slug=slug)

        elif 'position_submit' in request.POST:
            position_form = PositionForm(request.POST)
            if position_form.is_valid():
                position = position_form.save(commit=False)
                position.company = company
                position.save()
                return redirect('company_profile', slug=slug)

        elif 'social_submit' in request.POST:
            company.linkedin = request.POST.get('linkedin', '')
            company.twitter = request.POST.get('twitter', '')
            company.facebook = request.POST.get('facebook', '')
            company.save()
            return redirect('company_profile', slug=slug)

    completion_percent = calculate_company_completion(company)

    context = {
        'company': company,
        'profile_views': 0,  # burayı şirket verilerine göre ayarla
        'open_positions_count': company.positions.count(),
        'applicants_count': 0,  # Başvuru sayısı varsa çek
        'completion_percent': completion_percent,
        'company_form': company_form,
        'position_form': position_form,
    }
    return render(request, 'profiles/company_profile.html', context)
@login_required
def profile_edit(request, username):
    return redirect('profile_detail', username=username)

