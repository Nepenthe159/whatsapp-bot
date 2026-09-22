import base64
import os
import requests
from flask import Flask, request
from openai import OpenAI
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# NVIDIA API istemcisini anahtarınla birlikte tanımlıyoruz
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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",
)


# DÜZELTME: Twilio'nun istek attığı adres /webhook olarak güncellendi
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

        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-v4.1-flash",
            messages=[
                {
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
                }
            ],
            temperature=0.2,
            top_p=0.7,
            max_tokens=500,
        )

        ai_response = completion.choices[0].message.content
        msg.body(ai_response)
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
