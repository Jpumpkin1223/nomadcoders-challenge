# Airbnb Challenge 1 - Django Tweets App

Django 프로젝트로 구현한 트윗 애플리케이션입니다.

## 프로젝트 구조

- **프로젝트명**: airbnb-challenge-1
- **Django 버전**: 5.2.8
- **패키지 관리**: uv

## 앱

### tweets

트윗과 좋아요 기능을 제공하는 앱입니다.

#### 모델

- **Tweet**: 트윗 모델
  - `payload`: 트윗 내용 (최대 180자)
  - `user`: 작성자 (ForeignKey)
  - `created_at`: 생성일
  - `updated_at`: 수정일

- **Like**: 좋아요 모델
  - `user`: 좋아요를 누른 사용자 (ForeignKey)
  - `tweet`: 좋아요가 달린 트윗 (ForeignKey)
  - `created_at`: 생성일
  - `updated_at`: 수정일

#### 특징

- 추상 기본 클래스(`TimeStampedModel`)를 사용하여 `created_at`과 `updated_at` 필드를 공통으로 제공
- 모든 모델에 커스터마이징된 `__str__` 메서드 구현
- Django Admin을 통한 모델 관리 지원

## 설치 및 실행

### 요구사항

- Python 3.14+
- uv

### 설치

```bash
# 의존성 설치
uv sync
```

### 데이터베이스 마이그레이션

```bash
# 마이그레이션 생성
uv run python manage.py makemigrations

# 마이그레이션 적용
uv run python manage.py migrate
```

### 개발 서버 실행

```bash
uv run python manage.py runserver
```

## 관리자 페이지

Django Admin을 통해 Tweet과 Like 모델을 관리할 수 있습니다.

```bash
# 관리자 계정 생성
uv run python manage.py createsuperuser
```

서버 실행 후 `http://127.0.0.1:8000/admin/`에서 접근할 수 있습니다.

