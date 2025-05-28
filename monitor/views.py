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

#def dashboard(request):
   # return render(request, 'dashboard.html')

def dashboard(request):
    try:
        response = requests.get(f"{FIREBASE_URL}/glucoseLevel.json")
        data = response.json()

        if data:
            # Sort keys and get the latest
            keys = sorted(data.keys())
            values = [entry.get('humidity', 0) for entry in data.values() if isinstance(entry, dict)]
            latest_value = data[keys[-1]].get('humidity', 'N/A')
            average_value = round(sum(values) / len(values), 1) if values else 'N/A'
        else:
            latest_value = 'No data'
            average_value = 'N/A'

    except Exception as e:
        latest_value = 'Error'
        average_value = 'N/A'

    return render(request, 'dashboard.html', {
        'glucose': latest_value,
        'average': average_value
    })