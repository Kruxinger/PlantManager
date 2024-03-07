import datetime

import customtkinter as ck
from navigation_panel import NavigationPanel
from main_panel import MainPanel
from plant import Plant
import pickle
import os
from tkinter import messagebox as mb

class MainWindow(ck.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("PlantManager")
        self.geometry("1030x800")


        if os.path.exists("plants.pkl"):
            with open('plants.pkl', 'rb') as inp:
                self.data: list[Plant] = pickle.load(inp)
            self._element_is_new = False
        else:
            self.data: list[Plant] = [Plant("", "", "")]
            self._element_is_new = True
        self.current_plant = self.data[0]
        self.nav_panel = NavigationPanel(self, [el.name for el in self.data], self.selection_changed, self.btn_new_clicked, fg_color="white")
        self.nav_panel.pack(side="left", fill="y", anchor="w", padx=4, pady=4)
        self.main_panel = MainPanel(
            self,
            self.current_plant,
            fg_color="white",
            save=self.save,
            delete=self.delete
        )
        self.main_panel.pack(side="left", fill="both", expand=True, padx=4, pady=4)

    def delete(self):
        res = mb.askquestion('Pflanze löschen',
                             'Möchtest du die Pflanze wirklich löschen?')
        if res == "yes":
            self.data = [el for el in self.data if el != self.current_plant]
            self.nav_panel.delete_item(self.current_plant.name)
            with open('plants.pkl', 'wb') as inp:
                pickle.dump(self.data, inp)
            if len(self.data):
                self.selection_changed(self.data[0].name)
            else:
                self.btn_new_clicked()

    def save(self):
        self.current_plant.name = self.main_panel.name.get()
        self.current_plant.heyday = self.main_panel.heyday.get()
        self.current_plant.last_modified = datetime.datetime.now()
        self.current_plant.location = self.main_panel.location.get()
        self.current_plant.etymologie = self.main_panel.etymologie.get()
        self.current_plant.eatable = self.main_panel.eatable.get()
        self.current_plant.further_info = self.main_panel.further_info.get("1.0","end")
        with open('plants.pkl', 'wb') as inp:
            pickle.dump(self.data, inp)
        if self._element_is_new:
            self.nav_panel.add_item(self.current_plant.name)

    def selection_changed(self, item: str):
        self._element_is_new = False
        if self.main_panel.element_changed():
            res = mb.askquestion('Änderungen speichern',
                                 'Möchtest du möglich Änderungen an der aktuellen Pflanze speichern?')
            if res == "yes":
                old_name = self.current_plant.name
                self.save()
                self.nav_panel.update_item(old_name, self.current_plant.name)
        self.current_plant = next(el for el in self.data if el.name == item)
        self.main_panel.set_to_plant(self.current_plant)

    def btn_new_clicked(self):
        if self.main_panel.element_changed():
            res = mb.askquestion('Pflanze löschen',
                                 'Möchtest du möglich Änderungen an der aktuellen Pflanze speichern?')
            if res == "yes":
                self.save()
                self.nav_panel.add_item(self.current_plant.name)
        self.current_plant = Plant("","","")
        self._element_is_new = True
        self.data.append(self.current_plant)
        self.main_panel.set_to_plant(self.current_plant)



if __name__=="__main__":
    ck.set_default_color_theme("blue")
    MainWindow().mainloop()