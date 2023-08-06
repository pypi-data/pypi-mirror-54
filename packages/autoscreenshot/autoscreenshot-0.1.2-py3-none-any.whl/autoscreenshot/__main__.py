import base64
import os
from datetime import datetime
import pyscreenshot as ImageGrab
import requests
import subprocess
import pyperclip
from subprocess import SubprocessError

os.getcwd()
url = "https://api.imgur.com/3/upload"
filename = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
t = filename + ".png"

if __name__ == "__main__":
    proc = subprocess.Popen(
        ["slop", "-f", "%x %y %w %h"], stdout=subprocess.PIPE
    )
    try:
        outs, errs = proc.communicate()
    except SubprocessError:
        proc.kill()
    rect = outs.decode().split(" ")
    rect = [int(x) for x in rect]
    if rect:
        im = ImageGrab.grab(
            bbox=(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
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
