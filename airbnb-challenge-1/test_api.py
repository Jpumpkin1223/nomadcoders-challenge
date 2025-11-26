"""
API 테스트 스크립트

사용법:
    uv run python test_api.py
"""

import os
import sys
import django

# Django 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 테스트를 위한 ALLOWED_HOSTS 설정
from django.conf import settings

if "testserver" not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append("testserver")

from django.contrib.auth.models import User
from tweets.models import Tweet
from rest_framework.test import APIClient
import json


def create_test_data():
    """테스트용 데이터 생성"""
    # 기존 데이터가 있으면 스킵
    if User.objects.exists():
        print("테스트 데이터가 이미 존재합니다.")
        return

    # 테스트 유저 생성
    user1 = User.objects.create_user(username="testuser1", password="testpass123")
    user2 = User.objects.create_user(username="testuser2", password="testpass123")

    # 테스트 트윗 생성
    Tweet.objects.create(user=user1, payload="첫 번째 테스트 트윗입니다!")
    Tweet.objects.create(user=user1, payload="두 번째 테스트 트윗입니다!")
    Tweet.objects.create(user=user2, payload="다른 유저의 트윗입니다!")

    print("테스트 데이터가 생성되었습니다:")
    print(f"  - Users: {User.objects.count()}")
    print(f"  - Tweets: {Tweet.objects.count()}")


def get_authenticated_client(user: User | None = None) -> APIClient:
    """세션 없이 간편하게 인증된 APIClient를 반환"""
    user = user or User.objects.first()
    if not user:
        raise AssertionError("인증할 유저가 없습니다.")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_all_tweets_api():
    """모든 트윗 리스트 API 테스트"""
    print("\n=== 테스트 1: /api/v1/tweets ===")
    client = get_authenticated_client()
    response = client.get("/api/v1/tweets")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

    assert response.status_code == 200, f"예상: 200, 실제: {response.status_code}"
    assert isinstance(response.json(), list), "응답이 리스트여야 합니다"
    print("✓ 테스트 통과!")


def test_user_tweets_api():
    """특정 유저의 트윗 리스트 API 테스트"""
    print("\n=== 테스트 2: /api/v1/users/<user_id>/tweets ===")

    # 유저 ID 가져오기
    user = User.objects.first()
    if not user:
        print("테스트할 유저가 없습니다.")
        return

    client = get_authenticated_client(user)
    response = client.get(f"/api/v1/users/{user.id}/tweets")

    print(f"User ID: {user.id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

    assert response.status_code == 200, f"예상: 200, 실제: {response.status_code}"
    assert isinstance(response.json(), list), "응답이 리스트여야 합니다"
    print("✓ 테스트 통과!")


def test_user_not_found():
    """존재하지 않는 유저 테스트"""
    print("\n=== 테스트 3: 존재하지 않는 유저 ===")
    client = get_authenticated_client()
    response = client.get("/api/v1/users/99999/tweets")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

    assert response.status_code == 404, f"예상: 404, 실제: {response.status_code}"
    assert "detail" in response.json(), "에러 메시지가 포함되어야 합니다"
    print("✓ 테스트 통과!")


if __name__ == "__main__":
    print("=" * 50)
    print("API 테스트 시작")
    print("=" * 50)

    # 테스트 데이터 생성
    create_test_data()

    # API 테스트 실행
    try:
        test_all_tweets_api()
        test_user_tweets_api()
        test_user_not_found()

        print("\n" + "=" * 50)
        print("모든 테스트 통과! ✓")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n❌ 테스트 실패: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
