import os
import sys
import tkinter as tk

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dartboard import Dartboard
from review import ReviewDisplayMixin
from controls import ControlsMixin
from utils.themes import THEME, FONTS
from utils.config import PROJECT_NAME

class DartVaderApp(ReviewDisplayMixin, ControlsMixin):
    def __init__(self, root):
        self.root = root
        self.root.title(PROJECT_NAME)
        self.root.state("zoomed")
        self.root.configure(bg=THEME["bg"])

        self.mood_photo = None
        self.current_review = None
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.root, bg=THEME["bg"])
        header.pack(fill="x", padx=28, pady=(20, 12))

        tk.Label(
            header,
            text=PROJECT_NAME,
            font=FONTS["title"],
            bg=THEME["bg"],
            fg=THEME["text"],
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Review Sentiment Analyzer",
            font=FONTS["heading"],
            bg=THEME["bg"],
            fg=THEME["muted"],
        ).pack(anchor="w", pady=(2, 0))

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
        right_panel.grid_columnconfigure(0, weight=3)
        right_panel.grid_columnconfigure(1, weight=2)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=0)

        review_section = tk.Frame(right_panel, bg=THEME["panel"])
        review_section.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(20, 10),
            pady=18,
        )

        tk.Label(
            review_section,
            text="RANDOM REVIEW",
            font=FONTS["heading"],
            bg=THEME["panel"],
            fg=THEME["muted"],
        ).pack(anchor="w")

        self.review_label = tk.Label(
            review_section,
            text="Click Roll a Review to begin.",
            font=FONTS["body"],
            bg=THEME["panel"],
            fg=THEME["text"],
            justify="left",
            anchor="nw",
            wraplength=400,
        )
        self.review_label.pack(
            fill="x", anchor="w", pady=(8, 20)
        )

        tk.Label(
            review_section,
            text="SENTIMENT",
            font=FONTS["heading"],
            bg=THEME["panel"],
            fg=THEME["muted"],
        ).pack(anchor="w")

        self.sentiment_label = tk.Label(
            review_section,
            text="—",
            font=FONTS["sentiment"],
            bg=THEME["panel"],
            fg=THEME["text"],
        )
        self.sentiment_label.pack(anchor="w", pady=(2, 14))

        tk.Label(
            review_section,
            text="SENTIMENT SCORE",
            font=FONTS["heading"],
            bg=THEME["panel"],
            fg=THEME["muted"],
        ).pack(anchor="w")

        self.score_label = tk.Label(
            review_section,
            text="—",
            font=FONTS["score"],
            bg=THEME["panel"],
            fg=THEME["text"],
        )
        self.score_label.pack(anchor="w", pady=(2, 18))

        self.review_count_label = tk.Label(
            review_section,
            text="Reviews available: —",
            font=FONTS["body"],
            bg=THEME["panel"],
            fg=THEME["muted"],
        )
        self.review_count_label.pack(anchor="w", pady=(0, 10))

        mood_section = tk.Frame(right_panel, bg=THEME["panel"])
        mood_section.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 20),
            pady=18,
        )

        tk.Label(
            mood_section,
            text="REVIEW'S MOOD",
            font=FONTS["heading"],
            bg=THEME["panel"],
            fg=THEME["muted"],
        ).pack(pady=(12, 8))

        self.mood_image_label = tk.Label(
            mood_section,
            bg=THEME["panel"],
            width=160,
            height=160,
        )
        self.mood_image_label.pack()

        self.mood_text_label = tk.Label(
            mood_section,
            text="Waiting for a review...",
            font=FONTS["body"],
            bg=THEME["panel"],
            fg=THEME["text"],
            wraplength=180,
        )
        self.mood_text_label.pack(pady=(8, 0))

        controls_section = tk.Frame(
            right_panel,
            bg=THEME["panel"],
        )
        controls_section.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(0, 18),
        )
        controls_section.grid_columnconfigure(0, weight=1)
        controls_section.grid_columnconfigure(1, weight=1)
        self.build_controls(controls_section)

        self.reviews = self.load_reviews()
        self.review_count_label.configure(
            text=f"Reviews available: {len(self.reviews)}"
        )

        if self.reviews:
            self.roll_review()

    def clear_custom_placeholder(self, event=None):
        if self.custom_review_entry.get() == "Type a custom review...":
            self.custom_review_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    DartVaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()