"""
Task 8: AI Virtual Assistant (Mini)
Install first:  pip install speechrecognition pyttsx3 pyaudio

Loop: listen -> recognize -> match command -> act -> speak
"""

import datetime
import os
import random
import subprocess
import webbrowser

import speech_recognition as sr
import pyttsx3

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the developer go broke? Because they used up all their cache.",
    "I would tell you a UDP joke, but you might not get it.",
]

# Note: closing a single tab isn't possible from here since webbrowser.open()
# gives no handle back. "Close" commands close the whole app/browser instead.
CLOSE_TARGETS = {
    "chrome.exe": ["youtube", "google", "whatsapp", "chrome"],
    "notepad.exe": ["notepad"],
    "calculator.exe": ["calculator", "calc"],  # calc.exe launches this on Win10/11
}

engine = pyttsx3.init()
engine.setProperty("rate", 175)  # default ~200 but varies by system; tune 150-200 to taste
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8  # shorter pause = quicker cutoff after you stop talking


def close_app(process_name: str) -> None:
    subprocess.run(["taskkill", "/im", process_name, "/f"], capture_output=True)


def speak(text: str) -> None:
    print(f"Assistant: {text}")  # kept for accessibility (visible + audible output)
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    with sr.Microphone() as source:  # add device_index=N here if list_mics.py shows the wrong default mic
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=6)

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Speech service is unavailable right now.")
    return ""


def handle_command(command: str) -> bool:
    """Returns False to stop the assistant."""
    if not command:
        return True

    if "close" in command:
        for process_name, keywords in CLOSE_TARGETS.items():
            if any(keyword in command for keyword in keywords):
                close_app(process_name)
                speak(f"Closing {process_name.replace('.exe', '')}")
                return True
        speak("I don't know what to close")
    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp Web")
    elif "search for" in command:
        query = command.split("search for", 1)[1].strip()
        if query:
            webbrowser.open(f"https://google.com/search?q={query}")
            speak(f"Searching for {query}")
        else:
            speak("What should I search for?")
    elif "open notepad" in command:
        os.startfile("notepad.exe")
        speak("Opening Notepad")
    elif "open calculator" in command:
        os.startfile("calc.exe")
        speak("Opening Calculator")
    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")
    elif "hello" in command or "hi" in command:
        hour = datetime.datetime.now().hour
        greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
        speak(greeting)
    elif "joke" in command:
        speak(random.choice(JOKES))
    elif "stop" in command or "exit" in command or "bye" in command:
        speak("Goodbye")
        return False
    else:
        speak("I don't know that command yet")

    return True


if __name__ == "__main__":
    with sr.Microphone() as mic_source:
        print("Calibrating for background noise...")
        recognizer.adjust_for_ambient_noise(mic_source, duration=1)

    speak("Assistant ready. Say a command.")
    running = True
    while running:
        running = handle_command(listen())