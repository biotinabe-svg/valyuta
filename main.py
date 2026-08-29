import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# 12 ta viloyat markazi va Qoraqalpog'iston (Nukus)
CITIES = {
    "Toshkent": (41.2995, 69.2401),
    "Samarqand": (39.6542, 66.9597),
    "Buxoro": (39.7747, 64.4286),
    "Andijon": (40.7821, 72.3442),
    "Farg'ona": (40.3864, 71.7864),
    "Namangan": (40.9983, 71.6726),
    "Qarshi": (38.8605, 65.7899),
    "Termiz": (37.2242, 67.2783),
    "Navoiy": (40.0844, 65.3792),
    "Jizzax": (40.1158, 67.8422),
    "Guliston": (40.4897, 68.7842),
    "Urganch": (41.5503, 60.6317),
    "Nukus": (42.4603, 59.6166),
}


def get_weather():
    weather_text = "🌤 **BUGUNGI KUTILAYOTGAN OB-HAVO (Min / Max):**\n\n"

    for city_name, (lat, lon) in CITIES.items():
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
            res = requests.get(url, timeout=5).json()

            min_temp = round(res["daily"]["temperature_2m_min"][0])
            max_temp = round(res["daily"]["temperature_2m_max"][0])

            weather_text += f"📍 **{city_name}:** {min_temp}°C ... {max_temp}°C\n"
        except Exception:
            weather_text += f"📍 **{city_name}:** Ma'lumot olinmadi\n"

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
