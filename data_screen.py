"""A screen to display the history of scores."""

from datetime import datetime

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Header, Footer
from textual.containers import Container, VerticalScroll, Horizontal
from textual.binding import Binding

import pyfiglet



class DataScreen(Screen):
    """A screen to display the history of scores."""

    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding("h", "app.pop_screen()", "Back to main screen"),
        Binding("t", "toggle_timer", "Toggle Timer", show=False),
        Binding("r", "reset_timer", "Reset Timer", show=False),
    ]

    def __init__(self, stats_manager) -> None:
        """Initialize the HighscoreScreen with a DataManager instance."""
        super().__init__()
        self.stats_manager = stats_manager
        self.highscores = self.stats_manager.highscores

    def compose(self) -> ComposeResult:
        ascii_title = pyfiglet.figlet_format("Stand Up!", font="slant")

        yield VerticalScroll(
            Header(show_clock=True, icon=""),
            Static(ascii_title, id="title"),
            Container(id="highscore-list", classes="highscore-list"),
            Footer(show_command_palette=False),
            id="app-wrapper",
        )

    def on_mount(self) -> None:
        """Event handler called when the screen is mounted."""
        highscores = list(reversed(self.highscores))  # Reverse to show the latest scores first
        highscore_list = self.query_one("#highscore-list")
        
        for score in highscores:
            minutes, seconds = divmod(score['score'], 60)
            formatted_date = datetime.strptime(score['date'], "%Y-%m-%d").strftime("%d.%m.%Y")
            
            # Wrap each score in its own container with proper spacing
            score_container = Horizontal(
                Static(
                    f"{formatted_date}: {int(minutes):02d} minutes, {seconds:05.2f} seconds",
                    classes="highscore-item"
                ),
                classes="highscore-container"
            )
            highscore_list.mount(score_container)
