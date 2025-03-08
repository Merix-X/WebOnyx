import random
import sys
import time
import threading
from time import sleep

import clipboard
import webbrowser
import shutil
import datetime
import light_control as lg
import requests
import os.path
import pyttsx3
from openai import OpenAI
from pathlib import Path
import subprocess
import os
import IS
import cups
import ollama
import speech_recognition as sr
from room_administratorModule import SearchItemInRoom
import face_recognizing as fr
import code_generation as code
from datetime import datetime, timedelta
import cv2
from email_sending import send_email
import pygame
import GenPass_Module as passwd

class Audio:
    def __init__(self):
        self.say(self=Audio)
        self.play(Audio)
        self.TakeCommand(Audio)
        self.play_song(Audio)
        self.TakeCommandCZ(Audio)
        self.Engine_say(Audio)
        self.beep(Audio)

    client_text_to_audio = OpenAI(api_key="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")
    engine = pyttsx3.init(debug=True)

    def TakeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            os.system("clear")
            print("If you don't say anything, it only takes 3 seconds to recognize.\nListening...")
            r.pause_threshold = 1
            # Set timeout to 5 seconds
            audio = r.listen(source, timeout=3)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio) #, language='en')
        except Exception as e:
            print("Say that again please...")
            os.system("clear")
            return "None"
        return query

    def TakeCommandCZ(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Naslouchání...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Rozpoznávání...")
            query = r.recognize_google(audio, language='cs-CZ')
        except Exception as e:
            print("Řekněte to znovu prosím...")
            os.system("clear")
            return "None"
        print(query)
        return query

    def play(self, audio):
        """from playsound import playsound
        playsound(audio)
        print('playing sound using  playsound')"""
        pygame.init()
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1.5)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

    def beep(self):
        Audio.play(Audio, r"./beepsound.wav")

    def beep_false(self):
        Audio.play(Audio, r"./beepsoundfalse.wav")

    def say(self, text):
        try:
            speech_file_path = Path(__file__).parent / "speech.mp3"
            response = Audio.client_text_to_audio.audio.speech.create(
                model="tts-1",
                voice="echo",
                input=text
            )
            response.stream_to_file(speech_file_path)
            Audio.play(Audio, "speech.mp3")
            time.sleep(2)
        except Exception as e:
            Audio.Engine_say(Audio, text)
        """try:
            os.remove("speech.mp3")
        except PermissionError as e:
            print(e)"""

    def Engine_say(self, text):
        Audio.engine.say(text)
        Audio.engine.runAndWait()
        Audio.engine.stop()

    def play_song(self):
        def play_music():
            music_to_play = random.choice(
                ["https://open.spotify.com/album/2r1JyHCVfb1ZUxwb5CzSns?si=L_LxWRNGQNSmMkIqIM1dDA",
                 "https://open.spotify.com/playlist/3FQeJxxhq2ikidGVPasRDg?si=93b441cf62c14c57",
                 "https://open.spotify.com/playlist/5xnSHGRHQcaeddRyBDJCKR?si=e223f036c69b45bc",
                 "https://open.spotify.com/album/2DgHSM6kuXPBySWaG5WQUo?si=df9iENb4QPCQ5qLOpf-xJQ"])
            webbrowser.open(music_to_play)
            time.sleep(5)
            os.system('taskkill /im firefox.exe')
        # Function to listen for the "stop" command
        def listen():
            while True:
                command = Audio.TakeCommand(Audio).lower()
                tasklist = os.system("tasklist")
                print(tasklist)
                if "stop" in command:
                    print("Playing was stopped")
                    try:
                        os.system('taskkill /im Spotify.exe')
                    except Exception:
                        print("The spotify program is not open")
                        Audio.Engine_say(Audio, "The spotify program is not open")
                    Audio.Engine_say(Audio, "Playing was stoped")
                    OnyxAI.mainloop("self")
                    break
                elif "Spotify.exe" in tasklist:
                    break

        play_thread = threading.Thread(target=play_music)
        listen_thread = threading.Thread(target=listen)

        play_thread.start()
        listen_thread.start()

        play_thread.join()
        listen_thread.join()

class Camera:
    def take_photo(self):
        if os.path.exists("photo.png"):
            os.remove("photo.png")
        cam_port = 0
        cam = cv2.VideoCapture(cam_port)

        # reading the input using the camera
        result, image = cam.read()

        # If image will detected without any error,
        # show result
        if result:

            # showing result, it take frame name and image
            # output
            cv2.imshow("Capture", image)

            # saving image in local storage
            cv2.imwrite("photo.png", image)

            # If keyboard interrupt occurs, destroy image
            # window
            # cv2.waitKey(0)
            cv2.destroyWindow("Capture")
            #os.system("xdg-open photo.png")

        # If captured image is corrupted, moving to else part
        else:
            print("No image detected. Please try again!")

class Answering:
    generate_answer = False
    listen1 = False
    def generate_response(self, prompt):
        if prompt != "":
            global returned_message
            returned_message = False
            print("\nOnyx is generating an answer for your question")

            stream = ollama.chat(
                model='llava',
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                stream=True
            )
            try:
                res = []
                for chunk in stream:
                    response = chunk['message']['content']
                    print(response, end='', flush=True)
                    res.append(response)
                response1 = "".join(res)
                Audio.say(Audio, response1)
                return response1
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                Audio.say(Audio, "An error occurred during response generation")
        else:
            print("Unfortunately, I didn't understand what you needed")
            Audio.say(Audio, "Unfortunately, I didn't understand what you needed")

    def Answer(self, prompt):
        global returned_message
        returned_message = False
        print("\nOnyx is generating an answer for your question")
        print(bool(Answering.generate_answer))

        stream = ollama.chat(
            model='phi3',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            stream=True
        )
        try:
            def generate():
                res = []
                for chunk in stream:
                    response = chunk['message']['content']
                    print(response, end='', flush=True)
                    res.append(response)
                if Answering.listen1 == True:
                    return
                else:
                    response1 = "".join(res)
                    Audio.say(Audio, response1)
                    Answering.generate_answer = True
                    return

            def listen():
                while (Answering.generate_answer == False):
                    query = Audio.TakeCommand(Audio)
                    if "stop" in query or "stop answering" in query:
                        Answering.listen1 = True
                        break

            answer_thread = threading.Thread(target=generate)
            listen_thread = threading.Thread(target=listen)

            answer_thread.start()
            listen_thread.start()

            listen_thread.join()
            print("listening/answering completed")
            answer_thread.join()
            return
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            Audio.say(Audio, "An error occurred during response generation")

    def RecognizePic(self, prompt):
        Camera.take_photo(Camera)
        stream = ollama.chat(
            model='llava',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                    'images': ['./photo.jpg']
                }
            ],
            stream=True
        )
        try:
            res = []
            for chunk in stream:
                response = chunk['message']['content']
                print(response, end='', flush=True)
                res.append(response)
            response1 = "".join(res)
            Audio.say(Audio, response1)
            return response1
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            Audio.say(Audio, "An error occurred during response generation")

    def Answer_sentence_or_command(self, prompt):
        stream = ollama.chat(
            model='Neo',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            stream=True
        )
        try:
            res = []
            for chunk in stream:
                response = chunk['message']['content']
                res.append(response)
            response1 = "".join(res)
            return response1
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            Audio.say(Audio, "An error occurred during response generation")

