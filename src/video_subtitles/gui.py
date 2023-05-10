"""
Gui for the video_subtitles package
"""

# pylint: disable=no-name-in-module,c-extension-no-member,invalid-name

import os
import platform
import subprocess
import sys
from threading import Thread

from PyQt6 import QtCore  # type: ignore
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow  # type: ignore

from video_subtitles.run import run
from video_subtitles.say import say


def open_folder(path):
    """Opens a folder in the OS."""
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])  # pylint: disable=consider-using-with
    else:
        subprocess.Popen(["xdg-open", path])  # pylint: disable=consider-using-with


class MainWidget(QMainWindow):
    """Main widget."""

    def __init__(self, on_drop_callback):
        super().__init__()
        self.setWindowTitle("Video Subtitle Generator")
        self.resize(720, 480)
        self.setAcceptDrops(True)
        # Add a label to the window on top of everythign elese
        self.label = QLabel(self)
        # Adjust label so it is centered
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setText("    Drag and Drop Video File Here")
        self.label.adjustSize()
        self.on_drop_callback = on_drop_callback

    def dragEnterEvent(self, event):
        """Drag and drop handler."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Drag and drop handler."""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.on_drop_callback(f)


def run_gui() -> None:
    """Runs the gui."""
    app = QApplication(sys.argv)

    def callback(videofile):
        # path, _ = os.path.splitext(videofile)
        # os.makedirs(path, exist_ok=True)
        # open_folder(path)

        # Open folder in the OS
        def _generate_subtitles(videofile):
            # perform the actual work here
            os.chdir(os.path.dirname(videofile))
            videofile = os.path.basename(videofile)
            try:
                out = run(
                    file=videofile,
                    deepl_api_key=None,
                    out_languages=["en", "zh", "it", "es", "fr"],
                    model="large",
                )
            except Exception as e:  # pylint: disable=broad-except
                print(e)
                say("Error: " + str(e))
                return
            open_folder(out)
            print("Generating subtitles for", videofile)
            voicename = os.path.basename(videofile).split(".")[0].replace("_", " ")
            say(f"Attention: {voicename} has completed subtitle generation")

        Thread(target=_generate_subtitles, args=(videofile,), daemon=True).start()

    gui = MainWidget(callback)
    gui.show()
    sys.exit(app.exec())
