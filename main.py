import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import sys
import subprocess
import datetime
import random
import cohere
import re
from config import apikey

def sanitize_filename(name):
    # Remove invalid filename characters and limit length
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip().replace(" ", "_")
    return name[:50]

def ai(prompt):
    try:
        co = cohere.Client(api_key=apikey)

        # Send the prompt to Cohere
        res = co.chat(
            model="command-r-plus",
            message=prompt
        )

        # Get the actual AI response
        text = res.text
        # print(text)

    except Exception as e:
        print(f"An error occurred: {e}")
        text = "Error: Could not generate response."

    # Ensure 'Generated' folder exists
    if not os.path.exists("Generated"):
        os.mkdir("Generated")

    safe_filename = sanitize_filename(prompt)
    file_path = f"Generated/{safe_filename}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)  # Slower speech rate
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query
        except Exception as e:
            print("Sorry, I didn't catch that.")
            return ""

def play_random_music_from_directory(music_dir):
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
        say("Music folder created, but it's empty.")
        return
    songs = [file for file in os.listdir(music_dir) if file.endswith(".mp3")]
    if not songs:
        say("No music files found in the folder.")
        return
    song_path = os.path.join(music_dir, random.choice(songs))
    say("Playing a random song.")
    if sys.platform == "win32":
        os.startfile(song_path)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, song_path])

if __name__ == "__main__":
    print("Hello, I am your David AI.")
    say("Hello, I am your David A I.")

    # Define your music directory
    music_dir = r"c:\Users\priya\PycharmProjects\PythonProject\music"

    while True:
        query = takeCommand().lower()
        sites = [
            ["youtube", "https://www.youtube.com/"],
            ["wikipedia", "https://en.wikipedia.org/"],
            ["google", "https://google.com/"]
        ]
        site_opened = False

        # Check for site opening
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                site_opened = True
                break

        # Check for named music files
        music_files = [
            ["calm", os.path.join(music_dir, "calm-song.mp3")],
            ["focus", os.path.join(music_dir, "focus-track.mp3")],
            ["ambient", os.path.join(music_dir, "ambient-loop.mp3")]
        ]
        music_matched = False

        for song in music_files:
            if f"play {song[0]}" in query:
                say(f"Playing {song[0]} music...")
                if sys.platform == "win32":
                    os.startfile(song[1])
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, song[1]])
                music_matched = True
                break

        # Random music
        # if "start music" in query and not music_matched:
        #     play_random_music_from_directory(music_dir)
        #     continue

        # Time announcement
        if "time" in query:
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {nowtime}")

        apps = [
            ["notepad", "notepad.exe"],
            ["calculator", "calc.exe"],
            ["paint", "mspaint.exe"],
            ["command prompt", "cmd.exe"],
            # ["chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe"],
            # ["discord", r"C:\Users\priya\AppData\Local\Discord.exe"]
        ]

        for app in apps:
            if f"open {app[0]}" in query:
                say(f"Opening {app[0]}...")
                os.startfile(app[1])
                app_opened = True
                break

        if "using AI".lower() in query.lower():
            ai(prompt=query)

        # Fallback response
        if not site_opened and query:
            say(query)