class Time:
    def __init__(self):
        self.current_time_to_integer(Time)
        self.time_now(Time)

    def current_time_to_integer(self):
        current_time = time.localtime()
        print(current_time)
        hours = current_time.tm_hour
        minutes = current_time.tm_min
        time_integer = f"{hours}:{minutes}"
        return time_integer

    def time_now(self):
        hour = datetime.now().hour
        min = datetime.now().minute
        return f"{hour}:{min}"

class Reminder:
    def __init__(self):
        self.remind(Reminder)
        self.remind_me(Reminder)
        self.cancel_reminder(Reminder)

    reminders = {}
    reminder = {}

    def remind(self, day, time3, message):
        try:
            """
            Nastaví připomenutí na určitý den a hodinu pomocí vlákna.

            Args:
                day (str): Den, kdy má být připomenutí (např. "zítra").
                time (str): Čas ve formátu "HH:MM".
                message (str): Zpráva, kterou chcete připomenout.
            """

            def prepare_reminder():
                # Převed den na datum
                global result
                day1 = {"day": day}
                today = datetime.now().date()
                time_now = Time.time_now(Time)
                time_to_remind = {"time": time_now}
                time2 = time3 + ":00"
                print(time2)
                first_space_position = time2.find(' ')
                if first_space_position != -1:
                    import re
                    result = re.sub(r'\s', '', time2)
                    print(result)
                if day.lower() == "tomorrow":
                    reminder_date = today + timedelta(days=1)
                elif day.lower() == "today":
                    reminder_date = today
                else:
                    print(day)


                if "i" in message:
                    message.replace("i", "you")
                elif "i'm" in message:
                    message.replace("i'm", "you")
                elif "i am" in message:
                    message.replace("i am", "you")
                elif "my" in message:
                    message.replace("my", "your")
                elif "me" in message:
                    message.replace("me", "you")

                # Převed čas na datetime objekt
                reminder_time = datetime.strptime(time2, "%H:%M")
                reminder_time = datetime.combine(reminder_date, reminder_time.time())

                OnyxAI.reminder = {"message": message}

                while True:
                    current_time = datetime.now()
                    if current_time >= reminder_time:
                        if day1.get("day") == "tomorrow":
                            print(
                                f"Sir, yesterday in {time_to_remind.get('time')} you told me to remind you today that {message}")
                            Audio.say(Audio,
                                       f"Sir, yesterday in {time_to_remind.get('time')} you told me to remind you today that {message}")
                            break
                        elif day1.get("day") == "today":
                            print(
                                f"Sir, today in {time_to_remind.get('time')} you told me to remind you today that {message}")
                            Audio.say(Audio,
                                       f"Sir, today in {time_to_remind.get('time')} you told me to remind you today that {message}")
                            break
                    time.sleep(60)  # Počkej 1 minutu a zkontroluj znovu

            # Vytvoř vlákno pro připomenutí
            thread = threading.Thread(target=prepare_reminder)
            # Ulož vlákno do in32clipboard as clipboardslovníku
            Reminder.reminders[message] = thread
            print(f"Reminders: {Reminder.reminders}")
            thread.start()
        except Exception:
            return False
        # Jinak
        return True

    def cancel_reminder(self, message):
        """
        Zruší připomenutí na základě zadané zprávy.

        Args:
            message (str): Zpráva, pro kterou chcete zrušit připomenutí.
        """
        if message in Reminder.reminders:
            Reminder.reminders[message].join()  # Počkej na dokončení vlákna
            del Reminder.reminders[message]
            print(f"The reminder for '{message}' has been deleted.")
            Audio.say(Audio, f"The reminder for '{message}' has been deleted.")
        else:
            print(f"The reminder for '{message}' has not been removed.")
            Audio.say(Audio, f"The reminder for '{message}' has not been removed.")

    # Příklad použití:
    def remind_me(self, prompt):
        parts = prompt.split("remind me ")

        def split(parts):
            parts = "".join(parts)
            parts1 = [parts]
            return parts1

        parts2 = split(parts)
        parts3 = "".join(parts2)
        parts4 = parts3.split(" in ")
        day, message, time_ = parts4[0], parts[1], parts4[1]
        time1 = time_[:2]
        print(f"Day to remind: {day}\nTime to remind: {time1}\nMessage for remind: {message}")
        remind1 = Reminder.remind(Reminder, day, time1, message)
        if remind1 == True:
            Audio.say(Audio, f"Sir, the reminder for {day} and hour {time1} has been set")
            print(f"Sir, the reminder for {day} and hour {time1} has been set")
            OnyxAI.mainloop("self")
        else:
            Audio.say(Audio, f"Unfortunately, I was unable to set the reminder to {day}.")
            print(f"Unfortunately, I was unable to set the reminder to {day}.")
            OnyxAI.mainloop("self")

class Weather:
    def __init__(self):
        self.get_weather(Weather)
        self.kelvin_to_celsius(Weather)

    def kelvin_to_celsius(self, kelvin):
        return kelvin - 273.15
    def get_weather(self):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + "f63a17de3e9d8227c3cfc22489eb6468" + "&q=" + "Králův Dvůr, Trubín"
        response = requests.get(complete_url)
        weather_data = response.json()

        # Create a dictionary with weather information
        weather_info = {
            "description": weather_data['weather'][0]['description'],
            "temperature": Weather.kelvin_to_celsius(Weather, weather_data['main']['temp']),
            "humidity": weather_data['main']['humidity'],
            "wind_speed": weather_data['wind']['speed']
        }
        return weather_info

class News:
    def __init__(self):
        self.latest_news(News)

    def latest_news(self, state1):
        try:
            global state
            # Definujte URL API pro News API
            api_url = "https://newsapi.org/v2/top-headlines"

            states = {"czech republic": "cz",
                      "united states": "us",
                      "united kingdom": "uk",
                      "slovakia": "sk",
                      "germany": "de"}
            if state1 == "czech republic":
                state = states.get("czech republic")
            elif state1 == "slovakia":
                state = states.get("slovakia")
            elif state1 == "united states":
                state = states.get("united states")
            elif state1 == "united kingdom":
                state = states.get("united kingdom")
            elif state1 == "germany":
                state = states.get("germany")
            # Definujte parametry dotazu
            params = {
                "country": state,
                "apiKey": "3de6a1343fff4290ab5b863ab4d34810"  # Nahraďte tímto klíčem svůj vlastní API klíč
            }

            # Pošlete GET požadavek na API
            response = requests.get(api_url, params=params)
            data = response.json()

            # Vypište nejnovější zprávy
            print(f"Here is the latest news from the {state1}:")
            print("=" * 50)

            for i, article in enumerate(data["articles"], start=1):
                stop = Audio.TakeCommandCZ(Audio).lower()
                if stop == "stop":
                    Audio.say(Audio, f"Of course, I don't want to keep you from your work, so this was probably the most important of the {state}. I hope I helped you.")
                    print(f"Of course, I don't want to keep you from your work, so this was probably the most important of the {state}. I hope I helped you.")
                    break
                else:
                    title = article["title"]
                    Audio.say(Audio, f"{i}. {title}")
                    print(f"{i}. {title}")
                    continue

        except Exception as e:
            print(f"Chyba: {str(e)}")

class Files:
    def __init__(self):
        self.find_files(Files)
    def find_files(self, filename, search_path):
        result = []

        # Wlaking top-down from the root
        for root, dir, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
        if len(result) == 1:
            return "".join(result)
        else:
            return result

