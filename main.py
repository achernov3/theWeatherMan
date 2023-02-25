from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import emoji


app = Flask(__name__) # __name__ это ссылка на текущий файл main.py

URL  = "https://api.telegram.org/botTOKEN"

codes = {
    200: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],
    201: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],
    202: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],
    210: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],	
    211: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],
    212: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],
    221: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],
    230: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],
    231: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],
    232: ["Гроза", emoji.emojize(":cloud_with_lightning_and_rain:")],
    300: ["Мелкий дождь", emoji.emojize(":cloud_with_rain:")],
    301: ["Мелкий дождь", emoji.emojize(":cloud_with_rain:")],
    302: ["Мелкий дождь", emoji.emojize(":cloud_with_rain:")],
    310: ["Мелкий дождь", emoji.emojize(":cloud_with_rain:")],
    311: ["Мелкий дождь", emoji.emojize(":cloud_with_rain:")],
    312: ["Мелкий дождь", emoji.emojize(":cloud_with_rain:")],
    313: ["Мелкий дождь", emoji.emojize(":cloud_with_rain:")],
    314: ["Мелкий дождь", emoji.emojize(":cloud_with_rain:")],
    321: ["Мелкий дождь", emoji.emojize(":cloud_with_rain:")],
    500: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    501: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    502: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    503: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    504: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    511: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    520: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    521: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    522: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    531: ["Дождь", emoji.emojize(":cloud_with_rain:")],
    600: ["Снег", emoji.emojize(":cloud_with_snow:")],
    601: ["Снег", emoji.emojize(":cloud_with_snow:")],
    602: ["Снег", emoji.emojize(":cloud_with_snow:")],
    611: ["Снег", emoji.emojize(":cloud_with_snow:")],
    612: ["Снег", emoji.emojize(":cloud_with_snow:")],
    613: ["Снег", emoji.emojize(":cloud_with_snow:")],
    615: ["Снег", emoji.emojize(":cloud_with_snow:")],
    616: ["Снег", emoji.emojize(":cloud_with_snow:")],
    620: ["Снег", emoji.emojize(":cloud_with_snow:")],
    621: ["Снег", emoji.emojize(":cloud_with_snow:")],
    622: ["Снег", emoji.emojize(":cloud_with_snow:")],
    701: ["Туман", emoji.emojize(":fog:")],
    711: ["Туман", emoji.emojize(":fog:")],
    721: ["Туман", emoji.emojize(":fog:")],
    731: ["Туман", emoji.emojize(":fog:")],
    741: ["Туман", emoji.emojize(":fog:")],
    751: ["Туман", emoji.emojize(":fog:")],
    761: ["Туман", emoji.emojize(":fog:")],
    762: ["Туман", emoji.emojize(":fog:")],
    771: ["Туман", emoji.emojize(":fog:")],
    781: ["Туман", emoji.emojize(":fog:")],
    800: ["Ясно", emoji.emojize(":sun_with_face:")],
    801: ["Небольшая облачность", emoji.emojize(":sun_behind_small_cloud:")],
    802: ["Переменная облачность", emoji.emojize(":sun_behind_large_cloud:")],
    803: ["Значительная облачность", emoji.emojize(":sun_behind_large_cloud:")],
    804: ["Пасмурно", emoji.emojize(":cloud:")]
}

def write_json(data, filename = "answer.json"):
    """Функция записи ответов в формате json
    Помогает удобнее читать и парсить ответы"""
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_weather(city: str):
    """Функция дергает API по названию города
    Результат функции приходит пользователю от бота"""
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=API_KEY")
    j = r.json()
    temp = j["main"]["temp"]
    feels_like = j["main"]["feels_like"]
    humidity = j["main"]["humidity"]
    weather_code = j["weather"][0]["id"]
    weather = codes[weather_code][0]
    weather_emoji = codes[weather_code][1]
    return f"{city} \nТемпература: {temp}, \nОщущается как {feels_like}, \nВлажность: {humidity}%, \n{weather}{weather_emoji}"

def send_message(chat_id: int, text: str):
    """Функция отправки сообщения
    Вызывается с двумя параметрами
    """
    url = URL + "sendMessage"
    answer = {
        "chat_id": chat_id,
        "text": text
    }
    r = requests.post(url, json=answer)
    return r.json()

@app.route("/", methods=["POST", "GET"])
def index():
    """Webhook
    Отправка сообщений от пользователя боту через метод POST
    Отвечаем пользователю, вызовом функции get_weather"""
    if request.method == "POST":
        r = request.get_json()
        city = r["message"]["text"]
        chat_id = r["message"]["chat"]["id"]
        send_message(chat_id=chat_id, text=get_weather(city))
        return jsonify(r)
    return "<h1>HEllo</h1>"

if __name__ == "__main__":
    app.run()