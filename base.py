import torch
import cv2 as cv
import numpy as np
import tkinter as tk
from mss import mss
from time import time

w = 3840
h = 2160
sct = mss()
monitor = sct.monitors[1]
base = np.array([w, h, w, h])

root = tk.Toplevel()
root.geometry("3840x2160")
root.attributes("-transparentcolor", "white")
root.attributes("-topmost", True)
root.overrideredirect(True)
root.config(bg="white")
canvas = tk.Canvas(root, bg="white", height=h, width=w)
canvas.pack()

model_path = "modelo_yolo/best.engine"
model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path)
model.cuda()
model.multi_label = False


class Object:

    def __init__(self, cord, label):
        self.coords = cord[:-1] * base
        self.width, self.height = cord[2] - cord[0], cord[3] - cord[1]
        self.confidence = cord[4]
        self.label = label

    def update(self, coords, confidence):
        self.coords = coords[:-1]
        self.coords[2], self.coords[3] = self.coords[0] + self.width, self.coords[1] + self.height
        self.confidence = confidence

    def draw(self, canvas):

        canvas.create_rectangle(self.coords[0], self.coords[1], self.coords[2], self.coords[3], outline="red")
        canvas.create_text(self.coords[2] + 5,
                           self.coords[3] + 15,
                           text=classes[int(self.label)],
                           fill="red",
                           font=("Arial", 12))
        canvas.create_text(self.coords[2] - 5,
                           self.coords[3] - 5,
                           text=str(round(self.confidence, 2)),
                           fill="red",
                           font=("Arial", 12))


def is_duplicate(old_list, coords, label):
    coords = coords * base
    for item in old_list:
        if np.linalg.norm(coords - item.coords) < 40 and label == item.label or classes[int(
                label)] == "player" and np.linalg.norm(coords - item.coords) < 100:
            return True
    return False


def remove_duplicates(old_list):
    for item in old_list:
        if is_duplicate(old_list, item.coords, item.label):
            old_list.remove(item)


classes = [
    "rogue", "warrior", "wizard", "champ_indicator", "mining_indicator", "plant_indicator", "rune_indicator",
    "silk_indicator", "wood_indicator", "blessed_thistle", "champstool", "chest", "columbine", "iron_ore",
    "ladys_smock", "maple", "pewter_seam", "platinum_seam", "rudedite_ore", "ruby_ash_wood", "runestone", "wormwood",
    "dragonthorn", "luminous_russula", "corn_flower", "nightshade", "jute", "ancestor_silk", "blue_entoloma",
    "emetic_russula", "bugloss", "player", "mountain_flower", "white_cap", "violet_coprinus", "namiras_rot", "stinkhorn"
]


def main_loop():
    item_list = []
    old_list = []
    time_start = time()

    while True:
        screenshot = cv.cvtColor(np.array(sct.grab(monitor)), cv.COLOR_BGR2RGB)

        results = model(screenshot)
        labels, cord = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()

        old_list = item_list
        item_list = []

        for i in range(len(labels)):
            if cord[i][4] > 0.3:
                found = False
                for item in old_list:
                    if is_duplicate(cord[i][:-1], labels[i]):
                        item.update(cord[i], cord[i][4])
                        item_list.append(item)
                        found = True
                        break
                if not found and cord[i][4] > 0.5:
                    item_list.append(Object(cord[i], labels[i]))

        remove_duplicates(item_list)
        if len(item_list) == 0:
            continue
        for item in item_list:
            item.draw(canvas)

        # refresh the canvas
        canvas.update()
        canvas.delete("all")

        print(f"FPS: {1 / (time() - time_start)}")
        time_start = time()
