"""A screen to display the history of scores."""

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Header, Footer
from textual.containers import Container, VerticalScroll
from textual.binding import Binding


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
        yield Container(
            Header(show_clock=True, icon=""),
            VerticalScroll(id="highscore-list", classes="highscore-list"),
            Footer(show_command_palette=False),
            id="app-wrapper",
        )

    def on_mount(self) -> None:
        for score in self.highscores:
            score_display = Static(
                f"{score['date']}: {score['score']:.2f} seconds",
                classes="highscore-item"
            )
            self.query_one("#highscore-list").mount(score_display)