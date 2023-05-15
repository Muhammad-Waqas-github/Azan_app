import requests
import time
import os
from datetime import datetime, date
from playsound import playsound

# import pygame
from azan import find_adhan_times_manually
from flask import Flask, jsonify
from main import update_times, get_data
from dotenv import load_dotenv

load_dotenv()

prayers = {
    "dhuhr": "",
    "asr": "",
    "maghrib": "",
    "isha": "",
    "fajr": "",
}


def update_api_call():
    response = ""
    tried = 0
    global prayers
    while response != [200]:
        try:
            api_key = os.getenv("API_KEY")
            if api_key:
                response = requests.get(
                    f"https://muslimsalat.com/london/daily/3.json?key={api_key}"
                )

            api_data = response.json()

            for key in prayers.keys():
                prayers[key] = api_data["items"][0][key]
            return prayers
        except:
            tried += 1
            # time.sleep(30)
            if tried >= 5:
                prayers = find_adhan_times_manually()
                tried = 0
                return prayers


def time_difference_in_seconds(time1, time2):
    """Calculates the time difference between two time objects in seconds."""
    datetime1 = datetime.combine(date.today(), time1)
    datetime2 = datetime.combine(
        date.today(), datetime.strptime(time2, "%I:%M %p").time()
    )
    timedelta = datetime2 - datetime1
    return timedelta.seconds


def find_next_prayer_and_time(time_now, prayers):
    # Find out if it is time for a prayer otherwise find the next prayer time

    next_prayer = None
    time_now = datetime.strptime(time_now, "%I:%M %p").time()
    for prayer, time in prayers.items():
        time = datetime.strptime(time, "%I:%M %p").time()
        print(prayer, time)
        print(time == time_now, time > time_now)
        if time == time_now:
            now_prayer = prayer
            print(f"It's time for {now_prayer} prayer.")
            return True, now_prayer, 0

        else:  # time > time_now:
            next_prayer = prayer
            to_sleep = time_difference_in_seconds(time_now, prayers[next_prayer])
            print(f"There is no prayer now. The next prayer is {next_prayer}.")
            print(
                f"and the time for {next_prayer} is {prayers[next_prayer]} which is in {time_difference_in_seconds(time_now, prayers[next_prayer])} seconds from now"
            )

            return False, next_prayer, to_sleep


# @app.route("/api")
def start():
    while True:
        now = datetime.now().strftime("%I:%M %p")
        first, first_first = True, True
        if first_first:
            first_first = False
            prayers = update_api_call()
            update_times(prayers)

            record_retrieved = get_data()
            record = {}
            for item in record_retrieved:
                prayer_record = item[0]
                status1 = item[2]
                status2 = item[3]
                record[prayer_record] = {"Azan": status1, "Dua": status2}

        if first or prayer_time == "fajr":
            first = False
            prayers = update_api_call()
            prayer_now, prayer_time, to_sleep = find_next_prayer_and_time(now, prayers)
            update_times(prayers)
        if prayer_now and record[prayer_time.capitalize()]["Azan"] == "on":
            # for raspberry pi/debian
            # pygame.mixer.init()
            # pygame.mixer.music.load("azan8.mp3")
            # pygame.mixer.music.play()

            playsound("azan8.mp3")
            print("Azan played")
        time.sleep(to_sleep)


start()
