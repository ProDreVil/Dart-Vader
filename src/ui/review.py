import os
import csv
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from utils.config import DATA_FILE
import random

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(SRC_DIR)
MOOD_IMAGE_DIR = os.path.join(
    PROJECT_DIR, "resources", "images", "mood"
)
MOOD_IMAGE_SIZE = (160, 160)

from utils.themes import THEME

class ReviewDisplayMixin:
    def load_reviews(self):
        if not os.path.exists(DATA_FILE):
            messagebox.showerror(
                "Reviews Not Found",
                f"Could not find the original reviews file:\n"
                f"{DATA_FILE}",
            )
            return []

        try:
            with open(
                DATA_FILE,
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

    def roll_review(self):
        if not self.reviews:
            messagebox.showwarning(
                "No Reviews",
                "No reviews are available. Check the original CSV file.",
            )
            return

        review = random.choice(self.reviews)
        self.current_review = review.copy()
        review_text = review.get("review_text", "").strip()

        self.review_label.configure(text=review_text)
        self.sentiment_label.configure(
            text="Not analyzed",
            fg=THEME["muted"],
        )
        self.score_label.configure(
            text="—",
            fg=THEME["text"],
        )
        self.show_mood("0.jpg", "Waiting for analysis...")

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