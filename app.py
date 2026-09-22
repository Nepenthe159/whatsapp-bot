import base64
import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

NVIDIA_API_KEY = (
    "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"
)
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


@app.route("/webhook", methods=["POST"])
def whatsapp_reply():
  incoming_msg = request.form.get("Body", "").strip()
  num_media = int(request.form.get("NumMedia", 0))

  resp = MessagingResponse()
  msg = resp.message()

  try:
    if num_media > 0:
      media_url = request.form.get("MediaUrl0")
      media_type = request.form.get("MediaContentType0", "")

      if "image" in media_type:
        # Twilio'dan görseli indirip base64 formatına çeviriyoruz
        img_data = requests.get(media_url).content
        b64_image = base64.b64encode(img_data).decode("utf-8")

        prompt_text = (
            incoming_msg
            if incoming_msg
            else (
                "Describe the path in this image and the landscape around it in"
                " two sentences."
            )
        )

        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json",
        }

        # Görsel destekleyen Llama Vision modeli ile güncellendi
        payload = {
            "model": "meta/llama-3.2-11b-vision-instruct",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}"
                        },
                    },
                ],
            }],
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 500,
        }

        response = requests.post(
            NVIDIA_URL, json=payload, headers=headers, timeout=60
        )

        if response.status_code == 200:
          res_json = response.json()
          ai_response = res_json["choices"][0]["message"]["content"]
          msg.body(ai_response)
        else:
          msg.body(
              f"NVIDIA API Hatası ({response.status_code}): {response.text}"
          )
      else:
        msg.body(
            "Kanka şu an sadece görsel (fotoğraf) dosyalarını analiz"
            " edebiliyorum."
        )
    else:
      msg.body(
          f"Mesajını aldım: '{incoming_msg}'. Bana bir fotoğraf gönderirsen"
           " onu da inceleyebilirim kanka!"
      )

  except Exception as e:
    msg.body(f"Bir hata oluştu kanka: {str(e)}")

  return str(resp)


@app.route("/", methods=["GET"])
def home():
  return "WhatsApp Bot aktif ve çalışıyor!"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
