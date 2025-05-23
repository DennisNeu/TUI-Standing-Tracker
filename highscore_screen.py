"""A screen to display the history of scores."""

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Header, Footer
from textual.containers import Container
from textual.binding import Binding


class HighscoreScreen(Screen):
    """A screen to display the history of scores."""

    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding("h", "app.pop_screen()", "Back to main screen"),
        Binding("t", "toggle_timer", "Toggle Timer", show=False),
        ("r", "reset_timer", "Reset Timer"),
    ]

    def __init__(self, data_manager) -> None:
        """Initialize the HighscoreScreen with a DataManager instance."""
        super().__init__()
        self.data_manager = data_manager
        # self.highscores = self.data_manager.highscores # Not sure if this is correct

    def compose(self) -> ComposeResult:
        yield Container(
            Header(show_clock=True, icon=""),
            Static("Highscores", id="highscore_title"),
            Static("Date: Score", id="highscore_header"),
            Footer(show_command_palette=False),
            id="app-wrapper",
        )


    # This is probably bogus too
    def display(self):
        """Display the highscore screen."""
        print("Highscores:")
          #for entry in self.highscores:
          #  print(f"Date: {entry['date']}, Score: {entry['score']}")