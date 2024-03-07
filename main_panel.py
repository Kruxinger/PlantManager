import customtkinter as ck
import tkinter as tk
from plant import Plant
from PIL import Image
import os
from tkinter.filedialog import askopenfile

from functools import partial
from typing import Callable


class MainPanel(ck.CTkScrollableFrame):
    def __init__(self, master, plant: Plant, save: Callable, delete: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self._plant = plant
        self._element_changed = False


        self.name = tk.StringVar(value=self._plant.name)
        self.heyday = tk.StringVar(value=self._plant.heyday)
        self.location = tk.StringVar(value=self._plant.location)
        self.eatable = tk.StringVar(value=self._plant.eatable)
        self.etymologie = tk.StringVar(value=self._plant.etymologie)

        panel_top = ck.CTkFrame(self, fg_color="white")
        panel_top.pack(side="top", anchor="w", padx=8, pady=8)
        panel_inner_left = ck.CTkFrame(panel_top, fg_color="white")
        panel_inner_left.pack(side="left", anchor="w", padx=8)
        panel_inner_right = ck.CTkFrame(panel_top, fg_color="white")
        panel_inner_right.pack(side="left", anchor="w", padx=8)
        # Name
        ck.CTkLabel(panel_inner_left, text="Name:").pack(side="top", pady=4, anchor="nw", padx=8)
        ck.CTkEntry(panel_inner_left, width=400, textvariable=self.name).pack(side="top", anchor="nw", padx=8)
        # Location
        ck.CTkLabel(panel_inner_left, text="Standort:").pack(side="top", pady=4, anchor="nw", padx=8)
        ck.CTkEntry(panel_inner_left, width=400, textvariable=self.location).pack(side="top", anchor="nw", padx=8)
        # Name
        ck.CTkLabel(panel_inner_left, text="Blütezeit:").pack(side="top", pady=4, anchor="nw", padx=8)
        ck.CTkEntry(panel_inner_left, width=400, textvariable=self.heyday).pack(side="top", anchor="nw", padx=8)
        # Name
        ck.CTkLabel(panel_inner_right, text="Essbar?").pack(side="top", pady=4, anchor="nw", padx=8)
        ck.CTkEntry(panel_inner_right, width=400, textvariable=self.eatable).pack(side="top", anchor="nw", padx=8)
        # Name
        ck.CTkLabel(panel_inner_right, text="Etymologie?").pack(side="top", pady=4, anchor="nw", padx=8)
        ck.CTkEntry(panel_inner_right, width=400, textvariable=self.eatable).pack(side="top", anchor="nw", padx=8)
        ck.CTkLabel(self, text="Zusätzliche Infos:").pack(side="top", pady=4, anchor="nw", padx=8)
        self.further_info = ck.CTkTextbox(self, width=800, height=100)
        self.further_info.pack(side="top", anchor="nw", padx=8)
        self.further_info.insert("end", self._plant.further_info)

        # Button
        button_frame = ck.CTkFrame(self, bg_color="white", fg_color="white")
        ck.CTkButton(button_frame, text="Löschen", command=delete).pack(side="left", padx=4)
        ck.CTkButton(button_frame, text="Speichern", command=save).pack(side="left", padx=4)
        button_frame.pack(side="top", anchor="w", padx=8)

        image_frame = ck.CTkFrame(self, bg_color="white", fg_color="white")
        # Image oben links

        self.image_buttons = []
        for i, path in enumerate(self._plant.image_paths):
            if path is None:
                img = Image.open("empty.png")
            else:
                img = Image.open(path)
            action = partial(self.load_new_image, i)
            button = ck.CTkButton(
                image_frame,
                image=ck.CTkImage(light_image=img, size=img.size),
                hover_color="lightgrey",
                fg_color="white",
                bg_color="white",
                text="",
                width=400,
                height=400,
                command=action
            )
            button.grid(column=int(i / 2), row=i % 2)
            self.image_buttons.append(button)
        image_frame.pack(side="top", anchor="w", padx=8)


    def element_changed(self) -> bool:
        self._element_changed = not(self.name.get() == self._plant.name)
        self._element_changed |= not(self.heyday.get() == self._plant.heyday)
        self._element_changed |= not(self.eatable.get() == self._plant.eatable)
        self._element_changed |= not(self.etymologie.get() == self._plant.etymologie)
        self._element_changed |= not(self.further_info.get("1.0","end") == self._plant.further_info)
        return self._element_changed

    def load_new_image(self, index: int):
        self._element_changed = True
        file = askopenfile(mode='r', filetypes=[
            ('Image File', '*.png'),
            ('Image File', '*.jpg'),
            ('Image File', '*.jpeg')])
        if file is not None:
            # Load and resize image
            image = Image.open(file.name)
            ratio = min(600 / image.size[0], 600 / image.size[1])
            image = image.resize(size=(int(ratio * image.size[0]), int(ratio * image.size[1])))
            i = 0
            file_name = f"plants\image_{i}.png"
            while os.path.exists(file_name):
                i += 1
                file_name = f"plants\image_{i}.png"

            image.save(file_name)
            self._plant.image_paths[index] = file_name
            self.image_buttons[index].configure(
                require_redraw=True,
                image=ck.CTkImage(light_image=image, size=image.size)
            )

    def set_to_plant(self, current_plant: Plant):
        self._element_changed = False
        self._plant = current_plant
        self.name.set(self._plant.name)
        self.heyday.set(self._plant.heyday)
        self.location.set(self._plant.location)
        self.etymologie.set(self._plant.etymologie)
        self.eatable.set(self._plant.eatable)
        self.further_info.delete("1.0", "end")
        self.further_info.insert("end", current_plant.further_info)

        for i, path in enumerate(self._plant.image_paths):
            if path is None:
                img = Image.open("empty.png")
            else:
                img = Image.open(path)
            self.image_buttons[i].configure(
                require_redraw=True,
                image=ck.CTkImage(light_image=img, size=img.size)
            )


