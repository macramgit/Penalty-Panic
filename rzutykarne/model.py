from abc import ABC, abstractmethod
import random

class Participant(ABC):
    @abstractmethod
    def __init__(self):
        self.score = 0

    @abstractmethod
    def increase_score(self):
        pass

    @abstractmethod
    def get_score(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

class Player(Participant):
    def __init__(self):
        super().__init__()
        self.score = 0

    def increase_score(self):
        self.score += 1

    def get_score(self):
        return self.score

    def __len__(self):
        return self.score

    def __add__(self, other):
        if isinstance(other, Player):
            new_player = Player()
            new_player.score = self.score + other.score  # te przeciążenia lekko na sile, ale są
            return new_player
        raise ValueError("Cannot add Player with non-Player object")

    def __str__(self):
        return f"Player with score {self.score}"

class Goalkeeper(Participant):
    def __init__(self):
        super().__init__()
        self.saves = 0

    def save(self, player_shot_direction):
        return random.choice(["left", "center", "right"])

    def increase_score(self):
        self.saves += 1

    def reset_saves(self):
        self.saves = 0

    def get_score(self):
        return self.saves

    def __len__(self):
        return self.saves

    def __add__(self, other):
        if isinstance(other, Goalkeeper):
            new_goalkeeper = Goalkeeper()
            new_goalkeeper.saves = self.saves + other.saves # te przeciążenia lekko na sile, ale są
            return new_goalkeeper
        raise ValueError("Cannot add Goalkeeper with non-Goalkeeper object")

    def __str__(self):
        return f"Goalkeeper with {self.saves} saves"
