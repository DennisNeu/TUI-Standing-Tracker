import os
import json
from datetime import date


class StatsManager:
    """A class that manages the data for highscore and total standing time."""

    def __init__(self, filename: str):
        """Initialize the DataManager with a filename."""
        self.filename = filename
        self.highscores = []
        self.total_time = 0.0
        self.load_data()

    def load_data(self):
        """Load data from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.highscores = data.get("highscores", [])
                self.total_time = data.get("total_time", 0.0)
        else:
            self.highscores = []
            self.total_time = 0.0
            self.highscores.append({"date": str(date.today()), "score": 0.0})
            self.save_data()

    def save_data(self):
        """Save data to a JSON file."""
        data = {
            "highscores": self.highscores,
            "total_time": self.total_time
        }
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def add_score(self, score: float):
        """Add a score to the list and save it. Since append adds to the end
           of the list, the last score is the highest"""
        self.highscores.append({"date": str(date.today()), "score": score})
        self.save_data()

    def get_highscore(self) -> float:
        """Get the highest score from the list."""
        if self.highscores:
            return max(score["score"] for score in self.highscores)
        return 0.0
    
    def get_total_time(self) -> float:
        """Get the total time from the list."""
        return self.total_time
    
    def add_total_time(self, time: float):
        """Add time to the total time."""
        self.total_time += time
        self.save_data()

class SessionManager:
    """A class that manages the data for each standing session."""

    def __init__(self, filename: str):
        self.filename = filename
        self.sessions = []
        self.load_data()
    
    def load_data(self):
        """Load session data from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.sessions = json.load(file)
        else:
            self.sessions = []
            self.save_data()

    def save_data(self):
        """Save session data to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.sessions, file, indent=4)