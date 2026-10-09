
import os
import sys
import random
import csv
import tkinter as tk
from tkinter import messagebox

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dartboard import Dartboard
from utils.themes import THEME, FONTS
from utils.config import PROJECT_NAME, ANALYZED_DATA_FILE

class DartVaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(PROJECT_NAME)
        self.root.geometry("1100x700")
        self.root.minsize(900, 620)
        self.root.configure(bg=THEME["bg"])
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.root, bg=THEME["bg"])
        header.pack(fill="x", padx=28, pady=(20, 12))
        tk.Label(header, text=PROJECT_NAME, font=FONTS["title"], bg=THEME["bg"], fg=THEME["text"],).pack(anchor="w")
        tk.Label(header, text="Review Sentiment Analyzer", font=FONTS["heading"], bg=THEME["bg"], fg=THEME["muted"],).pack(anchor="w", pady=(2, 0))
        content = tk.Frame(self.root, bg=THEME["bg"])
        content.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)
        board_panel = tk.Frame(
            content,
            bg=THEME["panel"],
            highlightbackground=THEME["border"],
            highlightthickness=1,
        )
        board_panel.grid(
            row=0, column=0, sticky="nsew", padx=(0, 10)
        )
        tk.Label(
            board_panel,
            text="SENTIMENT DARTBOARD",
            font=FONTS["heading"],
            bg=THEME["panel"],
            fg=THEME["muted"],
        ).pack(pady=(18, 4))
        self.dartboard = Dartboard(
            board_panel,
            size=400,
            bg=THEME["panel"],
        )
        self.dartboard.pack(expand=True)
        right_panel = tk.Frame(
            content,
            bg=THEME["panel"],
            highlightbackground=THEME["border"],
            highlightthickness=1,
        )
        right_panel.grid(
            row=0, column=1, sticky="nsew", padx=(10, 0)
        )
        tk.Label(
            right_panel,
            text="RANDOM REVIEW",
            font=FONTS["heading"],
            bg=THEME["panel"],
            fg=THEME["muted"],
        ).pack(anchor="w", padx=20, pady=(18, 8))
        self.review_label = tk.Label(
            right_panel,
            text="Click Roll a Review to begin.",
            font=FONTS["body"],
            bg=THEME["panel"],
            fg=THEME["text"],
            justify="left",
            anchor="nw",
            wraplength=400,
        )
        self.review_label.pack(
            fill="x", padx=20, pady=(0, 16)
        )
        self.roll_button = tk.Button(
            right_panel,
            text="Roll a Review",
            font=FONTS["button"],
            bg=THEME["accent"],
            fg=THEME["button_text"],
            activebackground=THEME["accent_hover"],
            activeforeground=THEME["button_text"],
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self.roll_review,
        )
        self.roll_button.pack(fill="x", padx=20, pady=(0, 24))
        tk.Label(
            right_panel,
            text="SENTIMENT",
            font=FONTS["heading"],
            bg=THEME["panel"],
            fg=THEME["muted"],
        ).pack(anchor="w", padx=20)
        self.sentiment_label = tk.Label(
            right_panel,
            text="—",
            font=FONTS["sentiment"],
            bg=THEME["panel"],
            fg=THEME["text"],
        )
        self.sentiment_label.pack(anchor="w", padx=20, pady=(2, 14))
        tk.Label(
            right_panel,
            text="SENTIMENT SCORE",
            font=FONTS["heading"],
            bg=THEME["panel"],
            fg=THEME["muted"],
        ).pack(anchor="w", padx=20)
        self.score_label = tk.Label(
            right_panel,
            text="—",
            font=FONTS["score"],
            bg=THEME["panel"],
            fg=THEME["text"],
        )
        self.score_label.pack(anchor="w", padx=20, pady=(0, 18))
        self.review_count_label = tk.Label(right_panel, text="Reviews available: —", font=FONTS["body"], bg=THEME["panel"], fg=THEME["muted"])
        self.review_count_label.pack(anchor="w", padx=20, pady=(0, 18))
        self.reviews = self.load_reviews()
        self.review_count_label.configure(text=f"Reviews available: {len(self.reviews)}")

    def load_reviews(self):
        if not os.path.exists(ANALYZED_DATA_FILE):
            messagebox.showerror(
                "Reviews Not Found",
                f"Could not find the analyzed reviews file:\n"
                f"{ANALYZED_DATA_FILE}\n\n"
                "Run your analysis script first.",
            )
            return []
        with open(
            ANALYZED_DATA_FILE,
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)
            return [
                row for row in reader
                if row.get("review_text", "").strip()
            ]
    def roll_review(self):
        if not self.reviews:
            messagebox.showwarning(
                "No Reviews",
                "No reviews are available. Check the analyzed CSV file.",
            )
            return
        review = random.choice(self.reviews)
        review_text = review.get("review_text", "").strip()
        sentiment = review.get("sentiment", "neutral").strip().lower()
        try:
            score = float(review.get("sentiment_score", 0))
        except (TypeError, ValueError):
            score = 0.0
        percentage = round(score * 100)
        if sentiment == "positive":
            color = THEME["positive"]
            sign = "+" if percentage >= 0 else ""
        elif sentiment == "negative":
            color = THEME["negative"]
            sign = "+" if percentage > 0 else ""
        else:
            color = THEME.get("neutral", THEME["muted"])
            sign = "+" if percentage > 0 else ""
        self.review_label.configure(text=review_text)
        self.sentiment_label.configure(
            text=sentiment.capitalize(),
            fg=color,
        )
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