from time import monotonic

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Digits
from textual.reactive import Reactive
from textual.containers import Vertical
import pyfiglet

class Timer(Digits):
    """A custom timer widget"""
    time = Reactive(0.0)
    total = Reactive(0.0)
    start_time = Reactive(monotonic)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update time to current."""
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        self.total = 0
        self.time = 0



class TrackerApp(App):
    """A simple app to track time spent standing on a sit-stand desk."""

    is_running = Reactive(False)
    start_time = Reactive(monotonic)

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
        self.status_display = Static("Timer is paused ⏸️", id="status")
        self.timer = Timer(id="timer")

        yield Vertical(
            Header(show_clock=True, icon=""),
            Static(ascii_title, id="title"),
            self.timer,
            self.status_display,
            Footer(),
            id="app-wrapper"
        )

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = (
            "tokyo-night" if self.theme == "textual-light" else "textual-light"
        )

    def action_toggle_timer(self) -> None:
        """Toggle the timer."""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
        else:
            self.timer.start()
            self.is_running = True

    def start_time(self) -> None:
        """Start the timer."""
        self.start_time = monotonic()
        self.update_timer()

    def update_time(self) -> None:
        """Method to update time to current."""
        self.time = self.total + (monotonic() - self.start_time) 

    def action_reset_timer(self) -> None:
        """Reset the timer."""
        self.timer.reset()

    def watch_is_running(self, status: bool) -> None:
        """Update the status display when the timer state changes."""
        if status:
            self.status_display.update("Timer is running 🕒")
        else:
            self.status_display.update("Timer is paused ⏸️")

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")


if __name__ == "__main__":
    app = TrackerApp()
    app.run()