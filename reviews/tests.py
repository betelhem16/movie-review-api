from django.test import TestCase
from django.contrib.auth.models import User
from .models import Review

class ReviewModelTest(TestCase):
    def test_create_review(self):
        u = User.objects.create_user(username='tuser', password='test1234')
        r = Review.objects.create(movie_title='Dummy', review_text='Nice', owner=u)
        self.assertEqual(r.movie_title, 'Dummy')
