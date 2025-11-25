# standard

# framework
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import CenterMiddle


# user-defined
from widgets.home_nav_widget import HomeNavContainer


class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        with CenterMiddle():
            yield HomeNavContainer()

    def action_go_inventory(self):
        pass

    def action_go_excess(self):
        pass

    def action_go_reports(self):
        pass

    def action_go_quit(self):
        pass
