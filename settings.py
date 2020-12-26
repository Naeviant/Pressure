import tkinter as tk
from functools import partial
import configparser


# Settings screen class
class Settings:
    # Build window
    def __init__(self):
        # Configures window
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.prevent)
        self.window.resizable(False, False)
        self.window.title("Pressure: Settings")

        # Get controls config from INI file
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.buttons = {}

        # Display move up control
        tk.Label(self.window, text="Move Up:", height=2,
                 width=12).grid(row=0, column=0)
        text = self.config["CONTROLS"]["up"].lower()
        command = partial(self.enable_bind, "up")
        self.buttons["up"] = tk.Button(self.window,
                                       text=text,
                                       width=10,
                                       command=command)
        self.buttons["up"].grid(row=0, column=1)

        # Display move down control
        tk.Label(self.window, text="Move Down:",
                 height=2, width=12).grid(row=1, column=0)
        text = self.config["CONTROLS"]["down"].lower()
        command = partial(self.enable_bind, "up")
        self.buttons["down"] = tk.Button(self.window,
                                         text=text,
                                         width=10,
                                         command=command)
        self.buttons["down"].grid(row=1, column=1)

        # Display move left control
        tk.Label(self.window, text="Move Left:",
                 height=2, width=12).grid(row=2, column=0)
        text = self.config["CONTROLS"]["left"].lower()
        command = partial(self.enable_bind, "left")
        self.buttons["left"] = tk.Button(self.window,
                                         text=text,
                                         width=10,
                                         command=command)
        self.buttons["left"].grid(row=2, column=1)

        # Display move right control
        tk.Label(self.window, text="Move Right:",
                 height=2, width=12).grid(row=3, column=0)
        text = self.config["CONTROLS"]["right"].lower()
        command = partial(self.enable_bind, "right")
        self.buttons["right"] = tk.Button(self.window,
                                          text=text,
                                          width=10,
                                          command=command)
        self.buttons["right"].grid(row=3, column=1)

        # Display pause control, but don't allow changes
        tk.Label(self.window, text="Pause:", height=2,
                 width=12).grid(row=4, column=0)
        tk.Label(self.window, text="<escape>", width=10).grid(row=4, column=1)

        # Display boss key control
        tk.Label(self.window, text="Boss Key:", height=2,
                 width=12).grid(row=5, column=0)
        text = self.config["CONTROLS"]["boss"].lower()
        command = partial(self.enable_bind, "boss")
        self.buttons["boss"] = tk.Button(self.window,
                                         text=text,
                                         width=10,
                                         command=command)
        self.buttons["boss"].grid(row=5, column=1)

        # Display cancel and save buttons
        tk.Button(self.window, text="Cancel", width=22, command=partial(
            self.die, False)).grid(row=6, column=0, columnspan=2)
        tk.Button(self.window, text="Save & Close", width=22, command=partial(
            self.die, True)).grid(row=7, column=0, columnspan=2)

        # Display windows
        self.window.mainloop()

    # Enable all key binds to set controls
    def enable_bind(self, control):
        # Bind all keys to set given control
        self.control = control
        self.original = self.buttons[self.control].config()["text"][4]
        self.window.bind("<KeyPress>", self.disable_bind)

        # Display dash on control awaiting input
        self.buttons[self.control].config(text="-")

    # Disable all key binds after controls set
    def disable_bind(self, event):
        # Disable key binds
        self.window.unbind("<KeyPress>")

        # Validate key pressed is valid and set control
        char = event.char.lower()
        code = event.keycode
        if code == 111:
            char = "<Up>"
        elif code == 116:
            char = "<Down>"
        elif code == 113:
            char = "<Left>"
        elif code == 114:
            char = "<Right>"
        elif char == " ":
            char = "<space>"
        if char == "":
            self.buttons[self.control].config(text=self.original)
        else:
            self.config["CONTROLS"][self.control] = char
            self.buttons[self.control].config(text=char.lower())
        del self.control
        del self.original

    # Dummy function used to disable close button
    def prevent(self):
        pass

    # Destroy window
    def die(self, save):
        # If save button pressed, update config file with new controls
        if save:
            with open("config.ini", "w") as configfile:
                self.config.write(configfile)
        # Quit and destroy used together allow the main menu to resume
        self.window.quit()
        self.window.destroy()


# Warn users who execute this file directly
if __name__ == "__main__":
    print("You have executed the wrong file. Please read the README, "
          "and then execute the pressure.py file.")
