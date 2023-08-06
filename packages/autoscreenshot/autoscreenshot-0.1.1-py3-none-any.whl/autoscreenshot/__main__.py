import base64
import os
from datetime import datetime
import pyscreenshot as ImageGrab
import requests
import slop
import pyperclip

os.getcwd()
url = "https://api.imgur.com/3/upload"
filename = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
t = filename + ".png"
if __name__ == "__main__":
    rect = slop.select(border=3, r=1, g=0, b=0, a=0.5)
    if rect["cancelled"] == 0:
        im = ImageGrab.grab(
            bbox=(
                rect["x"],
                rect["y"],
                rect["x"] + rect["w"],
                rect["y"] + rect["h"],
            )
        )
        im.save(t)
        with open(t, "rb") as shot:
            base64img = base64.b64encode(shot.read())
            r = requests.post(
                url,
                headers={"Authorization": ("Client-ID 372b559e92be165")},
                data={"image": base64img},
            )
            if r.json()["data"]["link"]:
                pyperclip.copy(r.json()["data"]["link"])
        os.remove(t)
