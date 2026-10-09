import os
import sys
import random
import tkinter as tk

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dartboard import Dartboard
from utils.themes import THEME
from utils.config import PROJECT_NAME

class DartVaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(PROJECT_NAME)
        self.root.geometry("540x700")
        self.root.minsize(480, 650)
        self.root.configure(bg=THEME["bg"])
        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text=PROJECT_NAME,
            font=("Arial", 25, "bold"),
            bg=THEME["bg"],
            fg=THEME["text"],
        )
        title.pack(pady=(24, 4))
        subtitle = tk.Label(
            self.root,
            text="Review Sentiment Analyzer",
            font=("Arial", 11),
            bg=THEME["bg"],
            fg=THEME["muted"],
        )
        subtitle.pack(pady=(0, 12))
        self.dartboard = Dartboard(
            self.root,
            size=400,
            bg=THEME["bg"],
        )
        self.dartboard.pack(pady=(0, 0))
        score_heading = tk.Label(
            self.root,
            text="SENTIMENT SCORE",
            font=("Arial", 10, "bold"),
            bg=THEME["bg"],
            fg=THEME["muted"],
        )
        score_heading.pack(pady=(0, 2))
        self.score_label = tk.Label(
            self.root,
            text="+87%",
            font=("Arial", 30, "bold"),
            bg=THEME["bg"],
            fg=THEME["positive"],
        )
        self.score_label.pack(pady=(0, 14))
        self.roll_button = tk.Button(
            self.root,
            text="Roll Review",
            font=("Arial", 13, "bold"),
            bg=THEME["accent"],
            fg=THEME["button_text"],
            activebackground=THEME["accent_hover"],
            activeforeground=THEME["button_text"],
            relief="flat",
            cursor="hand2",
            width=18,
            pady=10,
            command=self.roll_review,
        )
        self.roll_button.pack(pady=(0, 22))

    def roll_review(self):
        score = random.uniform(-1.0, 1.0)
        percentage = round(score * 100)
        if score >= 0.05:
            color = THEME["positive"]
            sign = "+"
        elif score <= -0.05:
            color = THEME["negative"]
            sign = ""
        else:
            color = THEME["muted"]
            sign = "+" if percentage >= 0 else ""
        self.score_label.configure(
            text=f"{sign}{percentage}%",
            fg=color,
        )

def main():
    root = tk.Tk()
    DartVaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()