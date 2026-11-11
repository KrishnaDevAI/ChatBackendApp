import json

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Profile
from .tasks import add_numbers

def run_task(request):
    task = add_numbers.delay(10, 20)
    return JsonResponse({
        "task_id": task.id,
        "status": "Task started"
    })


def _json_body(request):
    try:
        return json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return None


def _api_response(data, status=200):
    response = JsonResponse(data, status=status)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response

def _user_response(user):
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def register_user(request):
    if request.method == "OPTIONS":
        return _api_response({})

    data = _json_body(request)
    if data is None:
        return _api_response({"detail": "Invalid JSON body."}, status=400)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    username = email

    if not email or not password:
        return _api_response({"detail": "Email and password are required."}, status=400)
    if User.objects.filter(username=username).exists():
        return _api_response({"detail": "A user with this email already exists."}, status=409)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=data.get("first_name", "").strip(),
        last_name=data.get("last_name", "").strip(),
    )
    Profile.objects.create(user=user, image=data.get("image"), address=data.get("address", "").strip())
    login(request, user)
    return _api_response({"message": "Registration successful.", "user": _user_response(user)}, status=201)


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def login_user(request):
    if request.method == "OPTIONS":
        return _api_response({})

    data = _json_body(request)
    if data is None:
        return _api_response({"detail": "Invalid JSON body."}, status=400)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    user = authenticate(request, username=email, password=password)

    if user is None:
        return _api_response({"detail": "Invalid email or password."}, status=401)

    login(request, user)
    return _api_response({"message": "Login successful.", "user": _user_response(user)})


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def logout_user(request):
    if request.method == "OPTIONS":
        return _api_response({})

    logout(request)
    return _api_response({"message": "Logout successful."})


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def google_login(request):
    if request.method == "OPTIONS":
        return _api_response({})

    data = _json_body(request)
    access_token = data.get("access_token") if data else None
    if not access_token:
        return _api_response({"detail": "Google access token is required."}, status=400)

    google_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    if not google_response.ok:
        return _api_response({"detail": "Invalid Google access token."}, status=401)

    google_user = google_response.json()

    email = google_user.get("email", "").strip().lower()
    if not email or not google_user.get("email_verified", False):
        return _api_response({"detail": "Google email could not be verified."}, status=401)

    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            "email": email,
            "first_name": google_user.get("given_name", ""),
            "last_name": google_user.get("family_name", ""),
        },
    )
    user.email = email
    user.first_name = google_user.get("given_name", user.first_name)
    user.last_name = google_user.get("family_name", user.last_name)
    user.save(update_fields=["email", "first_name", "last_name"])
    Profile.objects.get_or_create(user=user)
    login(request, user)

    return _api_response({
        "message": "Google registration successful." if created else "Google login successful.",
        "user": _user_response(user),
    }, status=201 if created else 200)
