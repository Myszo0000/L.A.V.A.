import os
import openai
import requests
import datetime

try:
    import speech_recognition as sr
    import pyttsx3
    USE_SPEECH = True
except ImportError:
    USE_SPEECH = False

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ustaw swój klucz API
openai.api_key = OPENAI_API_KEY

def speak(text):
    if USE_SPEECH:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        print("[AI]:", text)

def recognize_speech():
    if USE_SPEECH:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Powiedz coś...")
            audio = r.listen(source)
        try:
            return r.recognize_google(audio, language="pl-PL")
        except Exception as e:
            print("Nie rozpoznano mowy:", e)
            return ""
    else:
        return input("Ty: ")

def get_gpt_response(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "Jesteś zaawansowanym polskim asystentem AI."},
                  {"role": "user", "content": prompt}],
        max_tokens=400
    )
    return response["choices"][0]["message"]["content"]

def get_weather(city):
    # Użyj swojego klucza API np. OpenWeatherMap
    API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=pl&units=metric"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Pogoda w {city}: {desc}, {temp}°C"
    else:
        return "Nie udało się pobrać pogody."

def handle_command(command):
    command = command.lower()
    if "pogoda" in command:
        miasto = command.split("w")[-1].strip()
        return get_weather(miasto)
    elif "notatka" in command:
        note = command.partition("notatka")[2].strip()
        with open("notatki.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()}: {note}\n")
        return "Notatka zapisana."
    elif "przypomnij" in command:
        return "Funkcja przypomnień do zaimplementowania."
    else:
        return get_gpt_response(command)

def main():
    speak("Witaj! Jestem zaawansowanym asystentem AI. Jak mogę Ci pomóc?")
    while True:
        if USE_SPEECH:
            text = recognize_speech()
        else:
            text = input("Ty: ")
        if text.lower() in ["wyjdź", "exit", "quit"]:
            speak("Do widzenia!")
            break
        response = handle_command(text)
        speak(response)

if __name__ == "__main__":
    main()
