import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)

# NVIDIA NIM API Yapılandırması (Güvenlik için env variable veya doğrudan key)
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "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")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

# Doğal, insansı ve samimi sohbet direktifi
SYSTEM_PROMPT = (
    "Sen WhatsApp üzerinden mesajlaşan kafa dengi, samimi ve son derece doğal bir arkadaşsın. "
    "Yazışma dilin resmi veya yapay zeka gibi olmamalı; tıpkı bir insanın yakın arkadaşıyla WhatsApp'ta yazışması gibi rahat, akıcı ve samimi olsun. "
    "Kullanıcının söylediği cümleleri aynen veya kelimelerini değiştirip tekrarlama (papağan gibi yansıtma). "
    "'Gönlündeki mutluluk benim için önemli' veya 'Uygulamayı eklemeye çalışırken sorun yaşıyor musun' gibi çeviri kokan robotik kalıpları KESİNLİKLE kullanma. "
    "Cevaplarını WhatsApp sohbetine uygun olarak kısa, öz, zaman zaman esprili ve doğal tut."
)

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    
    print(f"\n[+] Gelen Mesaj ({sender}): {incoming_msg}")

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.2-11b-vision-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": incoming_msg}
            ],
            temperature=0.7,   # Yanıtların daha özgün ve kalıp dışı olması için
            max_tokens=400     # WhatsApp'ta hem daha hızlı üretilsin hem de gereksiz uzamasın
        )
        ai_response = completion.choices[0].message.content
        print(f"[+] Yapay Zeka Yanıtı: {ai_response}")
    except Exception as e:
        print(f"[-] NVIDIA API Hatası: {e}")
        ai_response = "Ufak bir aksaklık oldu, tekrar yazar mısın?"

    resp = MessagingResponse()
    resp.message(ai_response)
    return str(resp)

if __name__ == "__main__":
    print("Bot sunucusu başlatılıyor...")
    app.run(port=5000, debug=True)
