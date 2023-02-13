import os
import sys
import uuid
from threading import Thread
from typing import Optional

import numpy as np
import sounddevice
import soundfile
import queue
import tempfile
import whisper
from PyQt6.QtCore import (Qt)
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QSizePolicy,
                             QVBoxLayout, QLabel)

import main


def get_asset_path(path: str):
    return os.path.join(os.path.dirname(__file__), path)


RECORD_ICON_PATH = get_asset_path('assets/mic.svg')
STOP_ICON_PATH = get_asset_path('assets/stop.svg')


class MainWindow(QMainWindow):
    is_recording = False
    record_button: QPushButton
    ICON_LIGHT_THEME_BACKGROUND = '#333'
    ICON_DARK_THEME_BACKGROUND = '#DDD'
    recording_thread: Optional[Thread] = None
    transcription_thread: Optional[Thread] = None
    temp_file_path: Optional[str] = None
    queue = queue.Queue()

    def __init__(self):
        super().__init__(flags=Qt.WindowType.Window)

        self.samples_buffer = np.ndarray([], dtype=np.float32)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.setFixedSize(275, 90)
        self.setWindowTitle("GPT Automator")

        widget = QWidget(parent=self)

        layout = QVBoxLayout()

        self.record_icon = self.load_icon(RECORD_ICON_PATH)
        self.stop_icon = self.load_icon(STOP_ICON_PATH)

        self.record_button = QPushButton(self.load_icon(RECORD_ICON_PATH), "Record", parent=self)
        self.record_button.clicked.connect(self.on_button_clicked)
        self.record_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        window_color = self.palette().window().color()
        background_color = window_color.lighter(150) if self.is_dark_theme() else window_color.darker(150)
        self.record_button.setStyleSheet(
            "QPushButton { border-radius: 8px; background-color: %s; }" % background_color.name())

        self.transcription_label = QLabel("Click 'Record' to begin", parent=self)
        self.transcription_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.record_button)
        layout.addWidget(self.transcription_label)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def transcribe_recording(self):
        model = whisper.load_model("base")
        result = model.transcribe(audio=self.temp_file_path, language="en", task="transcribe")

        text = result["text"]
        print(f'Transcribed text: {text}')

        if text is None:
            self.transcription_label.setText('No text found. Please try again.')
        else:
            self.transcription_label.setText(f'"{text.strip()}"')

            try:
                # Run command execution
                main.main(result["text"])
            except Exception as e:
                print(f'Error executing command: {e}')
                self.transcription_label.setText(f'An error occurred: {str(e)}')

        self.record_button.setDisabled(False)

    def start_recording(self):
        device = sounddevice.query_devices(kind='input')

        self.temp_file_path = os.path.join(tempfile.gettempdir(), f'{uuid.uuid1()}.wav')
        print(f'Temporary recording path: {self.temp_file_path}')

        with soundfile.SoundFile(self.temp_file_path, mode='x', samplerate=int(device['default_samplerate']),
                                 channels=1) as file:
            with sounddevice.InputStream(channels=1, callback=self.callback, device=device['index'], dtype="float32"):
                while self.is_recording:
                    file.write(self.queue.get())

    def callback(self, in_data, frames, time, status):
        self.queue.put(in_data.copy())

    def on_button_clicked(self):
        if self.is_recording:
            self.record_button.setText("Record")
            self.record_button.setIcon(self.record_icon)
            self.is_recording = False

            self.transcription_label.setText('Transcribing...')
            self.record_button.setDisabled(True)

            self.transcription_thread = Thread(target=self.transcribe_recording)
            self.transcription_thread.start()
        else:
            # Reset samples buffer
            self.samples_buffer = np.ndarray([], dtype=np.float32)

            self.recording_thread = Thread(target=self.start_recording)
            self.recording_thread.start()

            self.transcription_label.setText('Listening...')

            self.record_button.setText("Stop")
            self.record_button.setIcon(self.stop_icon)
            self.is_recording = True

    def is_dark_theme(self):
        return self.palette().window().color().black() > 127

    def load_icon(self, file_path: str):
        background = self.ICON_DARK_THEME_BACKGROUND if self.is_dark_theme() else self.ICON_LIGHT_THEME_BACKGROUND
        return self.load_icon_with_color(file_path, background)

    @staticmethod
    def load_icon_with_color(file_path: str, color: str):
        """Adapted from https://stackoverflow.com/questions/15123544/change-the-color-of-an-svg-in-qt"""
        pixmap = QPixmap(file_path)
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), QColor(color))
        painter.end()
        return QIcon(pixmap)


class Application(QApplication):
    window: MainWindow

    def __init__(self) -> None:
        super().__init__(sys.argv)

        self.window = MainWindow()
        self.window.show()


if __name__ == "__main__":
    app = Application()
    sys.exit(app.exec())
