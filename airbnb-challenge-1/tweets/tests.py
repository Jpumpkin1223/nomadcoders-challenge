from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Tweet


class TweetUserAPITestCase(APITestCase):
    """Tweet/User API 통합 테스트"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="pass1234"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@example.com", password="pass1234"
        )
        self.tweet = Tweet.objects.create(user=self.user, payload="hello world")
        self.other_tweet = Tweet.objects.create(
            user=self.other_user, payload="other tweet"
        )

        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)

        self.other_client = APIClient()
        self.other_client.force_authenticate(user=self.other_user)

        self.anon_client = APIClient()

    def test_requires_authentication(self):
        response = self.anon_client.get("/api/v1/tweets")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_tweets(self):
        response = self.auth_client.get("/api/v1/tweets")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_create_tweet(self):
        payload = {"payload": "new tweet"}
        response = self.auth_client.post("/api/v1/tweets", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["user"], self.user.id)

    def test_update_tweet_by_owner(self):
        payload = {"payload": "updated"}
        response = self.auth_client.put(
            f"/api/v1/tweets/{self.tweet.id}", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["payload"], "updated")

    def test_update_tweet_by_non_owner_forbidden(self):
        payload = {"payload": "hacked"}
        response = self.other_client.put(
            f"/api/v1/tweets/{self.tweet.id}", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_and_detail(self):
        response = self.auth_client.get("/api/v1/users")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

        detail = self.auth_client.get(f"/api/v1/users/{self.user.id}")
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.json()["username"], self.user.username)

    def test_user_tweets_endpoint(self):
        response = self.auth_client.get(f"/api/v1/users/{self.user.id}/tweets")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["payload"], self.tweet.payload)

    def test_user_tweets_not_found(self):
        response = self.auth_client.get("/api/v1/users/9999/tweets")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
