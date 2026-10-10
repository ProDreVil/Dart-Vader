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
        self.values = [None] * self.segment_count
        self.target_index = None
        self.active_segment = None
        self.animation_job = None
        self.draw_board()

    def assign_values(self, real_score):
        print("DEBUG real_score:", real_score)
        real_value = round(real_score * 100)
        print("DEBUG real_value:", real_value)
        positive_count = 6 if real_score > 0 else 5
        negative_count = 11 - positive_count

        positive_values = [
            random.randint(2, 99)
            for _ in range(positive_count)
        ]
        negative_values = [
            -random.randint(2, 99)
            for _ in range(negative_count)
        ]

        entries = [(value, False) for value in positive_values + negative_values]
        entries.append((real_value, True))

        random.shuffle(entries)

        self.values = [value for value, _ in entries]
        self.target_index = next(
            index
            for index, (_, is_real) in enumerate(entries)
            if is_real
        )
        self.active_segment = None
        self.draw_board()

        return self.target_index

    def highlight_segment(self, index):
        self.active_segment = index
        self.draw_board()

    def start_animation(self, target_index, on_complete):
        if self.animation_job is not None:
            self.after_cancel(self.animation_job)
            self.animation_job = None

        if target_index is None:
            on_complete()
            return

        self.animation_step = 0
        self.animation_total_steps = random.randint(24, 36)
        self.animation_target = target_index
        self.animation_callback = on_complete
        self._animate_step()

    def _animate_step(self):
        step = self.animation_step
        total = self.animation_total_steps

        if step >= total:
            self.highlight_segment(self.animation_target)
            self.animation_job = None
            callback = self.animation_callback
            self.animation_callback = None

            if callback:
                callback()
            return

        if step < total - 6:
            delay = 45
        else:
            delay = 45 + (step - (total - 6)) * 70

        segment = (step + random.randint(0, self.segment_count - 1)) % self.segment_count
        if step == total - 1:
            segment = self.animation_target

        self.highlight_segment(segment)
        self.animation_step += 1
        self.animation_job = self.after(delay, self._animate_step)

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
                fill=(
                    THEME["bullseye"]
                    if index == self.active_segment
                    else THEME["board_colors"][index % len(THEME["board_colors"])]
                ),
                outline=(
                    THEME["bullseye_border"]
                    if index == self.active_segment
                    else THEME["board_border"]
                ),
                width=4 if index == self.active_segment else 2,
            )
            middle_angle = math.radians(
                start_angle + angle_per_segment / 2
            )
            label_radius = radius * 0.72
            x = cx + label_radius * math.cos(middle_angle)
            y = cy - label_radius * math.sin(middle_angle)
            number = self.values[index]
            self.create_text(x, y, text="—" if number is None else (f"+{number}" if number > 0 else str(number)),
                fill=(
                    THEME["bullseye_border"]
                    if number == 1
                    else THEME["board_number"]
                ),
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