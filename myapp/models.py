# models.py

from django.db import models

class UserProfile1(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255) # Stored as comma-separated values
    location = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    years_experience = models.IntegerField()

    def __str__(self):
        return self.name

    def skill_list(self):
        return [skill.strip() for skill in self.skills.split(',')]