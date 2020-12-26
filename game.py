import tkinter as tk
from random import shuffle, randint
import configparser
import json
from os import remove

from boss import Boss
from pause_menu import PauseMenu
from game_over import GameOver


# Main game class
class Game:
    # Build window and configure game
    def __init__(self, load):
        # Define key flags and lists
        self.walls = []
        self.plates = []
        self.float = 0
        self.paused = False
        self.halted = False

        # Configures window
        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.protocol("WM_DELETE_WINDOW", self.prevent)
        self.window.title("Pressure")

        # Loads config file
        config = configparser.ConfigParser()
        config.read("config.ini")

        # Bind keys based on controls file
        self.window.bind(config["CONTROLS"]["up"], self.up)
        self.window.bind(config["CONTROLS"]["down"], self.down)
        self.window.bind(config["CONTROLS"]["left"], self.left)
        self.window.bind(config["CONTROLS"]["right"], self.right)
        self.window.bind("<Control-R>", self.cheat_reset)
        self.window.bind("<Control-F>", self.cheat_float)
        self.window.bind(config["CONTROLS"]["boss"], self.boss)
        self.window.bind("<Escape>", self.pause)

        # Create canvas
        self.canvas = tk.Canvas(self.window, height=1080, width=1920)

        # Generate outer walls
        self.walls.append(self.canvas.create_rectangle(
            0, 0, 1920, 30, fill="black"))
        self.walls.append(self.canvas.create_rectangle(
            0, 0, 30, 1080, fill="black"))
        self.walls.append(self.canvas.create_rectangle(
            0, 1050, 1920, 1080, fill="black"))
        self.walls.append(self.canvas.create_rectangle(
            1890, 0, 1920, 1080, fill="black"))

        # Define coordinates of inner walls
        self.wall_coords = ((1, 1, 9, 1), (0, 11, 1, 5), (1, 13, 3, 1),
                            (3, 13, 3, 1), (5, 13, 3, 1), (7, 9, 8, 1),
                            (6, 11, 1, 1), (3, 9, 6, 1), (2, 7, 1, 7),
                            (4, 9, 1, 1), (6, 9, 1, 1), (3, 1, 1, 5),
                            (3, 3, 1, 5), (3, 5, 1, 5), (9, 0, 6, 1),
                            (9, 9, 8, 1), (10, 7, 1, 6), (11, 7, 7, 1),
                            (10, 5, 1, 2), (11, 1, 4, 1), (13, 0, 4, 1),
                            (15, 1, 4, 1), (17, 0, 9, 1), (12, 5, 1, 4),
                            (11, 15, 1, 7), (13, 8, 6, 1), (14, 9, 1, 2),
                            (14, 11, 1, 2), (14, 13, 1, 2), (14, 15, 1, 2),
                            (17, 10, 5, 1), (19, 9, 9, 1), (19, 9, 1, 7),
                            (21, 11, 5, 1), (21, 11, 1, 5), (23, 13, 3, 1),
                            (23, 13, 1, 3), (25, 15, 1, 1), (19, 1, 7, 1),
                            (19, 7, 1, 7), (21, 1, 5, 1), (21, 5, 1, 5),
                            (23, 1, 3, 1), (23, 3, 1, 3), (25, 1, 1, 1),
                            (27, 3, 13, 1), (29, 2, 2, 1), (29, 5, 4, 1),
                            (29, 10, 4, 1), (29, 15, 3, 1), (27, 0, 2, 4))

        # Put walls onto canvas
        for wall in self.wall_coords:
            self.generate_wall(wall[0], wall[1], wall[2], wall[3])

        # Recall saved game if available or generate new game
        if load:
            # Recover data from file
            raw_data = open("save.json")
            save = json.load(raw_data)

            # Recover key status data and score
            self.plate_pointer = save["plate_pointer"]
            self.plate_coords = save["plate_coords"]
            self.ticks = save["score"]
            self.player_coords = save["player_coords"]

            # Generate pressure plates in original positions
            for i in range(len(save["plates"])):
                self.generate_plate(
                    save["plates"][i]["origin"][0],
                    save["plates"][i]["origin"][1],
                    self.plate_colour(save["plates"][i]),
                    save["plates"][i]["full_time"],
                    save["plates"][i]["remaining_time"])

            # Display score text
            self.score = self.canvas.create_text(
                1785, 90, text=save["score"], fill="white", font=("Arial", 50))

            # Display player in original positions
            self.player = self.canvas.create_oval(
                save["player_coords"][0], save["player_coords"][1],
                save["player_coords"][2], save["player_coords"][3],
                fill="blue")

            # Destroy save file
            remove("save.json")
        else:
            # Define key status data
            self.plate_pointer = 3
            self.ticks = 0

            # Generate possible coordinates for pressure plates
            self.plate_coords = []
            x = 35
            while x < 1920:
                y = 35
                while y < 1080:
                    if not self.test_wall_collision(
                            self.canvas.find_overlapping(
                                x, y, x + 50, y + 50)):
                        self.plate_coords.append(
                            ((x - 35) // 60, (y - 35) // 60))
                    y += 60
                x += 60

            # Randomise where pressure plates appear
            shuffle(self.plate_coords)

            # Display starting three plates
            self.generate_plate(
                self.plate_coords[0][0], self.plate_coords[0][1], "green")
            self.generate_plate(
                self.plate_coords[1][0], self.plate_coords[1][1], "green")
            self.generate_plate(
                self.plate_coords[2][0], self.plate_coords[2][1], "green")

            # Display score text
            self.score = self.canvas.create_text(
                1785, 90, text=0, fill="white", font=("Arial", 50))

            # Display player in top left of screen
            self.player = self.canvas.create_oval(35, 35, 85, 85, fill="blue")

        # Put canvas onto window
        self.canvas.pack()

        # Starts game "ticking" - allows the game to progress
        self.tick()

        # Display window
        self.window.mainloop()

    # Handle "move up" key pressed
    def up(self, event):
        # Gets coordinates and checks for walls in new place
        coords = self.canvas.coords(self.player)
        overlaps = self.canvas.find_overlapping(
            coords[0], coords[1] - 60, coords[2], coords[3] - 60)

        # Stop execution if wall is in the way
        if self.test_wall_collision(overlaps):
            return

        # Reset pressure plate if touched
        self.test_plates_collision(overlaps)

        # Move player
        self.move(0, 0, -2)

    # Handle "move down" key pressed
    def down(self, event):
        # Gets coordinates and checks for walls in new place
        coords = self.canvas.coords(self.player)
        overlaps = self.canvas.find_overlapping(
            coords[0], coords[1] + 60, coords[2], coords[3] + 60)

        # Stop execution if wall is in the way
        if self.test_wall_collision(overlaps):
            return

        # Reset pressure plate if touched
        self.test_plates_collision(overlaps)

        # Move player
        self.move(0, 0, 2)

    # Handle "move left" key pressed
    def left(self, event):
        # Gets coordinates and checks for walls in new place
        coords = self.canvas.coords(self.player)
        overlaps = self.canvas.find_overlapping(
            coords[0] - 60, coords[1], coords[2] - 60, coords[3])

        # Stop execution if wall is in the way
        if self.test_wall_collision(overlaps):
            return

        # Reset pressure plate if touched
        self.test_plates_collision(overlaps)

        # Move player
        self.move(0, -2, 0)

    # Handle "move right" key pressed
    def right(self, event):
        # Gets coordinates and checks for walls in new place
        coords = self.canvas.coords(self.player)
        overlaps = self.canvas.find_overlapping(
            coords[0] + 60, coords[1], coords[2] + 60, coords[3])

        # Stop execution if wall is in the way
        if self.test_wall_collision(overlaps):
            return

        # Reset pressure plate if touched
        self.test_plates_collision(overlaps)

        # Move player
        self.move(0, 2, 0)

    # Move player
    def move(self, n, x, y):
        # Move player to new location
        self.canvas.move(self.player, x, y)

        # Animate movement
        n += 1
        if n < 30:
            self.canvas.after(1, self.move, n, x, y)

    # Handle reset cheat activation
    def cheat_reset(self, event):
        # Loop through all existing plates
        i = 0
        while i < len(self.plates):
            # Reset timer and colour
            self.plates[i]["remaining_time"] = self.plates[i]["full_time"]
            self.canvas.itemconfig(self.plates[i]["id"], fill="green")
            i += 1

    # Handle float cheat activation
    def cheat_float(self, event):
        # Activate cheat for 1000 ticks
        self.float = 1000

    # Handle "pause" key pressed
    def pause(self, event):
        # Set paused flag and launch pause menu
        self.paused = True
        PauseMenu(self)

        # Unset paused flag after pause menu closed
        self.paused = False

    # Handle "boss key" pressed
    def boss(self, event):
        # Do not allow boss screen to appear when the game is paused
        if self.paused:
            return

        # Set paused flag and launch boss screen
        self.paused = True
        Boss()

        # Unset paused flag
        self.paused = False

    # Check if player tries to move into wall
    def test_wall_collision(self, overlaps):
        # Prevent movement if game paused
        if self.paused:
            return True

        # Allow movement if the float cheat is active
        if self.float > 0:
            return False

        # Test if wall is in the way
        for item in overlaps:
            if item in self.walls:
                return True

        # If this line is reached, there is no collision
        return False

    # Check if player has touched pressure plate
    def test_plates_collision(self, overlaps):
        # Check each plate in sequence
        for item in overlaps:
            i = 0
            while i < len(self.plates):
                # Test for overlap
                if (self.plates[i]["id"] == item):
                    # Reset time to full and change colour to green
                    self.plates[i]["remaining_time"] = \
                        self.plates[i]["full_time"]
                    self.canvas.itemconfig(self.plates[i]["id"], fill="green")
                i += 1

    # Determine pressure plate colour
    def plate_colour(self, plate):
        ratio = plate["remaining_time"] / plate["full_time"]
        if ratio <= 0.1:  # Red for <10% of lifespan
            return "red"
        elif ratio <= 0.25:  # Orange for 10-25% of lifespan
            return "orange"
        elif ratio <= 0.5:  # Yellow for 25-50% of lifespan
            return "yellow"
        else:
            return "green"

    # Generate walls
    def generate_wall(self, originx, originy, height, width):
        # Calculate coordinates
        x1 = (originx * 60) + 30
        y1 = (originy * 60) + 30
        x2 = x1 + (width * 60)
        y2 = y1 + (height * 60)

        # Draw wall on canvas and keep object in list
        self.walls.append(self.canvas.create_rectangle(
            x1, y1, x2, y2, fill="black"))

    # Generate pressure plates
    def generate_plate(self, originx, originy, colour, *args):
        # Calculate coordinates
        x1 = (originx * 60) + 35
        y1 = (originy * 60) + 35
        x2 = x1 + 50
        y2 = y1 + 50

        # Draw pressure plate on canvas
        plate = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colour)

        if len(args) > 0:
            # Keep object in list
            self.plates.append({
                "id": plate,
                "full_time": args[0],
                "remaining_time": args[1],
                "origin": (originx, originy)
            })
        else:
            # Choose random time period for pressure plate
            time = randint(20, 40)

            # Keep object in list
            self.plates.append({
                "id": plate,
                "full_time": time,
                "remaining_time": time,
                "origin": (originx, originy)
            })

    # Save game
    def save(self):
        # Build save object
        save = {}
        save["score"] = self.ticks
        save["plate_pointer"] = self.plate_pointer
        save["plate_coords"] = self.plate_coords
        save["player_coords"] = self.canvas.coords(self.player)
        save["plates"] = self.plates

        # Save game to file
        with open("save.json", "w") as output:
            json.dump(save, output)

    # Handle game "tick" - every 10ms
    def tick(self):
        # Close game if halted
        if self.halted:
            # Quit and destroy used together allow the main menu to resume
            self.window.quit()
            self.window.destroy()
        else:
            # Only tick if the game isn't paused
            if not self.paused:
                # Add tick - used for score
                self.ticks += 1

                # Update score text
                self.canvas.itemconfig(self.score, text=self.ticks)

                # Do these actions every second
                if self.ticks % 100 == 0:
                    # Loop through pressure plates
                    i = 0
                    while i < len(self.plates):
                        # Check for pressure plates expiring
                        if self.plates[i]["remaining_time"] <= 0:
                            # End game
                            self.paused = True
                            GameOver(self.ticks)
                            self.die()
                            break
                        # Reduce lifespan of pressure plate
                        self.plates[i]["remaining_time"] -= 1

                        # Calculate new pressure plate colour
                        colour = self.plate_colour(self.plates[i])

                        # Recolour pressure plate
                        self.canvas.itemconfig(
                            self.plates[i]["id"], fill=colour)
                        i += 1

                # If float cheat is active, decrement its lifespan by one
                if self.float > 0:
                    self.float -= 1

                # Do these actions every 30 seconds
                if self.ticks % 3000 == 0:
                    # Generate new pressure plate
                    self.generate_plate(
                        self.plate_coords[self.plate_pointer][0],
                        self.plate_coords[self.plate_pointer][1],
                        "green")
                    self.plate_pointer += 1

                    # Brings player forward in canvas so it goes over plates
                    self.canvas.tag_raise(self.player)

            # Tick again after 10ms
            self.window.after(10, self.tick)

    # Dummy function used to disable close button
    def prevent(self):
        pass

    # End game
    def die(self):
        # Set halted flag to stop game
        self.halted = True


# Warn users who execute this file directly
if __name__ == "__main__":
    print("You have executed the wrong file. Please read the README, "
          "and then execute the pressure.py file.")
