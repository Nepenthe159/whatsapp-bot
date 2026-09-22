import base64
from openai import OpenAI

# NVIDIA API istemcisini verdiğin anahtarla tanımlıyoruz
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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",
)

# Görseli okuyup Base64 formatına çevirme
image_path = "resim.jpg"  # Analiz ettireceğin görselin dosya adı veya yolu

with open(image_path, "rb") as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")

# API isteğini gönderme
response = client.chat.completions.create(
    model="deepseek-ai/deepseek-v4.1-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Describe the path in this image and the landscape"
                        " around it in two sentences."
                    ),
                },
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
    max_tokens=1024,
)

# Yapay zekanın cevabını ekrana yazdırma
print(response.choices[0].message.content)
