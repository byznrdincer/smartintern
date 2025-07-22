from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    graduation_year = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    legacy_website = models.URLField(blank=True, null=True)

    internship_type = models.CharField(max_length=50, blank=True, null=True)
    preferred_locations = models.CharField(max_length=255, blank=True, null=True)
    open_to_relocate = models.BooleanField(default=False)

    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    technologies = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.profile.user.username}"

class Certification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    date_obtained = models.DateField()
    certificate_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.profile.user.username}"

class Company(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    industry = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Eğer slug boşsa, name'den otomatik oluştur
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Position(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"
