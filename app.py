from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)

# NVIDIA NIM API Yapılandırması
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')
    
    print(f"\n[+] Gelen Mesaj ({sender}): {incoming_msg}")

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.2-11b-vision-instruct",
            messages=[
                {
                    "role": "system", 
                    "content": "Sen WhatsApp üzerinden hizmet veren yardımsever, akıllı ve samimi bir yapay zeka asistanısın. Yanıtlarını WhatsApp formatına uygun, net ve kısa tut."
                },
                {"role": "user", "content": incoming_msg}
            ],
            temperature=0.6,
            max_tokens=1024
        )
        ai_response = completion.choices[0].message.content
        print(f"[+] Yapay Zeka Yanıtı: {ai_response}")
    except Exception as e:
        print(f"[-] NVIDIA API Hatası: {e}")
        ai_response = "Üzgünüm, şu an yanıt üretirken bir sorun oluştu."

    resp = MessagingResponse()
    resp.message(ai_response)
    return str(resp)

if __name__ == "__main__":
    print("Bot sunucusu başlatılıyor...")
    app.run(port=5000, debug=True)
