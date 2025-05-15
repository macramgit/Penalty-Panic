import tkinter as tk
from PIL import Image, ImageTk

class TkinterView:
    def __init__(self, root, shoot_callback, reset_callback, set_shot_direction_callback):
        self.root = root
        self.root.title("Symulator rzutów karnych")

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.goal_image = ImageTk.PhotoImage(Image.open("goal.png").resize((800, 600)))
        self.ball_image = ImageTk.PhotoImage(Image.open("ball.png").resize((50, 50)))
        self.goalkeeper_image = ImageTk.PhotoImage(Image.open("goalkeeper.png").resize((150, 200)))

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.goal_image)
        self.ball_id = self.canvas.create_image(400, 550, anchor=tk.CENTER, image=self.ball_image)
        self.goalkeeper_id = self.canvas.create_image(400, 380, anchor=tk.CENTER, image=self.goalkeeper_image)

        self.message_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.message_label.pack()

        self.score_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.score_label.pack()

        self.play_again_button = tk.Button(root, text="Zagraj ponownie", command=reset_callback)
        self.quit_button = tk.Button(root, text="Wyjdź", command=root.quit)

        self.shoot_callback = shoot_callback
        self.set_shot_direction_callback = set_shot_direction_callback

        self.bind_keys()

    def display_score(self, player_score, goalkeeper_score):
        self.score_label.config(text=f"Wynik: Gracz {player_score} - Bramkarz {goalkeeper_score}")

    def display_message(self, message):
        self.message_label.config(text=message)

    def display_winner(self, winner_message):
        self.message_label.config(text=winner_message)

    def display_end_options(self):
        self.play_again_button.pack(side=tk.LEFT, padx=20)
        self.quit_button.pack(side=tk.LEFT, padx=20)

    def reset_view(self):
        self.play_again_button.pack_forget()
        self.quit_button.pack_forget()
        self.reset_ball_position()
        self.reset_goalkeeper_position()
        self.display_message("")
        self.display_score(0, 0)

    def bind_keys(self):
        self.root.bind('<space>', lambda event: self.shoot_callback())
        self.root.bind('<Left>', lambda event: self.set_shot_direction_callback("left"))
        self.root.bind('<Up>', lambda event: self.set_shot_direction_callback("center"))
        self.root.bind('<Right>', lambda event: self.set_shot_direction_callback("right"))

    def animate_ball(self, target_position, callback):
        current_position = self.canvas.coords(self.ball_id)
        steps = 25  # to zwieksza plynnosc animacji lotu piłki
        delta_x = (target_position[0] - current_position[0]) / steps
        delta_y = (target_position[1] - current_position[1]) / steps

        def animate(step=0):
            if step < steps:
                current_position[0] += delta_x
                current_position[1] += delta_y
                self.canvas.coords(self.ball_id, current_position)
                self.root.after(20, animate, step + 1)
            else:
                callback()

        animate()

    def reset_ball_position(self):
        self.canvas.coords(self.ball_id, 400, 550)

    def animate_goalkeeper_move(self, direction):
        current_position = self.canvas.coords(self.goalkeeper_id)

        target_positions = {"left": (300, 380), "center": (400, 380), "right": (500, 380)}
        target_position = target_positions.get(direction, current_position)

        steps = 20  # to zwieksza plynnosc animacji lotu piłki
        delta_x = (target_position[0] - current_position[0]) / steps

        def animate(step=0):
            if step < steps:
                current_position[0] += delta_x
                self.canvas.coords(self.goalkeeper_id, current_position)
                self.root.after(20, animate, step + 1)  # Decrease the delay for smoother animation
            else:
                self.canvas.coords(self.goalkeeper_id, target_position)

        animate()

    def reset_goalkeeper_position(self):
        self.canvas.coords(self.goalkeeper_id, 400, 380)
