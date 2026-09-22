import os
import sys
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    print("[+] Ana sayfaya ping geldi (UptimeRobot)", flush=True)
    return "Bot aktif ve çalışıyor!", 200

@app.route("/webhook", methods=['POST'])
def webhook():
    # İstek geldiği an konsola yazması gerekiyor
    print("\n--------------------------------------------------", flush=True)
    print("[+] WEBHOOK'A İSTEK DÜŞTÜ!", flush=True)
    print(f"[+] Form Verileri: {request.form}", flush=True)
    
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    
    print(f"[+] Gönderen: {sender} | Mesaj: {incoming_msg}", flush=True)
    print("--------------------------------------------------\n", flush=True)

    # Yapay zekaya girmeden doğrudan test yanıtı dönüyoruz
    resp = MessagingResponse()
    resp.message("bağlantı başarılı kanka, mesajı aldım!")
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
