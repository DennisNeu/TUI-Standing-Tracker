"""A simple app to track time spent standing on a sit-stand desk."""
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container

import pyfiglet

from timer import Timer
from data_manager import DataManager
from highscore_screen import HighscoreScreen


class TrackerApp(App):
    """A simple app to track time spent standing on a sit-stand desk."""

    def __init__(self) -> None:
        super().__init__()
        self.data_manager = DataManager("data.json")
        self.highscore = self.data_manager.get_highscore()
        self.total = self.data_manager.total_time
        self.time_when_last_total = 0.0
        self.timer_running = False

    CSS_PATH = "style.tcss"

    SCREENS = {"highscore": HighscoreScreen}

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "toggle_timer", "Toggle Timer"),
        ("r", "reset_timer", "Reset Timer"),
        ("h", "show_screen('highscore')", "Highscore"),
    ]

    def on_mount(self) -> None:
        """Event handler called when the app is mounted."""
        self.title = ""
        self.theme = "tokyo-night"

    def compose(self) -> ComposeResult:
        """Generate layout for the app."""
        ascii_title = pyfiglet.figlet_format("Stand Up!", font="slant")
        self.timer = Timer("00:00:00.00", id="timer")
        #  TODO: fix f-string formatting
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
        self.compare_time()
        self.data_manager.add_total_time(self.timer.time - self.time_when_last_total)
        self.data_manager.save_data()
        self.exit()

    def action_toggle_timer(self) -> None:
        """Toggle the timer."""
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.compare_time()
            self.calculate_total_time()
        else:
            self.timer.start()
            self.timer_running = True

    def action_reset_timer(self) -> None:
        """Reset the timer."""
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
        self.timer.reset()
        self.time_when_last_total = 0.01

    def action_show_screen(self, screen_name: str) -> None:
        """Show a screen."""
        if screen_name == "highscore":
            self.push_screen(HighscoreScreen(self.data_manager))
        else:
            return
        
    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def watch_highscore(self, highscore: float) -> None:
        """Called when the highscore attribute changes."""
        self.score_display.update(f"Highscore: {int(self.highscore) // 3600:02}:{(int(self.highscore) % 3600) // 60:02}:{int(self.highscore) % 60:02}")


    # TODO: function does more than just one thing, should be split up
    def compare_time(self) -> None:
        """Compare the current time with the highscore."""
        if self.timer.time > self.highscore:
            self.highscore = self.timer.time
            self.data_manager.add_score(self.highscore)
            self.watch_highscore(self.highscore)
        else:
            return

    def calculate_total_time(self) -> None:
        """Calculate the total time spent standing."""

        self.data_manager.add_total_time(self.timer.time - self.time_when_last_total)
        self.total = self.data_manager.get_total_time()
        self.total_display.update(
            f"Total Time: {int(self.total) // 3600:02}:{(int(self.total) % 3600) // 60:02}:{int(self.total) % 60:02}"
        )
        self.data_manager.save_data()
        self.time_when_last_total = self.timer.time


if __name__ == "__main__":
    app = TrackerApp()
    app.run()
