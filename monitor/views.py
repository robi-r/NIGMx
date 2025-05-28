import os
import firebase_admin
from firebase_admin import credentials, db
from django.http import JsonResponse
from django.shortcuts import render
import requests
# Create your views here.

FIREBASE_URL = "https://glucoease-default-rtdb.asia-southeast1.firebasedatabase.app"


def home(request):
    try:
        response = requests.get(f"{FIREBASE_URL}/glucoseLevel.json")
        data = response.json()

        if data:
            latest_key = sorted((data.keys()))[-1]
            latest_value =  data[latest_key].get("humidity", "N/A")
        else:
            latest_value = "No data"
            latest_key = "N/A"
    except Exception as e:
        latest_value = 'Error'
        latest_key = str(e)

    return render(request, 'home.html', {
        'glucose' : latest_value,
        'timestamp': latest_key
    })

def dashboard(request):
    return render(request, 'dashboard.html')