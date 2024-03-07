import customtkinter as ck
import tkinter as tk
from CTkListbox import *
from typing import Callable


class NavigationPanel(ck.CTkFrame):


    def __init__(self,
                 master,
                 initial_data: list[str],
                 selection_changed: Callable[[str], None],
                 add_new: Callable[[str], None],
                 **kwargs):
        super().__init__(master, **kwargs)

        # Search bar
        # self._search_value = tk.StringVar(value="")
        # search_bar = ck.CTkEntry(self, textvariable=self._search_value)
        # search_bar.bind("<KeyPress>", self._search)

        # Add Button
        ck.CTkButton(self,text="Neue Pflanze", command=add_new).pack(side="top", pady=4)

        # Listbox

        self._listbox = CTkListbox(self, command=selection_changed, fg_color="white", text_color="black")
        initial_data.sort()
        self.data = initial_data
        self._listbox.pack(side="top", fill="both", expand=True)

        self._refresh()

    def _refresh(self):
        self._listbox.delete("all")
        self.data.sort()
        for el in self.data:
            self._listbox.insert("end", el)

    def add_item(self, item: str):
        self.data.append(item)
        self._refresh()

    def delete_item(self, item: str):
        self.data.remove(item)
        self._refresh()


    def update_item(self, old_name: str, new_name: str):
        for i, el in enumerate(self.data):
            if el == old_name:
                self.data[i] = new_name
                break
        self._refresh()


