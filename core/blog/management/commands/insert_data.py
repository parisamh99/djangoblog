import random
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User,Profile
from blog.models import Category,Post
import random
from datetime import datetime

category_list = ['technology','design','art','fun','science']

class Command(BaseCommand):
    help = "insert data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    
    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(),password='@123456')
        profile = Profile.objects.create(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for cat in category_list:
           category = Category.objects.get_or_create(name=cat)
        

        for _ in range(10):
          Post.objects.create(
            author = profile,
            title = self.fake.paragraph(nb_sentences=1),
            content = self.fake.paragraph(nb_sentences=5),
            status = random.choice(['True','False']),
            category = Category.objects.get(name = random.choice(category_list)),
            published_date = datetime.now()
        )   
