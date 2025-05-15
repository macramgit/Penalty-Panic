import tkinter as tk
from model import Player, Goalkeeper
from view import TkinterView
import random

class GameController:
    def __init__(self, root):
        self.root = root
        self.player = Player()
        self.goalkeeper = Goalkeeper()
        self.view = TkinterView(root, self.shoot, self.reset_game, self.set_shot_direction)

        self.shot_direction = "center"
        self.player_score = 0
        self.goalkeeper_score = 0
        self.max_score = 5

    def start(self):
        self.view.display_message("Tura gracza. Naciśnij strzałkę, a następnie spację, aby strzelić.")

    def shoot(self):
        if not self.is_game_over():
            self.execute_shot(self.shot_direction)

    def execute_shot(self, shot_direction):
        direction_map = {"left": "lewo", "center": "środek", "right": "prawo"}
        direction_polish = direction_map.get(shot_direction, shot_direction)
        self.view.display_message(f"Gracz strzela w {direction_polish}")

        self.goalkeeper_direction = random.choice(["left", "center", "right", "left", "right"])
        self.view.animate_goalkeeper_move(self.goalkeeper_direction)
        ball_target_x, ball_target_y = self.calculate_target_coordinates(shot_direction)

        def on_ball_animation_complete():
            if shot_direction != self.goalkeeper_direction:
                self.player_score += 1
                self.view.display_message("Gol!")
            else:
                self.goalkeeper_score += 1
                self.view.display_message("Obrona!")

            self.view.display_score(self.player_score, self.goalkeeper_score)
            self.view.reset_ball_position()
            self.view.animate_goalkeeper_move("center")

            if self.is_game_over():
                self.display_winner()
                self.view.display_end_options()
            else:
                self.view.display_message("Tura gracza. Naciśnij strzałkę, aby strzelić.")

        self.view.animate_ball((ball_target_x, ball_target_y), on_ball_animation_complete)

    def set_shot_direction(self, direction):
        self.shot_direction = direction

    def reset_game(self):
        self.player_score = 0
        self.goalkeeper_score = 0
        self.view.reset_view()
        self.view.display_message("Tura gracza. Naciśnij strzałkę, aby strzelić.")

    def is_game_over(self):
        return self.player_score >= self.max_score or self.goalkeeper_score >= self.max_score

    def calculate_target_coordinates(self, direction):
        if direction == "left":
            return 250, 350
        elif direction == "right":
            return 550, 350
        else:
            return 400, 350

    def display_winner(self):
        if self.player_score > self.goalkeeper_score:
            self.view.display_winner("Gracz wygrywa!")
        else:
            self.view.display_winner("Bramkarz wygrywa!")

if __name__ == "__main__":
    root = tk.Tk()
    game = GameController(root)
    game.start()
    root.mainloop()
