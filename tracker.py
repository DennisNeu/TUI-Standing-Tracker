from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.reactive import Reactive


class TrackerApp(App):
    """A simple app to track time spent standing on a sit-stand desk."""

    is_running = Reactive(False)

    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "start_timer", "Start Timer"),
        ("p", "pause_timer", "Pause Timer"),
        ("r", "reset_timer", "Reset Timer"),
        ("t", "toggle_dark", "Toggle Dark Mode")
    ]

    def compose(self) -> ComposeResult:
        """Generate layout for the app."""
        yield Header(show_clock=True, icon="🕒")
        yield Static("Time Tracker", id="title")
        self.status_display = Static(f"I display the status {self.is_running}", id="status")
        yield self.status_display
        yield Footer()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_start_timer(self) -> None:
        """Start the timer."""
        self.is_running = True
        # self.query_one("#status").update("Timer is running")

    def action_pause_timer(self) -> None:
        """Pause the timer."""
        self.is_running = False
        pass

    def action_reset_timer(self) -> None:
        """Reset the timer."""
        pass

    def watch_is_running(self, status: bool) -> None:
        """Update the status display when the timer state changes."""
        if status:
            self.status_display.update("Timer is running")
        else:
            self.status_display.update("Timer is paused")

if __name__ == "__main__":
    app = TrackerApp()
    app.run()