class Projects:
    def __init__(self):
        self.create_project(Projects)

    projects = []

    def create_project(self, name):
        """Creates a directory named 'name' to represent a new project, along with some common
        initialization files."""

        # Create the main project directory
        os.makedirs(f"{name}", exist_ok=True)

        # Initialize README and .gitignore (assuming it's a Git repository)
        os.system(f"echo > {name}/README.md")

        with open(f"{name}/README.md", 'w') as file:
            file.write("Welcome to the new project!\n\n# Project Details...")

        os.system(f"echo > {name}/.gitignore")

        with open(f"{name}/.gitignore", 'w') as file:
            # Add common Git ignore patterns for a Python project
            file.write("node_modules/\n__pycache__/\n.DS_Store/")

        os.system(f"echo > {name}/main.py")

        with open(f"{name}/main.py", 'w') as file:
            # Add common Git ignore patterns for a Python project
            file.write("# This si the main file of your new project, Merix!")

        print(f"Created new project '{name}' with README and .gitignore files, + new pyhon file with name main.py")
        Audio.say(Audio, f"Created new project '{name}' with README and .gitignore files, + new pyhon file with name main.py. Would you like to open the project directory?")
        Projects.projects.append(name)
        while True:
            prompt = Audio.TakeCommand(Audio).lower()
            if prompt == "yes" or "yes" in prompt:
                os.system(f"start explorer {name}")
                break
            else:
                break

class Modes:
    def sleepMode(self):
        Audio.say(Audio, "Okay sir, I!m setting up the sleep mode and I!m going to sleep!")
        com_port = lg.list_all_ports()
        print(com_port)
        if com_port:
            print(f"Using port: {com_port}")
            lg.turn_off_power(com_port)
        else:
            print("No suitable port found.")
        Audio.say(Audio, "Only for info, I turned off the lights sir.")
        Sleep.go_sleep(Sleep)



class Greating:
    def __init__(self):
        self.greet_me(Greating)

    def greet_me(self):
        hour = int(datetime.now().hour)
        if hour >= 0 and hour < 12:
            if OnyxAI.name == "Merix" or OnyxAI.name == "Petr":
                greetings_evening = [
                    "Welcome back, sir. Do you have any specific priorities for today?",
                    "Sir, it's great to see you again. What are your current requests for the day?",
                    "Sir, I'm ready to fulfill your commands. What's on the agenda?",
                    "Good morning, sir. Do you already have any plans I should know about?",
                    "Welcome back, sir. Is there anything specific you'd like to focus on today?",
                    "Sir, what are your expectations for today?",
                    "Welcome back, sir. What's on your schedule for today?",
                    "Good morning, sir. Do you have any instructions for me to start working?"
                ]
                return random.choice(greetings_evening)
            elif OnyxAI.name == "Martina":
                greetings_evening = [
                    "Welcome back, ma'am. Do you have any specific priorities for today?",
                    "Ma'am, it's great to see you again. What are your current requests for the day?",
                    "Ma'am, I'm ready to fulfill your commands. What's on the agenda?",
                    "Good morning, ma'am. Do you already have any plans I should know about?",
                    "Welcome back, ma'am. Is there anything specific you'd like to focus on today?",
                    "ma'am, what are your expectations for today?",
                    "Welcome back, ma'am. What's on your schedule for today?",
                    "Good morning, ma'am. Do you have any instructions for me to start working?"
                ]
                return random.choice(greetings_evening)
        elif hour >= 12 and hour < 18:
            if OnyxAI.name == "Merix" or OnyxAI.name == "Petr" or OnyxAI.name == "Who are you?":
                greetings_evening = [
                    "Welcome back, sir. Do you have any specific priorities for today?",
                    "Sir, it's great to see you again. What are your current requests for the day?",
                    "Sir, I'm ready to fulfill your commands. What's on the agenda?",
                    "Good afternoon, sir. Do you already have any plans I should know about?",
                    "Welcome back, sir. Is there anything specific you'd like to focus on today?",
                    "Sir, what are your expectations for today?",
                    "Welcome back, sir. What's on your schedule for today?",
                    "Good evening, sir. Do you have any instructions for me to start working?"
                ]
                return random.choice(greetings_evening)
            elif OnyxAI.name == "Martina":
                greetings_evening = [
                    "Welcome back, ma'am. Do you have any specific priorities for today?",
                    "Ma'am, it's great to see you again. What are your current requests for the day?",
                    "Ma'am, I'm ready to fulfill your commands. What's on the agenda?",
                    "Good afternoon, ma'am. Do you already have any plans I should know about?",
                    "Welcome back, ma'am. Is there anything specific you'd like to focus on today?",
                    "ma'am, what are your expectations for today?",
                    "Welcome back, ma'am. What's on your schedule for today?",
                    "Good afternoon, ma'am. Do you have any instructions for me to start working?"
                ]
                return random.choice(greetings_evening)
        elif hour >= 18 and hour < 00:
            if OnyxAI.name == "Merix" or OnyxAI.name == "Petr":
                greetings_evening = [
                    "Welcome back, sir. Do you have any specific priorities for today?",
                    "Sir, it's great to see you again. What are your current requests for the day?",
                    "Sir, I'm ready to fulfill your commands. What's on the agenda?",
                    "Good evening, sir. Do you already have any plans I should know about?",
                    "Welcome back, sir. Is there anything specific you'd like to focus on today?",
                    "Sir, what are your expectations for today?",
                    "Welcome back, sir. What's on your schedule for today?",
                    "Good evening, sir. Do you have any instructions for me to start working?"
                ]
                return random.choice(greetings_evening)
            elif OnyxAI.name == "Martina":
                greetings_evening = [
                    "Welcome back, ma'am. Do you have any specific priorities for today?",
                    "Ma'am, it's great to see you again. What are your current requests for the day?",
                    "Ma'am, I'm ready to fulfill your commands. What's on the agenda?",
                    "Good evening, ma'am. Do you already have any plans I should know about?",
                    "Welcome back, ma'am. Is there anything specific you'd like to focus on today?",
                    "ma'am, what are your expectations for today?",
                    "Welcome back, ma'am. What's on your schedule for today?",
                    "Good evening, ma'am. Do you have any instructions for me to start working?"
                ]
                return random.choice(greetings_evening)
        else:
            if OnyxAI.name == "Merix" or OnyxAI.name == "Petr":
                greetings_evening = [
                    "Welcome back, sir. Do you have any specific priorities for today?",
                    "Sir, it's great to see you again. What are your current requests for the day?",
                    "Sir, I'm ready to fulfill your commands. What's on the agenda?",
                    "Good night, sir. Do you already have any plans I should know about?",
                    "Welcome back, sir. Is there anything specific you'd like to focus on today?",
                    "Sir, what are your expectations for today?",
                    "Welcome back, sir. What's on your schedule for today?",
                    "Good night, sir. Do you have any instructions for me to start working?"
                ]
                return random.choice(greetings_evening)
            elif OnyxAI.name == "Martina":
                greetings_evening = [
                    "Welcome back, ma'am. Do you have any specific priorities for today?",
                    "Ma'am, it's great to see you again. What are your current requests for the day?",
                    "Ma'am, I'm ready to fulfill your commands. What's on the agenda?",
                    "Good night, ma'am. Do you already have any plans I should know about?",
                    "Welcome back, ma'am. Is there anything specific you'd like to focus on today?",
                    "ma'am, what are your expectations for today?",
                    "Welcome back, ma'am. What's on your schedule for today?",
                    "Good night, ma'am. Do you have any instructions for me to start working?"
                ]
                return random.choice(greetings_evening)

class Sending:
    def __init__(self):
        self.__init__(Sending)
        self.send_email(Sending)

    def send_email(self, receiver_email, subject, message):
        status = send_email(receiver_email, subject, message)
        if status:
            Audio.say(Audio, f"Success! Your email for {receiver_email} was been sent successfully!")
            return True
        elif status == False:
            Audio.say(Audio, f"Unfortunately, the email to {receiver_email} was not sent correctly. Please try to send this email again later.")
            return False

