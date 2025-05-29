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


def missions(request):
    try:
        # Fetch latest glucose data
        response = requests.get(f"{FIREBASE_URL}/glucoseLevel.json")
        data = response.json()

        if data:
            latest_key = sorted(data.keys())[-1]
            latest_value = data[latest_key].get("glucose level", "N/A")
        else:
            latest_value = "No data"
            latest_key = "N/A"

        # Generate missions based on glucose value
        missions = []

        if isinstance(latest_value, (int, float)):
            if latest_value < 70:
                missions = [
                    "Take fast-acting glucose (juice or glucose tablets)",
                    "Rest for 15 minutes and retest",
                    "Notify caregiver or family member"
                ]
            elif latest_value > 180:
                missions = [
                    "Go for a 20-minute walk",
                    "Drink a glass of water",
                    "Avoid sugar or carbs for the next hour"
                ]
            else:
                missions = [
                    "Maintain a balanced diet today",
                    "Take a 30-minute walk",
                    "Log today’s glucose reading"
                ]
        else:
            missions = ["Unable to generate missions due to missing glucose data."]

    except Exception as e:
        latest_value = 'Error'
        latest_key = str(e)
        missions = ["Could not fetch data from Firebase."]

    return render(request, 'missions.html', {
        'glucose': latest_value,
        'timestamp': latest_key,
        'missions': missions
    })