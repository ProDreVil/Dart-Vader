import math
import random
import tkinter as tk

from utils.themes import THEME

class Dartboard(tk.Canvas):
    def __init__(self, parent, size=400, **kwargs):
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=kwargs.pop("bg", THEME["bg"]),
            highlightthickness=0,
            **kwargs,
        )
        self.size = size
        self.center = size / 2
        self.radius = size * 0.44
        self.segment_count = 12
        self.draw_board()

    def draw_board(self):
        self.delete("all")
        cx = self.center
        cy = self.center
        radius = self.radius
        angle_per_segment = 360 / self.segment_count
        for index in range(self.segment_count):
            start_angle = index * angle_per_segment
            self.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start_angle,
                extent=angle_per_segment,
                style=tk.PIESLICE,
                fill=THEME["board_colors"][index % len(THEME["board_colors"])],
                outline=THEME["board_border"],
                width=2,
            )
            middle_angle = math.radians(
                start_angle + angle_per_segment / 2
            )
            label_radius = radius * 0.72
            x = cx + label_radius * math.cos(middle_angle)
            y = cy - label_radius * math.sin(middle_angle)
            number = random.randint(1, 99)
            self.create_text(
                x,
                y,
                text=str(number),
                fill=THEME["board_number"],
                font=("Arial", 12, "bold"),
            )
        bullseye_radius = radius * 0.16
        self.create_oval(
            cx - bullseye_radius,
            cy - bullseye_radius,
            cx + bullseye_radius,
            cy + bullseye_radius,
            fill=THEME["bullseye"],
            outline=THEME["bullseye_border"],
            width=2,
        )
        inner_radius = bullseye_radius * 0.42
        self.create_oval(
            cx - inner_radius,
            cy - inner_radius,
            cx + inner_radius,
            cy + inner_radius,
            fill=THEME["bullseye_inner"],
            outline="",
        )