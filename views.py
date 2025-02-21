from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse

import pickle
import numpy as np

# Load your ransomware detection model
with open('models/ransomware_model.pkl', 'rb') as f:
    model = pickle.load(f)

def home(request):
    return render(request, 'detector/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'detector/login.html', {'error': 'Invalid credentials'})
    return render(request, 'detector/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'detector/signup.html')

def detect(request):
    if request.method == 'POST':
        data = request.POST.getlist('data[]')
        data = np.array(data, dtype=float).reshape(1, -1)
        prediction = model.predict(data)
        result = "Ransomware Detected!" if prediction[0] == 1 else "No Ransomware Found."
        return JsonResponse({'result': result})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def result_view(request):
    # Your logic here
    return render(request, 'detector/result.html')




def upload_image(request):
    if request.method == 'POST':
        # Handle file upload, processing, and prediction here
        prediction = "Your prediction result"  # Replace with actual prediction

        # Render a separate template with the prediction 
        return render(request, 'prediction_result.html', {'prediction': prediction}) 

    return render(request, 'upload_image.html')