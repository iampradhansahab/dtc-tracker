import os
import time
import requests
from google.transit import gtfs_realtime_pb2

# --- AAPKI CONFIGURATION ---
API_KEY = "6FW941OTPC5fGl34zEi7ptHSQPSWyaxm"

# In dono ko apne Telegram bot token aur chat ID se replace karo
TELEGRAM_BOT_TOKEN = "8805266344:AAF2_hs5a8aHu5A1In_AC3lmcz1e81UEfQ8"  # BotFather wala token
TELEGRAM_CHAT_ID = "6296101949"      # userinfobot wala ID

DTC_URL = f"https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key={API_KEY}"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

def run_tracker():
    print("Cloud tracker starting...")
    send_telegram("🚀 DTC Tracker cloud par live ho gaya hai! Ready to track buses.")
    
    while True:
        try:
            res = requests.get(DTC_URL, timeout=20)
            if res.status_code == 200:
                feed = gtfs_realtime_pb2.FeedMessage()
                feed.ParseFromString(res.content)
                print(f"Tracking active: {len(feed.entity)} buses currently active.")
            else:
                print(f"API status code: {res.status_code}")
        except Exception as e:
            print(f"Fetch error: {e}")
        
        # Har 45 second baad DTC data check karega
        time.sleep(45)

if __name__ == "__main__":
    run_tracker()
