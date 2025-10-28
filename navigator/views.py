import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
import os
from dotenv import load_dotenv
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

from mistralai import Mistral
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def chatbot(request):
    return render(request, 'chatbot.html')

def chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # 🌐 Navigation intents
        navigation_map = {
            "home": "/",
            "about": "/about/",
            "contact": "/contact/",
            "chatbot": "/chatbot/",
        }

        redirect_url = None
        for keyword, url in navigation_map.items():
            if keyword in user_message.lower():
                bot_reply = f"Sure! Redirecting you to the {keyword.capitalize()} page..."
                return JsonResponse({"reply": bot_reply, "redirect_url": url})

        # 🧠 Mistral AI API call
        try:
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {MISTRAL_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistral-tiny",
                    "messages": [
                        {"role": "system", "content": "You are an AI website navigation chatbot. Help users explore the website and answer general questions clearly."},
                        {"role": "user", "content": user_message}
                    ]
                }
            )
            response_data = response.json()

            if "choices" in response_data:
                bot_reply = response_data["choices"][0]["message"]["content"]
            else:
                bot_reply = "Hmm... I couldn't get a response right now. Try again in a moment."

        except Exception as e:
            bot_reply = f"Error connecting to AI: {str(e)}"

        return JsonResponse({"reply": bot_reply})

    return JsonResponse({"error": "Invalid request"}, status=400)
