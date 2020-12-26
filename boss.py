import tkinter as tk
import configparser


# Boss screen class
class Boss:
    # Build window
    def __init__(self):
        # Configures window
        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.title("Sublime Text 3")

        # Loads config file
        config = configparser.ConfigParser()
        config.read("config.ini")

        # Binds exit screen
        self.window.bind(config["CONTROLS"]["boss"], self.die)

        # Display "working" screen
        background = tk.PhotoImage(
            master=self.window, file="images/bossKey.png")
        wrapper = tk.Label(self.window, image=background)
        wrapper.pack()

        # Display window
        self.window.mainloop()

    # Destroy window
    def die(self, event):
        # Quit and destroy used together allow the main game to resume
        self.window.quit()
        self.window.destroy()


# Warn users who execute this file directly
if __name__ == "__main__":
    print("You have executed the wrong file. Please read the README, "
          "and then execute the pressure.py file.")
