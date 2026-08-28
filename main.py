import os
import requests

# Secrets'dan kalitlarni olish
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_rates():
    # O'zbekiston Markaziy Banki API
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    response = requests.get(url).json()

    # Kerakli valyutalarni ajratib olish
    usd = next(item for item in response if item["Ccy"] == "USD")
    eur = next(item for item in response if item["Ccy"] == "EUR")
    rub = next(item for item in response if item["Ccy"] == "RUB")

    # Xabar matnini shakllantirish
    text = (
        f"📊 **Bugungi valyuta kurslari:**\n\n"
        f"🇺🇸 1 USD = {usd['Rate']} so'm ({usd['Diff']} so'm)\n"
        f"🇪🇺 1 EUR = {eur['Rate']} so'm ({eur['Diff']} so'm)\n"
        f"🇷🇺 1 RUB = {rub['Rate']} so'm ({rub['Diff']} so'm)"
    )
    return text

def send_telegram():
    message = get_rates()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        print("Xabar muvaffaqiyatli yuborildi!")
    else:
        print(f"Xatolik yuz berdi: {res.text}")

if __name__ == "__main__":
    send_telegram()