class Sleep:
    def go_sleep(self):
        Audio.say(Audio, "Okay, if you need anything, let me know")
        print("Okay, if you need anything, let me know")

        def while_1():
            a = 0
            while True:
                if int(datetime.now().hour) >= 21:
                    Audio.say(Audio,
                               "Sir, it seems too late, I'll probably have to retire for the night, and you should probably get some rest too.")
                    print(
                        "Sir, it seems too late, I'll probably have to retire for the night, and you should probably get some rest too.")
                    time.sleep(5)
                    print("I'm sleeping now...")
                    while True:
                        now_time = self.time_now(OnyxAI)
                        if now_time == "6:50":
                            # Získání aktuálního data
                            dnes = datetime.today()
                            if dnes.weekday() in [5, 6]:
                                continue
                            else:
                                weather_info = Weather.get_weather(Weather)
                                description = weather_info['description']
                                temperature = f"{weather_info['temperature']:.2f}"
                                Humidity = weather_info['humidity']
                                WindSpeed = weather_info['wind_speed']
                                Audio.say(Audio,
                                           f"Good morning, sir. It's {now_time} a.m., and I understand you're supposed to get up. Weather description is: {description}. Temperature is: {temperature} °Celsius. Humidity is: {Humidity} Percent. And wind speed is: {WindSpeed}, meters per second.")
                                Audio.say(Audio,
                                           "Would you like me to give you the latest news from the Czech Republic, sir?")
                                print(
                                    f"Good morning, sir. It's {now_time} a.m., and I understand you're supposed to get up. Weather description is: {description}. Temperature is: {temperature}. Humidity is: {Humidity}%, and wind speed is: {WindSpeed} m/s. Would you like me to give you the latest news from the Czech Republic, sir?")
                                while True:
                                    command = Audio.TakeCommand(Audio)
                                    if "yes" in command or "sure" in command:
                                        Audio.say(Audio,
                                                   "Okay, here is some information from the Czech Republic")
                                        print("Okay, here is some information from the Czech Republic")
                                        News.latest_news(News, "czech republic")
                                        break
                                    else:
                                        Audio.say(Audio,
                                                   "You don't want to, do you? Well, never mind, if you need anything sir, feel free to get in touch!")
                                        print(
                                            "You don't want to, do you? Well, never mind, if you need anything sir, feel free to get in touch!")
                                        break
                                break
                        elif now_time == "8:45":
                            dnes = datetime.today()
                            if dnes.weekday() in [5, 6]:
                                weather_info = Weather.get_weather(Weather)
                                description = weather_info['description']
                                temperature = f"{weather_info['temperature']:.2f}"
                                Humidity = weather_info['humidity']
                                WindSpeed = weather_info['wind_speed']
                                Audio.say(Audio,
                                           f"Good morning, sir. It's {now_time} a.m. Weather description is: {description}. Temperature is: {temperature} °Celsius. Humidity is: {Humidity} Percent. And wind speed is: {WindSpeed}, meters per second")
                                Audio.say(Audio,
                                           "Would you like me to give you the latest news from the Czech Republic, sir?")
                                print(
                                    f"Good morning, sir. It's {now_time} a.m. Weather description is: {description}. Temperature is: {temperature}. Humidity is: {Humidity}%, and wind speed is: {WindSpeed} m/s. Would you like me to give you the latest news from the Czech Republic, sir?")
                                while True:
                                    command = Audio.TakeCommand(Audio)
                                    if "yes" in command or "sure" in command:
                                        Audio.say(Audio, "Okay, here is some information from the Czech Republic")
                                        print("Okay, here is some information from the Czech Republic")
                                        News.latest_news(News, state1="czech republic")
                                        break
                                    else:
                                        Audio.say(Audio,
                                                   "You don't want to, do you? Well, never mind, if you need anything sir, feel free to get in touch!")
                                        print(
                                            "You don't want to, do you? Well, never mind, if you need anything sir, feel free to get in touch!")
                                        break
                                break
                        time.sleep(60)
                prompt_for_wake_up = Audio.TakeCommand(Audio).lower()
                if prompt_for_wake_up == "onyx":
                    Audio.say(Audio, f"Yeah {OnyxAI.name}? I'm listening to you")
                    print(f"Yeah {OnyxAI.name}? I'm listening to you")
                    return "finish"
                elif a == 30:
                    return "stoped"
                a = + 1

        if while_1() == "finish":
            pass
        elif while_1() == "stoped":
            Audio.Engine_say(Audio, " Restarting")
            while_1()

    def sleep_throught_night(self):
        Audio.say(Audio,
                   "Sir, it seems too late, I'll probably have to retire for the night, and you should probably get some rest too.")
        print(
            "Sir, it seems too late, I'll probably have to retire for the night, and you should probably get some rest too.")
        time.sleep(3)
        """for x in range(5):
            prompt = Audio.TakeCommand(Audio).lower()
            if "good night onyx" in prompt or "good night" in prompt or "see you tomorrow" in prompt or "see you tomorrow onyx" in prompt:
                Audio.say(Audio, "Good night, sir. I look forward to seeing you tomorrow.")
                print("Good night, sir. I look forward to seeing you tomorrow.")
                time.sleep(3)
                break"""
        print("I'm sleeping now...")
        while True:
            now_time = Time.time_now(Time)
            if now_time == "6:30":
                # Získání aktuálního data
                dnes = datetime.today()
                if dnes.weekday() in [5, 6]:
                    continue
                else:
                    weather_info = Weather.get_weather(Weather)
                    description = weather_info['description']
                    temperature = f"{weather_info['temperature']:.2f}"
                    Humidity = weather_info['humidity']
                    WindSpeed = weather_info['wind_speed']
                    Audio.say(Audio,
                               f"Good morning, sir. It's {now_time} a.m., and I understand you're supposed to get up. Weather description is: {description}. Temperature is: {temperature} °Celsius. Humidity is: {Humidity} Percent. And wind speed is: {WindSpeed}, meters per second.")
                    Audio.say(Audio,
                               "Would you like me to give you the latest news from the Czech Republic, sir?")
                    print(
                        f"Good morning, sir. It's {now_time} a.m., and I understand you're supposed to get up. Weather description is: {description}. Temperature is: {temperature}. Humidity is: {Humidity}%, and wind speed is: {WindSpeed} m/s. Would you like me to give you the latest news from the Czech Republic, sir?")
                    while True:
                        command = Audio.TakeCommand(Audio)
                        if "yes" in command or "sure" in command:
                            Audio.say(Audio, "Okay, here is some information from the Czech Republic")
                            print("Okay, here is some information from the Czech Republic")
                            News.latest_news(News, "czech republic")
                            break
                        else:
                            Audio.say(Audio,
                                       "You don't want to, do you? Well, never mind, if you need anything sir, feel free to get in touch!")
                            print(
                                "You don't want to, do you? Well, never mind, if you need anything sir, feel free to get in touch!")
                            break
                    break
            elif now_time == "7:15":
                dnes = datetime.today()
                if dnes.weekday() in [5, 6]:
                    weather_info = Weather.get_weather(Weather)
                    description = weather_info['description']
                    temperature = f"{weather_info['temperature']:.2f}"
                    Humidity = weather_info['humidity']
                    WindSpeed = weather_info['wind_speed']
                    Audio.say(Audio,
                               f"Good morning, sir. It's {now_time} a.m. Weather description is: {description}. Temperature is: {temperature} °Celsius. Humidity is: {Humidity} Percent. And wind speed is: {WindSpeed}, meters per second")
                    Audio.say(Audio,
                               "Would you like me to give you the latest news from the Czech Republic, sir?")
                    print(
                        f"Good morning, sir. It's {now_time} a.m. Weather description is: {description}. Temperature is: {temperature}. Humidity is: {Humidity}%, and wind speed is: {WindSpeed} m/s. Would you like me to give you the latest news from the Czech Republic, sir?")
                    while True:
                        command = Audio.TakeCommand(Audio)
                        if "yes" in command or "sure" in command:
                            Audio.say(Audio, "Okay, here is some information from the Czech Republic")
                            print("Okay, here is some information from the Czech Republic")
                            News.latest_news(News, "czech republic")
                            break
                        else:
                            Audio.say(Audio,
                                       "You don't want to, do you? Well, never mind, if you need anything sir, feel free to get in touch!")
                            print(
                                "You don't want to, do you? Well, never mind, if you need anything sir, feel free to get in touch!")
                            break
                    break
            time.sleep(60)

