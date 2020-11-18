from time import sleep
import pyautogui
import json
import pprint

interval = 0.08


def combinations(comb=tuple(), main="enter", times=1):
    for key in comb:
        pyautogui.keyDown(key)
    for _ in range(times):
        pyautogui.press(main)
    for key in comb:
        pyautogui.keyUp(key)


def connect_fields(text):
    # creating new field for later
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("up")
    # marking
    combinations(("shift",), "right", 2)
    # menu selection
    # 1. open format menu
    combinations(("alt", "shift"), "o")
    # 2. connect
    pyautogui.press('2')
    pyautogui.press('m')
    # centered
    combinations(("ctrl", "shift"), "e")
    # write text
    pyautogui.write(text, interval=interval)
    # go to new field
    pyautogui.press("down")


def write_two(a, b):
    pyautogui.write(a, interval=interval)
    pyautogui.press("tab")
    pyautogui.write(b, interval=interval)
    pyautogui.press("tab")


def rewrap_movies(movies):
    movie_dict = {}
    for movie in movies:
        if movies[movie] is not None:
            services = {}
            for country in movies[movie]:
                for service in movies[movie][country]:
                    if service not in services:
                        services[service] = []
                    services[service].append(country)
            movie_dict[movie] = services
        else:
            movie_dict[movie] = None
    return movie_dict


with open("movies.json", "r", encoding="utf-8") as file:
    _movies = json.load(file)

sleep(7)

_rewrap = rewrap_movies(_movies)
for _movie in _rewrap:
    if _rewrap[_movie] is None:
        connect_fields(_movie)
    else:
        write_two(_movie,
                  ", ".join([" ".join((i, "(" + (", ".join(_rewrap[_movie][i])) + ")")) for i in _rewrap[_movie]]))
