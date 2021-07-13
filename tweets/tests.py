from django.contrib.auth.models import User
from django.test import TestCase
from tweets.models import Tweet
from datetime import timedelta
from utils.time_helpers import utc_now
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from tweets.models import Tweet
from utils.time_helpers import utc_now


# Create your tests here.
class TweetTests(TestCase):

    def test_hours_to_now(self):
        user1 = User.objects.create_user(username='user1')
        tweet = Tweet.objects.create(user=user1, content='This is awesome!')
        tweet.created_at = utc_now() - timedelta(hours=10)
        tweet.save()
        self.assertEqual(tweet.hours_to_now, 10)
