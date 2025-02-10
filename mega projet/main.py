import speech_recognition as sr
import pyttsx3
import webbrowser
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()

API_KEY = "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"  # Replace with your real API key
URL = "https://api.openai.com/v1/chat/completions"

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def fetch_openai_response(prompt):
    """Fetch a response from OpenAI API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",  # Use "gpt-4" if your account supports it
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": prompt}],
        "max_tokens": 100
    }

    try:
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()  # Check for HTTP errors
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
        print("Response:", response.text)  # Show error details
        return "Sorry, I couldn't fetch the response from OpenAI."
    except requests.exceptions.RequestException as err:
        print(f"API Error: {err}")
        return "Sorry, an error occurred while connecting to OpenAI."

def process(c):
    """Process the user command and take action."""
    c = c.lower().strip()  # Normalize input
    if "open google" in c:
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com")
    elif c.startswith("play"):
        song = c.replace("play ", "").strip()
        speak(f"Searching for {song} on YouTube...")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
    else:
        response = fetch_openai_response(c)
        speak(response)

def listen():
    """Capture and recognize voice commands."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Improve accuracy
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio).strip()
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            return None

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        command = listen()
        if command:
            process(command)
