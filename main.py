import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# 12 ta viloyat markazlari va Nukus
CITIES = {
    "Tashkent": "Toshkent",
    "Samarkand": "Samarqand",
    "Bukhara": "Buxoro",
    "Andijan": "Andijon",
    "Fergana": "Farg'ona",
    "Namangan": "Namangan",
    "Qarshi": "Qarshi",
    "Termez": "Termiz",
    "Navoiy": "Navoiy",
    "Jizzakh": "Jizzax",
    "Guliston": "Guliston",
    "Urgench": "Urganch",
    "Nukus": "Nukus",
}


def get_weather():
    weather_text = "🌤 **BUGUNGI OB-HAVO MA'LUMOTLARI:**\n\n"
    for city_en, city_uz in CITIES.items():
        try:
            # wttr.in orqali ob-havo va haroratni olish
            url = f"https://wttr.in/{city_en}?format=%c+%t"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                weather_text += f"📍 **{city_uz}:** {res.text.strip()}\n"
        except Exception:
            weather_text += f"📍 **{city_uz}:** Noma'lum\n"
    return weather_text


def get_rates():
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    response = requests.get(url).json()

    usd = next(item for item in response if item["Ccy"] == "USD")
    eur = next(item for item in response if item["Ccy"] == "EUR")
    rub = next(item for item in response if item["Ccy"] == "RUB")

    rates_text = (
        "📈 **BUGUNGI VALYUTA KURSLARI:**\n\n"
        f"🇺🇸 1 USD = {usd['Rate']} so'm ({usd['Diff']} so'm)\n"
        f"🇪🇺 1 EUR = {eur['Rate']} so'm ({eur['Diff']} so'm)\n"
        f"🇷🇺 1 RUB = {rub['Rate']} so'm ({rub['Diff']} so'm)\n"
    )
    return rates_text


def send_telegram():
    # Ikkala ma'lumotni bitta xabarga biriktirish
    rates = get_rates()
    weather = get_weather()

    full_message = f"{rates}\n➖➖➖➖➖➖➖➖➖\n\n{weather}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": full_message,
        "parse_mode": "Markdown",
    }

    requests.post(url, json=payload)


if __name__ == "__main__":
    send_telegram()
