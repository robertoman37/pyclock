from datetime import datetime
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Header, Footer, Button, Static, Label, TabbedContent, TabPane, Digits

class Clock(Static):
    def compose(self) -> ComposeResult:
        yield Digits("", id="Clock")
    
    def on_mount(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)
    
    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")


class Timer(Static):
    def compose(self) -> ComposeResult:
        yield Label("Timer Time")


class PyClock(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with TabbedContent(initial="Clock"):
            with TabPane("Clock", id="Clock"):
                yield Clock()
            with TabPane("Timer", id="Timer"):
                yield Timer()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = PyClock()
    app.run()