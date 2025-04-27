from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class TrackerApp(App):
    """A simple app to track time spent standing on a sit-stand desk."""

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
        yield Footer()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_start_timer(self) -> None:
        """Start the timer."""
        pass

    def action_pause_timer(self) -> None:
        """Pause the timer."""
        pass

    def action_reset_timer(self) -> None:
        """Reset the timer."""
        pass

if __name__ == "__main__":
    app = TrackerApp()
    app.run()