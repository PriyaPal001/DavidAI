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

chatStr = ""
conversation_file_path = None

def chat(query):
    global chatStr, conversation_file_path

    try:
        co = cohere.Client(api_key=apikey)

        chatStr += f"User: {query}\nDavid:"

        res = co.chat(
            model="command-r-plus",
            message=query,
            chat_history=[
                {"role": "USER", "message": query},
            ]
        )

        text = res.text
        chatStr += f" {text}\n"

        say(text)

        if not os.path.exists("Generated"):
            os.mkdir("Generated")

        if conversation_file_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            conversation_file_path = f"Generated/conversation_{timestamp}.txt"

        with open(conversation_file_path, "w", encoding="utf-8") as f:
            f.write(chatStr)

        return text

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error: Could not generate response."

def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip().replace(" ", "_")
    return name[:50]

def ai(prompt):
    try:
        co = cohere.Client(api_key=apikey)

        res = co.chat(
            model="command-r-plus",
            message=prompt
        )

        text = res.text

    except Exception as e:
        print(f"An error occurred: {e}")
        text = "Error: Could not generate response."

    if not os.path.exists("Generated"):
        os.mkdir("Generated")

    safe_filename = sanitize_filename(prompt)
    file_path = f"Generated/{safe_filename}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)
    engine.setProperty('volume', 1.0)
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

    music_dir = r"c:\Users\priya\PycharmProjects\PythonProject\music"

    while True:
        query = takeCommand().lower()
        handled = False

        sites = [
            ["youtube", "https://www.youtube.com/"],
            ["wikipedia", "https://en.wikipedia.org/"],
            ["google", "https://google.com/"]
        ]

        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                handled = True
                break

        music_files = [
            ["break", os.path.join(music_dir, "break.mp3")],
            ["focus", os.path.join(music_dir, "focus-track.mp3")],
            ["sweet", os.path.join(music_dir, "sweet.mp3")]
        ]

        for song in music_files:
            if f"play {song[0]}" in query:
                say(f"Playing {song[0]} music...")
                if sys.platform == "win32":
                    os.startfile(song[1])
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, song[1]])
                handled = True
                break

        apps = [
            ["notepad", "notepad.exe"],
            ["calculator", "calc.exe"],
            ["paint", "mspaint.exe"],
            ["command prompt", "cmd.exe"]
        ]

        for app in apps:
            if f"open {app[0]}" in query:
                say(f"Opening {app[0]}...")
                os.startfile(app[1])
                handled = True
                break

        if "time" in query:
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {nowtime}")
            handled = True

        elif "using ai" in query:
            ai(prompt=query)
            handled = True

        elif "david quit" in query:
            exit()

        elif "reset chat" in query:
            chatStr = ""
            handled = True

        elif not handled and query:
            print("chatting....")
            chat(query)
