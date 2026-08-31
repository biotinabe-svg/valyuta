import os
import requests
import time
from datetime import datetime

# ----------------- SOZLAMALAR -----------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "8857142678:AAHGFzU_z80GM7Lk42b2ZMX69GLr04D7ErI")
CHANNEL_ID = "@annapida"

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

WEEKDAYS = {
    0: "Dushanba", 1: "Seshanba", 2: "Chorshanba",
    3: "Payshanba", 4: "Juma", 5: "Shanba", 6: "Yakshanba"
}

CURRENCY_EMOJIS = {
    "USD": "🇺🇸 1 USD",
    "EUR": "🇪🇺 1 EUR",
    "RUB": "🇷🇺 1 RUB",
    "TRY": "🇹🇷 1 TRY"
}

# ----------------- OB-HAVO OLISH (OPEN-METEO / KALITSIZ) -----------------
def get_weather():
    text = "🌤 **BUGUNGI OB-HAVO MA'LUMOTLARI**\n\n"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for city, (lat, lon) in CITIES.items():
        # Open-Meteo bepul API (API Key talab qilmaydi)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                temp_min = round(data["daily"]["temperature_2m_min"][0])
                temp_max = round(data["daily"]["temperature_2m_max"][0])
                
                if temp_min == temp_max:
                    text += f"📍 **{city}**: {temp_max}°C\n"
                else:
                    text += f"📍 **{city}**: {temp_min}°C ... {temp_max}°C\n"
            else:
                text += f"📍 **{city}**: Ma'lumot olinmadi\n"
        except Exception:
            text += f"📍 **{city}**: Ulanishda xatolik\n"
        
        time.sleep(0.2)
        
    return text

# ----------------- VALYUTA KURSI OLISH -----------------
def get_currency():
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    text = "\n💱 **MARKAZIY BANK VALYUTA KURSLARI**\n\n"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    target_order = ["USD", "EUR", "RUB", "TRY"]
    rates_dict = {}
    
    try:
        res = requests.get(url, headers=headers, timeout=8, verify=False)
        if res.status_code == 200:
            data = res.json()
            for item in data:
                ccy = item.get("Ccy")
                if ccy in target_order:
                    rate = float(item.get("Rate", 0))
                    formatted_rate = f"{rate:,.2f}".replace(",", " ").replace(".00", "")
                    rates_dict[ccy] = formatted_rate
            
            for ccy in target_order:
                if ccy in rates_dict:
                    label = CURRENCY_EMOJIS.get(ccy, f"🔹 1 {ccy}")
                    text += f"{label} = **{rates_dict[ccy]}** so'm\n"
        else:
            text += "Valyuta kurslarini olishda xatolik yuz berdi.\n"
    except Exception:
        text += "Valyuta serveriga bog'lanishda xatolik yuz berdi.\n"
        
    return text

# ----------------- TELEGRAMGA YUBORISH -----------------
def send_to_telegram(message_text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message_text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Post kanala muvaffaqiyatli yuborildi!")
        else:
            print(f"Telegramga yuborishda xatolik: {response.text}")
    except Exception as e:
        print(f"Telegram API ulanishda xatolik: {e}")

# ----------------- ASOSIY QISM -----------------
if __name__ == "__main__":
    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    weekday_str = WEEKDAYS[now.weekday()]
    
    header = f"📅 **{date_str} - {weekday_str}**\n\n"
    
    weather_info = get_weather()
    currency_info = get_currency()
    
    full_text = f"{header}{weather_info}{currency_info}"
    send_to_telegram(full_text)
