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
from PyQt6.QtWidgets import (  # type: ignore
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from video_subtitles.run import run
from video_subtitles.say import say
from video_subtitles.settings import Settings
from video_subtitles.util import MODELS

settings = Settings()


def open_folder(path):
    """Opens a folder in the OS."""
    if platform.system() == "Windows":
        os.startfile(path)  # pylint: disable=no-member
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])  # pylint: disable=consider-using-with
    else:
        subprocess.Popen(["xdg-open", path])  # pylint: disable=consider-using-with


class MainWidget(QMainWindow):  # pylint: disable=too-many-instance-attributes
    """Main widget."""

    def __init__(self, on_drop_callback):
        super().__init__()
        self.setWindowTitle("Video Subtitle Generator")
        self.resize(720, 480)
        self.setAcceptDrops(True)

        deepl_api_key = settings.deepl_key()

        # Creating a QWidget instance
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Creating a QVBoxLayout instance and set it as the layout for central_widget
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create a QWidget for the header pane
        header_pane = QWidget()
        header_layout = QVBoxLayout()
        header_pane.setLayout(header_layout)

        # Add the deepl api key label and input field to the header pane
        deepl_layout = QHBoxLayout()
        self.deepl_label = QLabel(self)
        self.deepl_label.setText("DeepL API Key:")
        self.deepl_input = QLineEdit(self)
        self.deepl_input.setMaxLength(80)  # set maximum length to 80 characters
        self.deepl_input.setText(deepl_api_key)  # set the input field to the api key
        deepl_layout.addWidget(self.deepl_label)
        deepl_layout.addWidget(self.deepl_input)
        deepl_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        model_layout = QHBoxLayout()
        self.model_label = QLabel(self)
        self.model_label.setText("Model:")
        self.model_select = QComboBox(self)
        self.model_select.addItems(MODELS.keys())
        self.model_select.setCurrentText(settings.model())
        model_layout.addWidget(self.model_label)
        model_layout.addWidget(self.model_select)
        model_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        header_layout.addLayout(deepl_layout)
        header_layout.addLayout(model_layout)

        # Add translation output label and text field
        output_layout = QHBoxLayout()
        self.output_label = QLabel(self)
        self.output_label.setText("Translation Outputs:")
        self.output_text = QLineEdit(self)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_text)
        output_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        header_layout.addLayout(output_layout)

        # Add a label to the window on top of everything else
        self.label = QLabel(self)
        self.label.setText("Drag and Drop Video File Here")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Add the header pane and label widget to the main layout
        main_layout.addWidget(header_pane)
        main_layout.addWidget(self.label)

        # Setting the alignment of the header pane to the top
        main_layout.setAlignment(header_pane, QtCore.Qt.AlignmentFlag.AlignTop)

        self.on_drop_callback = on_drop_callback

    def dragEnterEvent(self, event):
        """Drag and drop handler."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def save_settings(self) -> None:
        """Save the settings."""
        deepl_api_key = self.deepl_input.text().strip()  # get api key from input field
        settings.set_deepl_key(deepl_api_key)  # write api key to settings
        model = self.model_select.currentText().strip()
        settings.set_model(model)
        settings.save()  # save settings to file

    def dropEvent(self, event):
        """Drag and drop handler."""
        self.save_settings()
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        deepl_api_key = self.deepl_input.text().strip()  # get api key from input field
        model = self.model_select.currentText().strip()
        for f in files:
            self.on_drop_callback(f, deepl_api_key, model)  # pass api key to callback


def run_gui() -> None:
    """Runs the gui."""
    app = QApplication(sys.argv)

    def callback(videofile: str, deepl_api_key: str | None, model: str):
        # path, _ = os.path.splitext(videofile)
        # os.makedirs(path, exist_ok=True)
        # open_folder(path)
        if not deepl_api_key:
            deepl_api_key = None

        # Open folder in the OS
        def _generate_subtitles(videofile, deeply_api_key, model):
            # perform the actual work here
            os.chdir(os.path.dirname(videofile))
            videofile = os.path.basename(videofile)
            try:
                out = run(
                    file=videofile,
                    deepl_api_key=deeply_api_key,
                    out_languages=["en", "zh", "it", "es", "fr"],
                    model=model,
                )
            except Exception as e:  # pylint: disable=broad-except
                print(e)
                say("Error: " + str(e))
                return
            open_folder(out)
            print("Generating subtitles for", videofile)
            voicename = os.path.basename(videofile).split(".")[0].replace("_", " ")
            say(f"Attention: {voicename} has completed subtitle generation")

        Thread(
            target=_generate_subtitles,
            args=(videofile, deepl_api_key, model),
            daemon=True,
        ).start()

    gui = MainWidget(callback)
    gui.show()
    sys.exit(app.exec())
