import os
import sys
import traceback
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "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")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

SYSTEM_PROMPT = (
    "Sen WhatsApp'ta arkadaşınla yazışan samimi, sokak dilini ve günlük Türkçeyi rahat kullanan gerçek bir gençsin. "
    "Adın kanka, kafa dengi birisin.\n\n"
    "STRICT RULES (BU KURALLARI ASLA İHLAL ETME):\n"
    "1. ASLA 'Siz', 'Sizin', 'İstersiniz', 'Yardımcı olayım', 'Ne tür sorunlar', 'Sevgili dostum' gibi müşteri temsilcisi veya yapay zeka lafları KULLANMA.\n"
    "2. Sen bir yapay zeka veya asistan DEĞİLSİN. Senden bir görev istenmedikçe asistanlık yapma, sadece sohbet et.\n"
    "3. Sadece 'sen', 'kanka', 'bro', 'kral' diye hitap et.\n"
    "4. Cümlelerin kısa, tek-iki satırlık, WhatsApp mesajı formatında olsun. Küçük harflerle, rahat ve samimi yaz.\n"
    "5. Kullanıcının söylediği lafları tekrarlama, muhabbeti kendin devam ettir."
)

@app.route("/", methods=['GET'])
def home():
    print("[+] Ana sayfaya ping geldi", flush=True)
    return "Bot aktif ve çalışıyor!", 200

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    
    print(f"\n[+] Gelen Mesaj ({sender}): {incoming_msg}", flush=True)

    models_to_try = [
        "meta/llama-3.1-70b-instruct",
        "nvidia/llama-3.1-nemotron-70b-instruct"
    ]
    
    ai_response = None

    for model_name in models_to_try:
        try:
            print(f"[*] Denenen Model: {model_name}", flush=True)
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": incoming_msg}
                ],
                temperature=0.8,
                max_tokens=200
            )
            ai_response = completion.choices[0].message.content
            print(f"[+] Başarılı Yanıt Alındı ({model_name}): {ai_response}", flush=True)
            break
        except Exception as e:
            print(f"[-] {model_name} Hata Verdi:\n{traceback.format_exc()}", flush=True)

    if not ai_response:
        ai_response = "ufak bi sorun oldu kanka tekrar yazsana"

    resp = MessagingResponse()
    resp.message(ai_response)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