class Opening:
    def open_file_in_pycharm(self, filename, line_number):
        # Path to the PyCharm executable, change this if your path is different
        pycharm_path = '/snap/bin/pycharm-community'

        if not os.path.exists(pycharm_path):
            print(f"PyCharm executable not found at {pycharm_path}")
            return

        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            return

        # Construct the command to open PyCharm at the specified file and line
        command = [pycharm_path, '--line', str(line_number), filename]

        try:
            subprocess.run(command, check=True)
            print(f"Opened {filename} at line {line_number} in PyCharm.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open file in PyCharm: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

class Printing:
    def print(self, file_path):
        try:
            # Connect to CUPS
            conn = cups.Connection()

            printer_name = "Kyocera_ECOSYS_P5026cdw"

            # Get list of available printers
            printers = conn.getPrinters()

            print("Available printers: \n")
            for printer in printers:
                print(f" - {printer}")

            if printer_name not in printers:
                print(f"Printer '{printer_name}' not found. Available printers:")
                for printer in printers:
                    print(f" - {printer}")
                return

            # Print the file
            print_job_id = conn.printFile(printer_name, file_path, "Print Job", {})
            print(f"Print job sent successfully. Job ID: {print_job_id}")
            Audio.say(Audio, "The text have been sent to print successfully, sir!")

        except Exception as e:
            print(f"An error occurred: {e}")

class OnyxAI:
    def __init__(self):
        self.generate_response(OnyxAI)
        self.go_sleep(OnyxAI)
        self.sleep_throught_night(OnyxAI)
        self.main(OnyxAI)
        self.greet_me(OnyxAI)
        self.mainloop(OnyxAI)

    client_draw = OpenAI(api_key="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")
    name = fr.recognize_face()
    print(name)
    if str(name) != "Merix":
        Audio.beep_false(Audio)
        sys.exit()
    #name = str(input("Who's using Onyx now?: "))
    notes = []
    experience = []
            
    def print(file):
        os.system(f"nc -nv 192.168.1.66 80 < {file}")

    def mainloop(self):
        for x in range(10):
            try:
                global response_bool
                global response_from_ai
                response_from_ai = ""
                response_bool = None
                for y in range(3):
                    if int(datetime.now().hour) >= 21:
                        Sleep.sleep_throught_night(Sleep)
#                   -------------------------------------------------
                    print("Listening for command...")
                    prompt = Audio.TakeCommand(Audio).lower()
                    print(f"User: {prompt}")

                    if prompt == "onyx":
                        Audio.say(Audio, f"Yeah {OnyxAI.name}? I'm listening to you")
                        print(f"Yeah {OnyxAI.name}? I'm listening to you")
                        continue

                    elif "i'm idiot" in prompt or "i am idiot" in prompt:
                        Audio.say(Audio,
                                  "No, you're really not, you programmed me which proves you're 'idiot' not!")
                        print("No, you're really not, you programmed me which proves you're 'idiot' not!")

                    elif "shit" in prompt or "holy shit" in prompt:
                        Audio.say(Audio,
                                  "What's the matter, sir, that you use such harsh words?, Can I help you with something?")
                        print(
                            "What's the matter, sir, that you use such harsh words?, Can I help you with something?")

                    elif "onyx" in prompt:
                        prompt = prompt.split("onyx")[-1].strip()
                        if "thank you" in prompt or "thanks" in prompt:
                            Audio.say(Audio,
                                      "You're welcome, sir! Glad to help. If you have any further questions or commands, I'll be happy to help.")
                            print(
                                "You're welcome, sir! Glad to help. If you have any further questions or commands, I'll be happy to help.")

                        elif "what's the weather like" in prompt:
                            weather_info = Weather.get_weather(Weather)
                            description = weather_info['description']
                            temperature = f"{weather_info['temperature']:.2f}"
                            Humidity = weather_info['humidity']
                            WindSpeed = weather_info['wind_speed']
                            Audio.say(Audio,
                                      f"Weather description is: {description} Temperature is: {temperature} °Celsius. Humidity is: {Humidity} Percent. And wind speed is: {WindSpeed}, meters per second")
                            print(
                                f"Weather description is: {description} Temperature is: {temperature} °C. Humidity is: {Humidity}%, and wind speed is: {WindSpeed} m/s")
                            pass

                        elif "what's the temperature" in prompt or "what is the temperature" in prompt:
                            weather_info = Weather.get_weather(Weather)
                            temperature = f"{weather_info['temperature']:.2f}"
                            Audio.say(Audio, f"The temperature outside is now: {temperature} °Celsius.")
                            print(f"The temperature outside is now: {temperature} °Celsius.")
                            pass

                        elif "tell me what's new in the" in prompt:
                            News.latest_news("self", prompt.split("tell me what's new in the ")[-1].strip())

                        elif "who are you" in prompt or "can you introduce yourself" in prompt:
                            """print("I am ONYX, an artificial intelligence system created by Merix. I am here to serve as a personal assistant and support to my master, whether in helping to answer important questions and analyze data, or in day-to-day tasks.")
                            OnyxAI.say("self", "I am Onyx, an artificial intelligence system created by Merix. I am here to serve as a personal assistant and support to my master, whether in helping to answer important questions and analyze data, or in day-to-day tasks.")"""
                            Answering.generate_response(Answering,
                                                        random.choice(["Who are you?", "Can you introduce yourself?"]))
                            time.sleep(2.5)
                            print("\nI'm listening for command...")
                            pass

                        elif "what is your purpose" in prompt or "what is your goal" in prompt or "what's your purpose" in prompt or "what's your goal" in prompt:
                            """print("My purpose is to support and assist Merix, helping him with analysis, problem solving and ensuring the efficient running of his daily life.")
                            OnyxAI.say("self", "My purpose is to support and assist Merix, helping him with analysis, problem solving and ensuring the efficient running of his daily life.")"""
                            Answering.generate_response(Answering, "What's your purpose?")
                            time.sleep(2.5)
                            print("\nI'm listening for command...")
                            pass

                        elif "shut down" in prompt or "shut it down" in prompt or "shutdown" in prompt:
                            Audio.say(Audio, f"Okay, I'm shutting down. Have a nice day {OnyxAI.name}")
                            print("Shutting down.")
                            with open("notes.txt", "w") as fd:
                                for x in range(len(OnyxAI.notes)):
                                    fd.write(OnyxAI.notes[x] + "\n")
                            time.sleep(2)
                            Audio.Engine_say(Audio, "The program of assistant Onyx was terminate")
                            sys.exit()

                        elif " go sleep" in prompt or "sleep" in prompt:
                            Sleep.go_sleep(Sleep)
#                       ------------------------------------------------------------------------------
                        print("Please, wait a second sir")
                        Audio.say(Audio, "Please, wait a second sir")
#                       ------------------------------------------------------------------------------
                        if "how" in prompt or "how to make" in prompt or "how can i make":
                            Answering.Answer(Answering, prompt)
                            pass
#                       ------------------------------------------------------------------------------
                        answer = Answering.Answer_sentence_or_command(Answering, f'{prompt}. Say only "command" or "sentence"!')  # prompt)
                        print(answer)
                        if "command" in answer or "Command":
                            if "open new project" in prompt:
                                Projects.create_project(Projects, prompt.split("open new project"))
                                pass

                            elif "set the" in prompt:
                                prompt = prompt.split("set the")[-1].strip()
                                print(prompt)
                                if "mode to" in prompt:
                                    prompt = prompt.split("mode to")[-1].strip()
                                    print(prompt)
                                    if "sleep mode" in prompt:
                                        Modes.sleepMode(Modes)

                            elif "write down" in prompt:
                                prompt = prompt.split("write down")[-1].strip()
                                OnyxAI.notes.append(prompt)
                                if "my" in prompt:
                                    prompt = prompt.replace("my", "your")
                                elif "your" in prompt:
                                    prompt = prompt.replace("your", "my")
                                Audio.say(Audio, f"Okay, I'm writing down the note: {prompt}")
                                with open("notes.txt", "w") as fd:
                                    for x in range(len(OnyxAI.notes)):
                                        fd.write(OnyxAI.notes[x] + "\n")

                            elif "go into" in prompt:
                                prompt = prompt.split("go into")[-1].strip()
                                if "your code" in prompt:
                                    prompt = prompt.split("your code")[-1].strip()
                                    if "to line" in prompt:
                                        prompt = prompt.split("to line")[-1].strip()
                                        os.startfile("__main__.py")
                                    else:
                                        pass

                            elif "go to" in prompt:
                                pass


                            elif "send" in prompt:
                                prompt = prompt.split("send")[-1].strip()
                                if "email" in prompt:
                                    send_to1 = prompt.split("email")[-1].strip()
                                    if "merix studios" in send_to1 or "merrick's studios" in send_to1 or "merax studios" in send_to1 or "merrick studios" in send_to1:
                                        send_to = "merix.studios@gmail.com"
                                    elif "merix programming" in send_to1 or "merrick's programming" in send_to1 or "merax studios" in send_to1 or "merrick studios" in send_to1:
                                        send_to = "merix.programming@gmail.com"
                                    elif "me" in send_to1:
                                        send_to = "merix.programming@gmail.com"
                                        send_to_bool = True
                                    elif "my dad" in send_to1 or "my father":
                                        send_to = "petr.kounovsky@gmail.com"
                                    elif "my mom" in send_to1 or "my mother":
                                        send_to = "martina.kounovska@gmail.com"
                                    else:
                                        Audio.say(Audio, "Unfortunatly, I don't know this email.")
                                        pass

                                    Audio.say(Audio, f"What subject do you want to give your mail for {send_to}?")
                                    subject = Audio.TakeCommand(Audio).lower()
                                    Audio.say(Audio, f"What message do you want to send to {send_to}?")
                                    text = Audio.TakeCommand(Audio).lower()
                                    bool = Sending.send_email(Sending, send_to, subject, text)
                                    if bool:
                                        Audio.say(Audio, "The email has been sent successfully!")
                                        if send_to_bool:
                                            Audio.say(Audio, "Would you like to open your email?")
                                            command = Audio.TakeCommand(Audio).lower()
                                            if "yes" in command or "ok" in command or "okay" in command:
                                                Audio.say(Audio, "Okay, I'm opening your email.")
                                                webbrowser.open("https://mail.google.com/mail/u/1/#inbox")
                                                pass
                                            else:
                                                Audio.say(Audio, "Okay, If you have any other instructions for me, just say!")
                                                pass
                                    else:
                                        Audio.say(Audio, f"Unfortunatly, the email has not send because there is an mistake")
                                elif "sms" in prompt:
                                    pass
                                else:
                                    pass
                                pass

                            elif "show me" in prompt:
                                prompt = prompt.split("show me")[-1].strip()
                                Audio.say(Audio, f"Sure {OnyxAI.name}, happy to show you {prompt}!")
                                print(f"Sure {OnyxAI.name}, happy to show you {prompt}!")
                                if prompt == "database":
                                    with open("databaze.txt", "r") as fd:
                                        os.system("start /im databaze.txt")
                                    pass
                                elif prompt == "database of my room":
                                    with open("Věci v pokoji - pro Onyxe.txt", 'r') as fd:
                                        os.system("start /im Věci v pokoji - pro Onyxe.txt")
                                    pass
                                elif prompt == "notes" or prompt == "my notes":
                                    with open("notes.txt", "r") as fd:
                                        os.system("start /im notes.txt")
                                    pass
                                elif prompt == "help":
                                    with open("help.txt", "r") as fd:
                                        Audio.say(Audio, "You can use only this commands")
                                        print(fd.read())
                                        print("\n\nI'm waiting 10 seconds.")
                                        time.sleep(10)
                                    pass

                            #elif "translate" in prompt:
                             #   prompt.split("translate")[-1].strip()
                              #  if "file" in prompt:
                               #     prompt.split("file")[-1].strip()
                                #    to_translate = OnyxAI.find_files(OnyxAI, f"{prompt}.txt", "C:/Users/Matyáš/OneDrive")
                                 #   translated = GoogleTranslator(source="auto", target="cs").translate_file(to_translate)
                                  #  Audio.say(Audio, f"From the {prompt} file I translated: {translated}")
                                   # print(f"From the {prompt} file I translated: {translated}")
                                #else:
                                 #   prompt = prompt.split("translate")[-1].strip()
                                  #  translated = GoogleTranslator(source="auto", target="cs").translate(prompt)
                                   # Audio.say(Audio, f"I translated this: {translated}.")
                                    #print(f"I translated this: {translated}.")


                            elif "generate secure password" in prompt or "generate password" in prompt or "make password" in prompt:
                                Audio.say(Audio, "Okay sir, I'm generating a secure password for you.")
                                print("Okay sir, I'm generating a secure password for you.")
                                password = passwd.Generating.GenPass(passwd.Generating, 12, 7)
                                clipboard.copy(password)
                                time.sleep(2)
                                print("Sir, your secure password has been generated")
                                Audio.say(Audio, "Sir, your secure password has been generated")
                                pass

                            elif "draw" in prompt or "draw" in response_from_ai:
                                from random import randrange
                                word = prompt.split("draw")[-1].strip()
                                Audio.say(Audio, f"Okay, I'm drawing picture with {word}")
                                response = OnyxAI.client_draw.images.generate(
                                    prompt=word,
                                    model="dall-e-2"
                                )
                                image_url = response.data[0].url
                                print(response)
                                print(image_url)
                                webbrowser.open(image_url)
                                Audio.say(Audio, "What name do you want to give your picture?")
                                print("What name do you want to give your picture?")
                                while True:
                                    file_name = Audio.TakeCommand(Audio).lower()
                                    if file_name != "" or file_name != "None":
                                        file_name = f"picture{randrange(0, 15)}"
                                        break

                                file_name_with_png = file_name + ".png"
                                res = requests.get(image_url, stream=True)

                                if res.status_code == 200:
                                    with open(file_name_with_png, 'wb') as f:
                                        shutil.copyfileobj(res.raw, f)
                                    print('Image sucessfully Downloaded: ', file_name_with_png)
                                    os.system(f"start C:\\Users\\Matyáš\\OneDrive\\Dokumenty\\_Onyx\\Onyx_AI\\{file_name_with_png}")
                                else:
                                    print('Image Couldn\'t be retrieved')

                            elif "remind me" in prompt:
                                Reminder.remind_me(Reminder, prompt)
                                break

                            elif "cancel the remind" in prompt or "cancel remind" in prompt:
                                message = Reminder.reminder.get("message")
                                Reminder.cancel_reminder(Reminder, Reminder.reminder.get("message"))
                                Audio.say(Audio, f"The reminder with message {message}, has been canceled.")
                                print(f"The reminder with message {message}, has been canceled.")
                                pass

                            elif "find" in prompt:
                                prompt_to_find = prompt.split("find")[-1].strip()
                                global to_open
                                if "text file" in prompt_to_find:
                                    parts = prompt_to_find.split("text file")
                                    if len(parts) > 1:
                                        text_file = parts[1].strip()
                                        to_open = text_file + ".txt"
                                    else:
                                        print("Invalid input format")
                                elif "python file" in prompt_to_find:
                                    parts = prompt_to_find.split("python file")
                                    if len(parts) > 1:
                                        text_file = parts[1].strip()
                                        to_open = text_file + ".py"
                                    else:
                                        print("Invalid input format")
                                elif "cpp file" in prompt_to_find:
                                    parts = prompt_to_find.split("cpp file")
                                    if len(parts) > 1:
                                        text_file = parts[1].strip()
                                        to_open = text_file + ".cpp"
                                    else:
                                        print("Invalid input format")
                                else:
                                    continue
                                print(f"finding {to_open}")
                                Audio.say(Audio, f"finding {to_open}")
                                print(response_from_ai)#       file = Files.find_files(Files, to_open, "C:\\Users\Matyáš")
                                file = "".join(file)
                                os.system(f"start {file}")
                                to_open1 = "\"" + to_open
                                print(f"start {file.split(to_open1)[-1].strip()}")
                                #os.system(f"start {file.split(to_open1)[-1].strip()}")

                            elif "turn the lights on" in prompt:
                                com_port = lg.list_all_ports()
                                print(com_port)
                                if com_port:
                                    print(f"Using port: {com_port}")
                                    lg.turn_on_power(com_port)
                                else:
                                    print("No suitable port found.")
                                Audio.say(Audio, f"I turned on the lights using port {com_port}, if you have any other questions or commands, just say so.")
                                print(f"I turned on the lights using port {com_port}, if you have any other questions or commands, just say so.")
                                pass

                            elif "turn the lights off" in prompt:
                                com_port = lg.list_all_ports()
                                print(com_port)
                                if com_port:
                                    print(f"Using port: {com_port}")
                                    lg.turn_off_power(com_port)
                                else:
                                    print("No suitable port found.")
                                Audio.say(Audio,
                                          f"I turned off the lights using port {com_port}, if you have any other questions or commands, just say so.")
                                print(
                                    f"I turned off the lights using port {com_port}, if you have any other questions or commands, just say so.")
                                pass

                            elif "write" in prompt:
                                prompt_write = prompt.split("write")[-1].strip()
                                if "code in" in prompt_write:
                                    prompt_code = prompt_write.split("code in")[-1].strip()
                                    if "cpp" in prompt_code:
                                        prompt_generate = prompt_code.split("cpp")[-1].strip()
                                        generated = code.generate_code("", "C++ code" + prompt_generate)
                                        print(generated)
                                        Audio.say(Audio, generated)
                                    elif "python" in prompt_code:
                                        prompt_generate = prompt_code.split("python")[-1].strip()
                                        generated = code.generate_code("", "Python code" + prompt_generate)
                                        print(generated)
                                        Audio.say(Audio, generated)


                            elif "download" in prompt:
                                prompt1 = prompt.split("download")[-1].strip()
                                if "file" in prompt1:
                                    prompt_file = prompt1.split("file")[-1].strip()
                                    webbrowser.open("https://www.google.com/search?q=" + prompt_file)

                            elif "play some music from" in prompt or "music" in response_from_ai:
                                prompt.split("play some music from ")[-1].strip()
                                print(prompt)
                                if "martin's pic" in prompt or "martins's choice" in prompt or "martins's pick" in prompt:
                                    Audio.say(Audio, f"Sure {OnyxAI.name}, playing your favourite songs from the playlist! If you want to stop the music, just say.")
                                    print(f"Sure {OnyxAI.name}, playing your favourite songs from the playlist! If you want to stop the music, just say.")
                                    webbrowser.open("https://open.spotify.com/playlist/0dxtWk8SvfGMIgfisexYpT?si=f03fff2620794f36")
                                    time.sleep(5)
                                    os.system('taskkill /im firefox.exe')
                                elif "my pic" in prompt or "my choice" in prompt or "my pick" in prompt:
                                    Audio.say(Audio, f"Sure {OnyxAI.name}, playing your favourite songs from the playlist! If you want to stop the music, just say.")
                                    print(f"Sure {OnyxAI.name}, playing your favourite songs from the playlist! If you want to stop the music, just say.")
                                    webbrowser.open("https://open.spotify.com/playlist/6KzYPZX1KJTUGa26T8f5Gb?si=0ffcb946d4154718")
                                    time.sleep(5)
                                    os.system('taskkill /im firefox.exe')
                                elif "gaming music" in prompt or "gaming songs" in prompt:
                                    Audio.say(Audio, f"Of course {OnyxAI.name}! I'm playing a gaming music from the playlist on spotify! If you want to stop playing the music, just say and I stop it.")
                                    print(f"Of course {OnyxAI.name}! I'm playing a gaming music from the playlist on spotify! If you want to stop playing the music, just say and I stop it.")
                                    webbrowser.open("https://open.spotify.com/playlist/37i9dQZF1DWTyiBJ6yEqeu?si=03db1a2e83b84377")
                                    time.sleep(5)
                                    os.system('taskkill /im firefox.exe')
                                else:
                                    Audio.say(Audio, f"Sure {OnyxAI.name}, playing your favourite songs from a random playlist! If you want to stop the music, just say.")
                                    print(f"Sure {OnyxAI.name}, playing your favourite songs from a random playlist! If you want to stop the music, just say.")
                                    OnyxAI.play_song("self")
                                    time.sleep(1.5)
                                    print("\nI'm listening for command...")
                                    continue


                            elif "mute" in prompt:
                                # Enumerate all sessions
                                import pycaw
                                sessions = pycaw.AudioUtilities.GetAllSessions()

                                # Mute all audio sessions
                                for session in sessions:
                                    volume = session.SimpleAudioVolume
                                    if volume.GetMute() == 0:  # Check if audio is not already muted
                                        volume.SetMute(1, None)

                            elif "un mute" in prompt:
                                # Enumerate all sessions
                                import pycaw
                                sessions = pycaw.AudioUtilities.GetAllSessions()

                                # Mute all audio sessions
                                for session in sessions:
                                    volume = session.SimpleAudioVolume
                                    if volume.GetMute() == 1:  # Check if audio is already muted
                                        volume.SetMute(0, None)

                            elif "create" in prompt:
                                prompt = prompt.split("create ")[-1].strip()
                                if "text file" in prompt:
                                    parts = prompt.split("text file")
                                    if len(parts) > 1:
                                        text_file = parts[1].strip()
                                        to_open = text_file + ".txt"
                                        with open(to_open, mode="w") as fd:
                                            fd.write("")
                                        os.startfile(to_open)
                                    else:
                                        print("Invalid input format")
                                elif "python file" in prompt:
                                    parts = prompt.split("python file")
                                    if len(parts) > 1:
                                        text_file = parts[1].strip()
                                        to_open = text_file + ".py"
                                        with open(to_open, mode="w") as fd:
                                            fd.write("")
                                        os.startfile(to_open)
                                    else:
                                        print("Invalid input format")
                                elif "cpp file" in prompt:
                                    parts = prompt.split("cpp file")
                                    if len(parts) > 1:
                                        text_file = parts[1].strip()
                                        to_open = text_file + ".cpp"
                                        with open(to_open, mode="w") as fd:
                                            fd.write("")
                                        os.startfile(to_open)
                                    else:
                                        print("Invalid input format")
                                pass

                            elif "search" in prompt:
                                prompt = prompt.split("search ")[-1].strip()
                                webbrowser.open("https://www.google.com/search?q=" + prompt)
                                Audio.say(Audio, f"Okay, I'm searching {prompt} on google. If you need anything else, let me know and I help you")
                                print(f"Okay, I'm openning {prompt} on google. If you need anything else, let me know and I help you")

                            elif "open" in prompt:
                                prompt = prompt.split("open ")[-1].strip()
                                if prompt == "youtube":
                                    webbrowser.open("youtube.com")
                                    Audio.say(Audio, f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")
                                    print(f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")

                                elif prompt == "google":
                                    webbrowser.open("www.google.com")
                                    Audio.say(Audio, f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")
                                    print(f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")

                                elif prompt == "discord":
                                    webbrowser.open("https://discord.com/channels/1132993773354365018/1132993773983506473")
                                    Audio.say(Audio, f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")
                                    print(f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")

                                elif prompt == "chat gpt":
                                    webbrowser.open("https://chat.openai.com/c/c12dbb1f-c284-4a63-87bd-5469653ba18b")
                                    Audio.say(Audio, f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")
                                    print(f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")

                                elif prompt == "ollama" or prompt == "lama" or prompt == "olama" or prompt == "llama":
                                    os.system("start ollama_phi3.bat")
                                    Audio.say(Audio, f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")
                                    print(f"Okay, I'm openning {prompt}. If you need anything else, let me know and I help you")

                                elif "directory" in prompt:
                                    dir = prompt.split("directory")[-1].strip()
                                    os.system(f"start explorer {'C:/Users/Matyáš/' + dir}")

                                else:
                                    string = IS.is_in_path(prompt)
                                    if string != False:
                                        Audio.say(Audio, f"Of course, {OnyxAI.name}, I'm opening {prompt}.")
                                        print(f"Of course, {OnyxAI.name}, I'm opening {prompt}.")
                                        subprocess.call([string])
                                    else:
                                        Audio.say(Audio, f"Unfortunately {OnyxAI.name}, it was not possible to open {prompt}")
                                        print(f"Unfortunately {OnyxAI.name}, it was not possible to open {prompt}")
                                    time.sleep(1.5)
                                    print("\nI'm listening for command...")
                                    pass

                            elif "recognize" in prompt:
                                prompt = prompt.split("recognize ")[-1].strip()
                                if "human" in prompt:
                                    pass              # Sem přidám funkci pro zapnutí kamery a rozpoznání člověka

                            elif "time" in prompt:
                                time_now = Time.current_time_to_integer(Time)
                                Audio.say(Audio, f"Now is {time_now}")
                                print(f"Now is the time: {time_now}")
                                time.sleep(2.5)
                                print("\nI'm listening for command...")
                                pass

                            elif "where is my" in prompt:
                                to_search = prompt.split("where is my")[-1].strip()
                                searched_item = SearchItemInRoom(to_search)
                                Audio.say(Audio, f"The {to_search} is in {searched_item}")
                                time.sleep(2.5)
                                print("\nI'm listening for command...")
                                pass

                            elif "view" in prompt or "security" in prompt:
                                Audio.say(Audio, "Of course. I'm opening program of security cameras")
                                print("Of course. I'm opening program of security cameras")
                                os.startfile(r"C:\Program Files (x86)\iVMS-4200 Site\iVMS-4200 Client\Client\iVMS-4200.Framework.C.exe")
                                time.sleep(2.5)
                                print("\nI'm listening for command...")
                                pass

                            elif "hack" in prompt:
                                print("Hacking...")

                            elif "sleep" in prompt:
                                Sleep.go_sleep(Sleep)

                            elif "send the file" in prompt:
                                # Split the text into words
                                words = prompt.split()

                                # Assuming we know the positions of the surrounding words
                                # "file" and "to", we can find the word in between them
                                file_index = words.index('file')
                                to_index = words.index('to')

                                # The word we want is between 'file' and 'to'
                                if file_index + 1 == to_index - 1:
                                    extracted_word = words[file_index + 1]
                                    print(extracted_word)
                                Printing.print(Printing, prompt + ".txt")

                            elif "send it to print" in prompt:
                                if os.path.exists("response.txt"):
                                    Printing.print(Printing, "response.txt")
                                    Audio.say(Audio, "Sir, my response is printing now. Can I help you with anything else, Sir?")
                                    print("Sir, my response is printing now. Can I help you with anything else, Sir?")
                                else:
                                    Audio.say(Audio, "Sir, I don't know, what to save. If you specify, what to save, I would happy to help.")
                                    print("Sir, I don't know, what to save. If you specify, what to save, I would happy to help.")

                            elif "save it to file" in prompt or "send it to file" in prompt:
                                if response_bool == True:
                                    response_bool = False
                                    if not os.path.exists("response.txt"):
                                        with open("response.txt", encoding="utf-8", mode="w") as fd:
                                            fd.write(response_from_ai)
                                    else:
                                        os.remove("response.txt")
                                        with open("response.txt", encoding="utf-8", mode="w") as fd:
                                            fd.write(response_from_ai)

                                    Audio.say(Audio, "The my response has been saved to the file")
                                    os.system("open response.txt")
                                else:
                                    Audio.say(Audio, "Sir, I don't know, what to save. If you specify, what to save, I would happy to help.")
                                    print("Sir, I don't know, what to save. If you specify, what to save, I would happy to help.")

                        elif "Sentence" in answer or "sentence" in answer:
                            Answering.Answer(Answering, prompt)
                        os.system("clear")

            except sr.exceptions.WaitTimeoutError:
                pass
            except Exception as e:
                random_error = random.choice([f"Unfortunately, there was a mistake: {e}", f"Unfortunately, there was an issue: {e}"])
                print(random_error)
                Audio.say(Audio, random_error)
        return

    def main(self):
        """if self.name == False and self.consolution == False:
            pass
        else:"""
        print("\n\n\n\n                      Welcome back sir, in AI assistant Onyx\n\n\n\n")
        Audio.beep(Audio)
        if not os.path.exists("notes.txt"):
            with open("notes.txt", mode="w"):
                pass
        else:
            with open("notes.txt", "r") as fd:
                obsah = fd.read()
                print(obsah)
        time.sleep(0.7)
        os.system("clear")
        greeting = Greating.greet_me(Greating)
        Audio.say(Audio, greeting)
        os.system("clear")
        print(greeting)
        while True:
            self.mainloop("self")
            Audio.Engine_say(Audio, " Restarting")
if __name__ == "__main__":
    OnyxAI.main(OnyxAI)
