import os
import json
from datetime import datetime


class DataManager:
    """A class that manages the data for the application."""

    def __init__(self, filename: str):
        """Initialize the DataManager with a filename."""
        self.filename = filename
        self.highscores = []
        self.load_data()

    def load_data(self):
        """Load data from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.highscores = json.load(file)
        else:
            self.highscores = []
            self.highscores.append({"date": str(datetime.now()), "score": 0.0})
            self.save_data()

    def save_data(self):
        """Save data to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.highscores, file, indent=4)

    def add_score(self, score: float):
        """Add a score to the list and save it."""
        self.highscores.append(score)  # Append adds to end of list
        self.save_data()

    def get_last_score(self) -> dict:
        """Get the last score from the list."""
        if self.highscores:
            return self.highscores[-1]
