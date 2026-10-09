
import os
import sys
import random
import csv
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(SRC_DIR)
MOOD_IMAGE_DIR = os.path.join(PROJECT_DIR, "resources", "images", "mood")
MOOD_IMAGE_SIZE = (160, 160)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dartboard import Dartboard
from utils.themes import THEME, FONTS
from utils.config import PROJECT_NAME, ANALYZED_DATA_FILE


class DartVaderApp:
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

        button_style = {
            "font": FONTS["button"],
            "bg": THEME["accent"],
            "fg": THEME["button_text"],
            "activebackground": THEME["accent_hover"],
            "activeforeground": THEME["button_text"],
            "relief": "flat",
            "cursor": "hand2",
            "pady": 9,
        }

        self.roll_button = tk.Button(
            controls_section,
            text="Roll a Review",
            command=self.roll_review,
            **button_style,
        )
        self.roll_button.grid(
            row=0, column=0, sticky="ew", padx=(0, 5), pady=5
        )

        self.start_analysis_button = tk.Button(
            controls_section,
            text="Start Analysis",
            command=self.start_analysis,
            **button_style,
        )
        self.start_analysis_button.grid(
            row=0, column=1, sticky="ew", padx=(5, 0), pady=5
        )

        self.custom_review_entry = tk.Entry(
            controls_section,
            font=FONTS["body"],
            bg=THEME["bg"],
            fg=THEME["text"],
            insertbackground=THEME["text"],
            relief="flat",
        )
        self.custom_review_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 5),
            pady=5,
            ipady=9,
        )
        self.custom_review_entry.insert(0, "Type a custom review...")
        self.custom_review_entry.bind(
            "<FocusIn>", self.clear_custom_placeholder
        )
        self.custom_review_entry.bind(
            "<Return>", lambda event: self.analyze_custom_review()
        )

        self.run_custom_button = tk.Button(
            controls_section,
            text="Run",
            command=self.analyze_custom_review,
            **button_style,
        )
        self.run_custom_button.grid(
            row=1, column=1, sticky="ew", padx=(5, 0), pady=5
        )

        self.force_positive_button = tk.Button(
            controls_section,
            text="Force Positive",
            command=lambda: self.force_sentiment("positive"),
            **button_style,
        )
        self.force_positive_button.grid(
            row=2, column=0, sticky="ew", padx=(0, 5), pady=5
        )

        self.force_negative_button = tk.Button(
            controls_section,
            text="Force Negative",
            command=lambda: self.force_sentiment("negative"),
            **button_style,
        )
        self.force_negative_button.grid(
            row=2, column=1, sticky="ew", padx=(5, 0), pady=5
        )

        self.reviews = self.load_reviews()
        self.review_count_label.configure(
            text=f"Reviews available: {len(self.reviews)}"
        )

    def clear_custom_placeholder(self, event=None):
        if self.custom_review_entry.get() == "Type a custom review...":
            self.custom_review_entry.delete(0, tk.END)

    def show_mood(self, image_name, mood_text):
        image_path = os.path.join(MOOD_IMAGE_DIR, image_name)

        if not os.path.exists(image_path):
            self.mood_text_label.configure(
                text=f"{mood_text}\n(Image not found)"
            )
            self.mood_image_label.configure(image="")
            self.mood_photo = None
            return

        try:
            with Image.open(image_path) as image:
                image = image.convert("RGB")
                image.thumbnail(
                    MOOD_IMAGE_SIZE,
                    Image.Resampling.LANCZOS,
                )

                canvas = Image.new(
                    "RGB",
                    MOOD_IMAGE_SIZE,
                    THEME["panel"],
                )
                x = (MOOD_IMAGE_SIZE[0] - image.width) // 2
                y = (MOOD_IMAGE_SIZE[1] - image.height) // 2
                canvas.paste(image, (x, y))

            self.mood_photo = ImageTk.PhotoImage(canvas)
            self.mood_image_label.configure(image=self.mood_photo)
            self.mood_text_label.configure(text=mood_text)

        except (OSError, ValueError) as error:
            self.mood_image_label.configure(image="")
            self.mood_photo = None
            self.mood_text_label.configure(
                text=f"{mood_text}\n(Could not load image)"
            )
            print(f"Could not load mood image '{image_path}': {error}")

    def load_reviews(self):
        if not os.path.exists(ANALYZED_DATA_FILE):
            messagebox.showerror(
                "Reviews Not Found",
                f"Could not find the analyzed reviews file:\n"
                f"{ANALYZED_DATA_FILE}\n\n"
                "Run your analysis script first.",
            )
            return []

        try:
            with open(
                ANALYZED_DATA_FILE,
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as file:
                reader = csv.DictReader(file)
                return [
                    row
                    for row in reader
                    if row.get("review_text", "").strip()
                ]
        except (OSError, csv.Error) as error:
            messagebox.showerror(
                "Could Not Read Reviews",
                f"An error occurred while reading the CSV:\n{error}",
            )
            return []

    def display_review(self, review_text, sentiment, score):
        sentiment = sentiment.lower()
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

        if score >= 0.70:
            self.show_mood("70+.jpg", "Very Happy")
        elif score >= 0.60:
            self.show_mood("60-70.jpg", "Happy")
        elif score >= 0.50:
            self.show_mood("50-60.jpg", "Happy")
        elif score >= 0.40:
            self.show_mood("40-50.jpg", "Pleased")
        elif score >= 0.30:
            self.show_mood("30-40.jpg", "Pleased")
        elif score >= 0.20:
            self.show_mood("20-30.jpg", "Slightly Positive")
        elif score >= 0.10:
            self.show_mood("10-20.jpg", "Slightly Positive")
        elif score >= 0:
            self.show_mood("0-10.jpg", "Neutral")
        elif score > -0.10:
            self.show_mood("-0-10.jpg", "Slightly Negative")
        elif score > -0.20:
            self.show_mood("-10-20.jpg", "Slightly Negative")
        elif score > -0.30:
            self.show_mood("-20-30.jpg", "Upset")
        elif score > -0.40:
            self.show_mood("-30-40.jpg", "Upset")
        elif score > -0.50:
            self.show_mood("-40-50.jpg", "Angry")
        elif score > -0.60:
            self.show_mood("-50-60.jpg", "Angry")
        elif score > -0.70:
            self.show_mood("-60-70.jpg", "Very Angry")
        else:
            self.show_mood("-70+.jpg", "Furious")

    def roll_review(self):
        if not self.reviews:
            messagebox.showwarning(
                "No Reviews",
                "No reviews are available. Check the analyzed CSV file.",
            )
            return

        review = random.choice(self.reviews)
        self.current_review = review

        review_text = review.get("review_text", "").strip()
        sentiment = review.get("sentiment", "neutral").strip().lower()

        try:
            score = float(review.get("sentiment_score", 0))
        except (TypeError, ValueError):
            score = 0.0

        self.display_review(review_text, sentiment, score)

    def start_analysis(self):
        messagebox.showinfo(
            "Start Analysis",
            "This button is ready for your analysis script to be connected. "
            "It currently reloads the analyzed reviews.",
        )
        self.reviews = self.load_reviews()
        self.review_count_label.configure(
            text=f"Reviews available: {len(self.reviews)}"
        )

    def analyze_custom_review(self):
        review_text = self.custom_review_entry.get().strip()

        if not review_text or review_text == "Type a custom review...":
            messagebox.showwarning(
                "Empty Review",
                "Please type a review first.",
            )
            return

        messagebox.showinfo(
            "Analysis Not Connected",
            "The custom review field is ready, but the sentiment-analysis "
            "function still needs to be connected to your analyzer.",
        )

    def force_sentiment(self, sentiment):
        if self.current_review is None:
            messagebox.showwarning(
                "No Review Selected",
                "Roll a review first before forcing its sentiment.",
            )
            return
        try:
            score = float(self.current_review.get("sentiment_score", 0))
        except (TypeError, ValueError):
            score = 0.0
        color = (
            THEME["positive"]
            if sentiment == "positive"
            else THEME["negative"]
        )
        self.sentiment_label.configure(
            text=sentiment.capitalize(),
            fg=color,
        )

def main():
    root = tk.Tk()
    DartVaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()