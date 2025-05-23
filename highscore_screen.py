"""A screen to display the history of scores."""

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static


class HighscoreScreen(Screen):
    """A screen to display the history of scores."""

    def __init__(self, data_manager) -> None:
        super().__init__()
        """Initialize the HighscoreScreen with a DataManager instance."""
        self.data_manager = data_manager
        # self.highscores = self.data_manager.highscores # Not sure if this is correct

    def compose(self) -> ComposeResult:
        yield Static("This is a test")


    # This is probably bogus too
    def display(self):
        """Display the highscore screen."""
        print("Highscores:")
          #for entry in self.highscores:
          #  print(f"Date: {entry['date']}, Score: {entry['score']}")