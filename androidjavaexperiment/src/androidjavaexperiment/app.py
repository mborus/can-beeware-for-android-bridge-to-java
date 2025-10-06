"""
Android Java Experiment using Beeware
"""

import toga
from toga.style.pack import COLUMN, ROW

def _make_counter():
    # Import Chaquopy bridge lazily to ensure Android classloader is ready.
    from java import jclass  # Chaquopy bridge
    AutoCounter = jclass("org.beeware.android.AutoCounter")
    return AutoCounter()

class AndroidJavaExperiment(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()

        button = toga.Button(
            "Click to count!",
            on_press=self.say_hello,
            margin=5,
        )
        main_box.add(button)

        self.main_window = toga.MainWindow(title="version 0.0.1")
        self.main_window.content = main_box
        self.main_window.show()

        self.counter = _make_counter()


    async def say_hello(self, widget):
        # Read the current value from the Java counter, which auto-increments.
        value = self.counter.read()

        await self.main_window.dialog(
            toga.InfoDialog(
                "Counter",
                f"I counted {value}!",
            )
        )

def main():
    return AndroidJavaExperiment()
