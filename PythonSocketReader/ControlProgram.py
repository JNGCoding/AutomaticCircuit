from tkinter import * # type: ignore
from ControlPacket import ControlPacket
from typing import Callable

class ControlWindow(object):
    def __init__(self, title: str, size: str, color: str) -> None:
        self.window: Tk = Tk()
        self.window.withdraw()

        self.window.title(title)
        self.window.geometry(size)
        self.window.resizable(False, False)
        self.window.configure(background=color)
        self.window.protocol("WM_DELETE_WINDOW", self.exit_program)

        self.buttons: dict = {
            "RELAY1": Button(self.window, text="Relay 1 OFF", highlightbackground="black", highlightthickness=2),
            "RELAY2": Button(self.window, text="Relay 2 OFF", highlightbackground="black", highlightthickness=2),
            "AutoMode": Button(self.window, text="AutoMode OFF", highlightbackground="black", highlightthickness=2)
        }

        self.labels: dict = {
            "Temperature": Label(self.window, text="Temperature: -- °C"),
            "Humidity": Label(self.window, text="Humidity: -- %"),
            "Light": Label(self.window, text="Light: -- Lux")
        }

        for label in self.labels.values():
            label.configure(background=color, font=("Arial", 14))
            label.pack(pady=10)

        for button in self.buttons.values():
            button.configure(width=27, height=5, highlightbackground="black", highlightthickness=2)
            button.pack(pady=5)

        self.TextInputVar = StringVar()
        self.TextInput = Entry(self.window, textvariable=self.TextInputVar, width=30)
        self.TextInput.pack(side="bottom")

        self.variables: dict = {
            "RELAY1": False,
            "RELAY2": False,
            "AutoMode": False,
            "Temperature": 0.0,
            "Humidity": 0.0,
            "Light": 0.0
        }

        self.exit_func: Callable | None = None

    def set_exit_function(self, func: Callable) -> None:
        self.exit_func = func

    def update_variables(self, Data: ControlPacket) -> None:
        self.variables["RELAY1"] = Data.relay1
        self.variables["RELAY2"] = Data.relay2
        self.variables["AutoMode"] = Data.auto_mode
        self.variables["Temperature"] = Data.temperature
        self.variables["Humidity"] = Data.humidity
        self.variables["Light"] = Data.light
    
    def disable_text_input(self):
        self.TextInput.configure(state=DISABLED)

    def enable_text_input(self):
        self.TextInput.configure(state=NORMAL)

    def bind_entry_command(self, key: str, command: Callable) -> None:
        self.TextInput.bind(key, command)
    
    def clear_entry_text(self) -> None:
        self.TextInputVar.set("")

    def assign_button_command(self, button_name: str, command: Callable) -> None:
        if button_name in self.buttons:
            self.buttons[button_name].configure(command=command)
        else:
            raise ValueError(f"Button '{button_name}' does not exist.")
        
    def update_label(self, label_name: str, text: str) -> None:
        if label_name in self.labels:
            self.labels[label_name].configure(text=text)
        else:
            raise ValueError(f"Label '{label_name}' does not exist.")
        
    def update(self) -> None:
        self.update_label("Temperature", f"Temperature: {self.variables['Temperature']} °C")
        self.update_label("Humidity", f"Humidity: {self.variables['Humidity']} %")
        self.update_label("Light", f"Analog Light: {self.variables['Light']}")

        if self.variables["RELAY1"]:
            self.buttons["RELAY1"].configure(text="Relay 1 ON")
        else:
            self.buttons["RELAY1"].configure(text="Relay 1 OFF")

        if self.variables["RELAY2"]:
            self.buttons["RELAY2"].configure(text="Relay 2 ON")
        else:
            self.buttons["RELAY2"].configure(text="Relay 2 OFF")

        if self.variables["AutoMode"]:
            self.buttons["AutoMode"].configure(text="Auto Mode ON")
            self.buttons["RELAY1"].configure(state=DISABLED)
            self.buttons["RELAY2"].configure(state=DISABLED)
        else:
            self.buttons["AutoMode"].configure(text="Auto Mode OFF")
            self.buttons["RELAY1"].configure(state=NORMAL)
            self.buttons["RELAY2"].configure(state=NORMAL)

    def exit_program(self, func = None) -> None:
        print("Exiting program...")
        if self.exit_func is not None:
            self.exit_func()
        self.window.destroy()

    def start_loop(self) -> None:
        self.window.deiconify()
        self.window.mainloop()
