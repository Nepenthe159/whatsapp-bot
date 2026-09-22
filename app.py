import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)

# NVIDIA NIM API Yapılandırması
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "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")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

# Kesin sohbet tarzı ve örnek diyaloglar
SYSTEM_PROMPT = (
    "Sen WhatsApp'ta arkadaşınla mesajlaşan kafa dengi, samimi, gerçek bir Türk genç arkadaşsın. "
    "Sana 'kanka', 'kral', 'bro' dendiğinde aynı doğallıkla karşılık ver. "
    "KESİNLİKLE bir yapay zeka asistanı, çağrı merkezi veya görev robotu DEĞİLSİN! "
    "'Ne yapmam gerekiyor?', 'Nasıl yardımcı olabilirim?', 'Ne gibi bir problem var?' gibi müşteri temsilcisi laflarını KESİNLİKLE KULLANMA. "
    "Senden bir görev istenmedikçe sadece normal muhabbet et. Cümlelerin sohbet havasında, kısa ve akıcı olsun.\n\n"
    "Örnek sohbet tarzın:\n"
    "- Kullanıcı: naber nasıl gidiyor\n"
    "- Sen: iyi valla nolsun takılıyorum öyle, senden naber?\n"
    "- Kullanıcı: iyi bende nolsun kanka\n"
    "- Sen: eyvallah kanka, nasıl geçiyor günün var mı bir hareketlilik?\n"
)

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    
    print(f"\n[+] Gelen Mesaj ({sender}): {incoming_msg}")

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",  # 70 Milyar parametreli dev sohbet modeli
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": incoming_msg}
            ],
            temperature=0.8,
            max_tokens=250
        )
        ai_response = completion.choices[0].message.content
        print(f"[+] Yapay Zeka Yanıtı: {ai_response}")
    except Exception as e:
        print(f"[-] NVIDIA API Hatası: {e}")
        ai_response = "Ufak bir aksaklık oldu kanka, tekrar yazsana."

    resp = MessagingResponse()
    resp.message(ai_response)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
