from timer import Timer
from datetime import date
from data_manager import DataManager

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.reactive import Reactive
from textual.containers import Vertical
import pyfiglet


class TrackerApp(App):
    """A simple app to track time spent standing on a sit-stand desk."""

    def __init__(self) -> None:
        super().__init__()
        self.data_manager = DataManager("data.json")
        self.highscore = self.data_manager.get_last_score()

    is_running = Reactive(False)

    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "toggle_timer", "Toggle Timer"),
        ("r", "reset_timer", "Reset Timer"),
    ]

    def on_mount(self) -> None:
        self.title = ""
        self.theme = "tokyo-night"

    def compose(self) -> ComposeResult:
        """Generate layout for the app."""
        ascii_title = pyfiglet.figlet_format("Time Tracker", font="slant")
        self.timer = Timer("00:00:00.00", id="timer")
        self.time = self.timer.time

        yield Vertical(
            Header(show_clock=True, icon=""),
            Static(ascii_title, id="title"),
            self.timer,
            Static(
                f"Highscore: {self.highscore['score']} seconds",
                id="highscore",
            ),
            Static(str(self.time)),
            Footer(),
            id="app-wrapper"
        )

    def action_quit(self) -> None:
        """Quit the app."""
        
        self.data_manager.save_data()
        self.exit()

    def action_toggle_timer(self) -> None:
        """Toggle the timer."""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
        else:
            self.timer.start()
            self.is_running = True

    def action_reset_timer(self) -> None:
        """Reset the timer."""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
        self.timer.reset()

    def watch_is_running(self, status: bool) -> None:
        """Update the status display when the timer state changes."""
        pass

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")


if __name__ == "__main__":
    app = TrackerApp()
    app.run()