import json
import os
import subprocess
import sys
from datetime import datetime
import urllib.request

SUNSET_API = "https://api.sunrise-sunset.org/json"
LAT = "52.377956"
LON = "4.897070"


def get_times():
    timings = ["civil_twilight_begin", "sunrise", "sunset", "civil_twilight_end"]
    url = "{}?lat={}&lng={}".format(SUNSET_API, LAT, LON)
    with urllib.request.urlopen(url) as f:
        json_response = json.load(f)

        for key in timings:
            yield datetime.strptime(json_response["results"][key], "%I:%M:%S %p").time()



def main(current_time):
    twilight, sunrise, sunset, day_end = get_times()

    if current_time >= twilight and current_time <= sunrise:
        image = 1
    elif current_time > sunrise and current_time < sunset:
        image = 2
    elif current_time >= sunset and current_time <= day_end:
        image = 3
    else:
        image = 4

    path = os.path.join(os.path.dirname(__file__), "images")
    command = "feh --bg-fill {}/{}.jpg".format(path, image)
    try:
        subprocess.check_output(command,
                                stderr=subprocess.STDOUT,
                                shell=True)
    except subprocess.CalledProcessError as e:
        print("Failed to set wallpaper: {}".format(e))


if __name__ == "__main__":
    current_time = datetime.now().time()
    if len(sys.argv) == 2:
        try:
            current_time = datetime.strptime(sys.argv[1], "%H:%M").time()
        except ValueError as e:
            print("Incorrect time provided: {}".format(e))
            exit(1)

    main(current_time)
