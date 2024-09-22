
# management/commands/populate_db.py

from django.core.management.base import BaseCommand
from myapp.models import UserProfile1
import random

class Command(BaseCommand):
    help = 'Populates the database with sample user profiles'

    def handle(self, *args, **kwargs):
        skills = ['Python', 'JavaScript', 'Java', 'C++', 'SQL', 'React', 'Angular', 'Vue.js', 'Django', 'Flask']
        locations = ['New York', 'San Francisco', 'London', 'Berlin', 'Tokyo', 'Sydney', 'Toronto', 'Paris']
        job_titles = ['Software Engineer', 'Data Scientist', 'Product Manager', 'UX Designer', 'DevOps Engineer']

        for i in range(100):  # Create 100 sample profiles
            profile = UserProfile1(
                name=f"User {i+1}",
                age=random.randint(22, 60),
                email=f"user{i+1}@example.com",
                bio=f"This is the bio for User {i+1}",
                skills=', '.join(random.sample(skills, random.randint(2, 5))),
                location=random.choice(locations),
                job_title=random.choice(job_titles),
                years_experience=random.randint(0, 30)
            )
            profile.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))