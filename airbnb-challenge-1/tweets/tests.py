from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Tweet

class TweetAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", 
            password="testpassword123"
        )
        # Create another user for permission testing
        self.other_user = User.objects.create_user(
            username="otheruser", 
            password="testpassword123"
        )
        # Create a test tweet
        self.tweet = Tweet.objects.create(
            payload="This is a test tweet", 
            user=self.user
        )
        # URL endpoints
        self.list_url = "/api/v1/tweets"
        self.detail_url = f"/api/v1/tweets/{self.tweet.pk}"

    def test_get_tweets(self):
        """Test GET /api/v1/tweets"""
        # Authenticate
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return at least one tweet
        self.assertGreaterEqual(len(response.data), 1)

    def test_post_tweet(self):
        """Test POST /api/v1/tweets"""
        self.client.force_authenticate(user=self.user)
        
        data = {"payload": "New tweet content"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["payload"], "New tweet content")
        self.assertEqual(response.data["user"], self.user.id)

    def test_get_tweet_detail(self):
        """Test GET /api/v1/tweets/<int:pk>"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"], self.tweet.payload)

    def test_put_tweet(self):
        """Test PUT /api/v1/tweets/<int:pk>"""
        self.client.force_authenticate(user=self.user)
        
        data = {"payload": "Updated tweet content"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"], "Updated tweet content")
        
        # Verify update in DB
        self.tweet.refresh_from_db()
        self.assertEqual(self.tweet.payload, "Updated tweet content")

    def test_delete_tweet(self):
        """Test DELETE /api/v1/tweets/<int:pk>"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deletion
        self.assertFalse(Tweet.objects.filter(pk=self.tweet.pk).exists())

    def test_put_tweet_not_owner(self):
        """Test PUT /api/v1/tweets/<int:pk> by non-owner"""
        self.client.force_authenticate(user=self.other_user)
        
        data = {"payload": "Malicious update"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_tweet_not_owner(self):
        """Test DELETE /api/v1/tweets/<int:pk> by non-owner"""
        self.client.force_authenticate(user=self.other_user)
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)