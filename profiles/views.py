from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, ProjectForm, CertificationForm

@login_required
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    years = list(range(2024, 2034))

    profile_form = ProfileForm(instance=profile)
    project_form = ProjectForm()
    certification_form = CertificationForm()

    if request.method == "POST":
        # Profil formu gönderildiyse
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

        # Proje formu gönderildiyse
        elif 'project_submit' in request.POST:
            project_form = ProjectForm(request.POST)
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.profile = profile
                project.save()
                return redirect('profile_detail', username=username)

        # Sertifika formu gönderildiyse
        elif 'certification_submit' in request.POST:
            certification_form = CertificationForm(request.POST)
            if certification_form.is_valid():
                cert = certification_form.save(commit=False)
                cert.profile = profile
                cert.save()
                return redirect('profile_detail', username=username)

    context = {
        'profile_user': user,
        'form': profile_form,
        'project_form': project_form,
        'certification_form': certification_form,
        'years': years,
        'projects': profile.projects.all(),
        'certifications': profile.certifications.all(),
    }
    return render(request, 'profiles/profile_detail.html', context)
@login_required
def profile_edit(request, username):
    return redirect('profile_detail', username=username)
