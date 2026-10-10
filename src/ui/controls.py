import tkinter as tk
from tkinter import messagebox

from utils.themes import THEME, FONTS
from sentiment.analyzer import analyze_sentiment

class ControlsMixin:
    def build_controls(self, controls_section):
        button_style = {
            "font": FONTS["button"],
            "fg": THEME["button_text"],
            "relief": "flat",
            "cursor": "hand2",
            "pady": 9,
        }

        roll_style = {
            **button_style,
            "bg": THEME["roll_button"],
            "activebackground": THEME["roll_button_hover"],
        }

        analysis_style = {
            **button_style,
            "bg": THEME["analysis_button"],
            "activebackground": THEME["analysis_button_hover"],
        }

        custom_style = {
            **button_style,
            "bg": THEME["custom_button"],
            "activebackground": THEME["custom_button_hover"],
        }

        self.roll_button = tk.Button(
            controls_section,
            text="Roll a Review",
            command=self.roll_review,
            **roll_style,
        )
        self.roll_button.grid(
            row=0, column=0, sticky="ew", padx=(0, 5), pady=5
        )

        self.start_analysis_button = tk.Button(
            controls_section,
            text="Start Analysis",
            command=self.start_analysis,
            **analysis_style,
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
            **custom_style,
        )
        self.run_custom_button.grid(
            row=1, column=1, sticky="ew", padx=(5, 0), pady=5
        )

    def start_analysis(self):
        if self.current_review is None:
            messagebox.showwarning(
                "No Review Selected",
                "Click Roll a Review before starting the analysis.",
            )
            return

        review_text = self.current_review.get("review_text", "").strip()

        if not review_text:
            messagebox.showwarning(
                "Empty Review",
                "The selected review has no text to analyze.",
            )
            return

        try:
            result = analyze_sentiment(review_text)
            sentiment = result["sentiment"]
            score = float(result["score"])

            self.current_review["sentiment"] = sentiment
            self.current_review["sentiment_score"] = score
            self.display_review(review_text, sentiment, score)

        except (KeyError, TypeError, ValueError) as error:
            messagebox.showerror(
                "Analysis Failed",
                f"Could not process the analysis result:\n{error}",
            )

        except Exception as error:
            messagebox.showerror(
                "Analysis Failed",
                f"An error occurred during analysis:\n{error}",
            )

    def analyze_custom_review(self):
        review_text = self.custom_review_entry.get().strip()

        if not review_text or review_text == "Type a custom review...":
            messagebox.showwarning(
                "Empty Review",
                "Please type a review first.",
            )
            return

        try:
            result = analyze_sentiment(review_text)
            sentiment = result["sentiment"]
            score = float(result["score"])

            self.current_review = {
                "review_text": review_text,
                "sentiment": sentiment,
                "sentiment_score": score,
            }

            self.display_review(review_text, sentiment, score)

        except (KeyError, TypeError, ValueError) as error:
            messagebox.showerror(
                "Analysis Failed",
                f"Could not process the analysis result:\n{error}",
            )

        except Exception as error:
            messagebox.showerror(
                "Analysis Failed",
                f"An error occurred during analysis:\n{error}",
            )