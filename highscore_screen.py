"""A screen to display the history of scores."""

from textual.screen import Screen

class HighscoreScreen(Screen):
    """A screen to display the history of scores."""

    def __init__(self, data_manager):
        """Initialize the HighscoreScreen with a DataManager instance."""
        self.data_manager = data_manager
        self.highscores = self.data_manager.highscores # Not sure if this is correct

    # This is probably bogus too
    def display(self):
        """Display the highscore screen."""
        print("Highscores:")
        for entry in self.highscores:
            print(f"Date: {entry['date']}, Score: {entry['score']}")