import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
import urllib.request

SUNSET_API = "https://api.sunrise-sunset.org/json"
LAT = "52.377956"
LNG = "4.897070"


def get_times(lat, lng):
    """
    Fetch Twilight Begin, Sunrise, Sunset, Twilight End times.
    """
    timings = ["civil_twilight_begin", "sunrise", "sunset", "civil_twilight_end"]
    url = "{}?lat={}&lng={}".format(SUNSET_API, lat, lng)
    with urllib.request.urlopen(url) as f:
        json_response = json.load(f)

        for key in timings:
            yield datetime.strptime(json_response["results"][key], "%I:%M:%S %p").time()


def main(current_time, lat, lng):
    """Set Wallpaper for given time at given location."""
    twilight, sunrise, sunset, day_end = get_times(lat, lng)

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
    parser = argparse.ArgumentParser(description="Dynamically set wallpaper.")
    parser.add_argument("time", nargs="?", help="Custom time")
    parser.add_argument("--lat", nargs="?", help="Latitude", default=LAT)
    parser.add_argument("--lng", nargs="?", help="Longitude", default=LNG)
    parser.add_argument("--print-timing",
                        help="Print timing and quit.",
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    if args.time is None:
        current_time = datetime.now().time()
    else:
        try:
            current_time = datetime.strptime(args.time, "%H:%M").time()
        except ValueError as e:
            print("Incorrect time provided: {}".format(e))
            exit(1)

    if args.print_timing:
        twilight, sunrise, sunset, down = list(get_times(args.lat, args.lng))
        print("Twilight: {}".format(twilight))
        print("Sunrise: {}".format(sunrise))
        print("Sunset: {}".format(sunset))
        print("Down: {}".format(down))
    else:
        main(current_time, lat=args.lat, lng=args.lng)
