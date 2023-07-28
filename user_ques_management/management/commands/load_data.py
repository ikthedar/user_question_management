import csv
from django.core.management.base import BaseCommand
from user_ques_management.models import UserProfile, Question

class Command(BaseCommand):
    help = 'Load generated data into the database'

    def handle(self, *args, **kwargs):
        # Load user data
        with open('users_data.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                UserProfile.objects.create(**row)

        # Load question data
        with open('questions_data.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Question.objects.create(**row)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
