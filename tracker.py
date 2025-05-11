from timer import Timer
from data_manager import DataManager

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, Button
from textual.reactive import Reactive
from textual.containers import Vertical, Container

import pyfiglet


class TrackerApp(App):
    """A simple app to track time spent standing on a sit-stand desk."""

    def __init__(self) -> None:
        super().__init__()
        self.data_manager = DataManager("data.json")
        score_data = self.data_manager.get_last_score()
        self.highscore = score_data["score"]
        self.highscore_date = score_data["date"]
        self.total = 0.0

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
        ascii_title = pyfiglet.figlet_format("Stand Up!", font="slant")
        self.timer = Timer("00:00:00.00", id="timer")
        # TODO: fix f-string formatting
        self.score_display = Static(
                f"Highscore: {int(self.highscore) // 3600:02}:{(int(self.highscore) % 3600) // 60:02}:{int(self.highscore) % 60:02}",
                id="highscore",
            )
        self.total_display = Static(
                f"Total Time: {int(self.total) // 3600:02}:{(int(self.data_manager.total_time) % 3600) // 60:02}:{int(self.data_manager.total_time) % 60:02}",
                id="total",
            )

        yield Container(
            Header(show_clock=True, icon=""),
            Static(ascii_title, id="title"),
            self.timer,
            self.score_display,
            self.total_display,
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
            self.compare_time()
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

    def watch_highscore(self, highscore: float) -> None:
        """Called when the highscore attribute changes."""
        self.score_display.update(f"Highscore: {int(self.highscore) // 3600:02}:{(int(self.highscore) % 3600) // 60:02}:{int(self.highscore) % 60:02}")

    def compare_time(self) -> None:
        """Compare the current time with the highscore."""
        score = self.highscore

        if self.timer.time > score:
            self.highscore = self.timer.time
            self.data_manager.add_score(self.highscore)
            self.watch_highscore(self.highscore)
        else:
            return


if __name__ == "__main__":
    app = TrackerApp()
    app.run()
