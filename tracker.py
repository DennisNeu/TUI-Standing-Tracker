from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Digits
from textual.reactive import Reactive
from textual.containers import Vertical
import pyfiglet


class TrackerApp(App):
    """A simple app to track time spent standing on a sit-stand desk."""

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
        self.status_display = Static("Timer is paused ⏸️", id="status")

        yield Vertical(
            Header(show_clock=True, icon=""),
            Static(ascii_title, id="title"),
            Digits("00:00:00", id="timer"),
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
            self.is_running = False
        else:
            self.is_running = True

    def action_reset_timer(self) -> None:
        """Reset the timer."""
        pass

    def watch_is_running(self, status: bool) -> None:
        """Update the status display when the timer state changes."""
        if status:
            self.status_display.update("Timer is running 🕒")
        else:
            self.status_display.update("Timer is paused ⏸️")


if __name__ == "__main__":
    app = TrackerApp()
    app.run()