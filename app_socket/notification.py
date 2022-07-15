import json

import requests
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from GMB_Django_web.settings import client_id, client_secret, ip, redirect_uri

created_campaign = False


def get_all_notification(request):
    current_user = request.session.get('curr_user_id')
    token = request.session["token"]
    try:
        response = requests.get(
            f"{ip}notifications/{current_user}",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        notifications = response.json()
        notifications = notifications["items"]
        context = {"notifications": notifications}
        return render(request, "campaign/notification.html", context)
    except Exception as e:
        pass

    return render(request, "campaign/notification.html")


def get_notification(request):
    current_user = request.session.get('curr_user_id')
    token = request.session["token"]
    if request.method == "GET":
        response = requests.get(
            f"{ip}notifications/{current_user}/?page=1&size=5",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)

    pass


def save_notification(request):
    token = request.session["token"]
    if request.method == "GET":
        notification = request.GET["notification"]
        user_id = int(request.GET["user_id"])
        campaign_id = int(request.GET["campaign_id"])
        campaign_status = int(request.GET["campaign_status"])
        try:
            data = {
                "user_id": user_id,
                "notification": notification,
                "campaign_id": campaign_id,
                "campaign_status": campaign_status,
                "is_seen": False,
            }
            response = requests.post(
                f"{ip}notifications/create/",
                json=data,
                headers={"Authorization": f"Bearer {token}"},
            )
            return JsonResponse(True, safe=False)
        except Exception as e:
            pass

    pass


def update_notification(request):
    token = request.session["token"]
    if request.method == "GET":
        try:
            notification_id = request.GET["id"]
            data = {
                "is_seen": True,
            }
            response = requests.put(
                f"{ip}notifications/update/is_seen/{notification_id}/",
                json=data,
                headers={"Authorization": f"Bearer {token}"},
            )
            return JsonResponse(True, safe=False)
        except Exception as e:
            pass
    pass
