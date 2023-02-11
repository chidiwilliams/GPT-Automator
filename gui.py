import sys
from threading import Thread

from PyQt6.QtCore import (QObject, Qt, QThread,
                          QTimer, QUrl, pyqtSignal, QModelIndex, QSize, QPoint,
                          QUrlQuery, QMetaObject, QEvent, QLocale)
from PyQt6.QtGui import (QAction, QCloseEvent, QDesktopServices, QIcon,
                         QKeySequence, QPixmap, QTextCursor, QValidator, QKeyEvent, QPainter, QColor)
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                             QDialogButtonBox, QFileDialog, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPlainTextEdit,
                             QProgressDialog, QPushButton, QVBoxLayout, QHBoxLayout, QMenu,
                             QWidget, QGroupBox, QToolBar, QTableWidget, QMenuBar, QFormLayout, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QListWidget, QListWidgetItem, QToolButton, QSizePolicy)
import sounddevice
import numpy as np
import whisper

import main
import transcriber
from transcriber import WhisperCpp


class MainWindow(QMainWindow):
    is_recording = False
    record_button: QPushButton
    queue = np.ndarray([], dtype=np.float32)

    def __init__(self):
        super().__init__(flags=Qt.WindowType.Window)

        self.setMinimumSize(450, 400)

        widget = QWidget(parent=self)

        self.record_button = QPushButton("Record", parent=self)
        self.record_button.clicked.connect(self.on_button_clicked)

        self.setCentralWidget(widget)

    def run_whisper(self):
        # model = WhisperCpp(model="/Users/chidiwilliams/Library/Caches/Buzz/ggml-model-whisper-base.bin")
        # model = WhisperCpp(model="/Users/chidiwilliams/Library/Caches/Buzz/ggml-base.en.bin")
        model = whisper.load_model("base")
        result = model.transcribe(audio=self.queue, language="en", task="transcribe")
        # result = model.transcribe(audio=self.queue, params=transcriber.whisper_cpp_params(language="en", word_level_timings=False))
        print(result["text"])
        main.main(result["text"])

    def start_recording(self):
        with sounddevice.InputStream(channels=1, samplerate=16000, callback=self.callback, dtype="float32"):
            while self.is_recording:
                pass

    def callback(self, in_data, frames, time, status):
        chunk: np.ndarray = in_data.ravel()
        self.queue = np.append(self.queue, chunk)

    def on_button_clicked(self):
        if self.is_recording:
            self.record_button.setText("Record")
            sounddevice.stop()
            self.is_recording = False

            self.thread = Thread(target=self.run_whisper)
            self.thread.start()
        else:
            self.thread = Thread(target=self.start_recording)
            self.thread.start()

            # self.stream = sounddevice.InputStream(channels=1, samplerate=16000, callback=self.callback)
            self.record_button.setText("Stop")
            self.is_recording = True


class Application(QApplication):
    window: MainWindow

    def __init__(self) -> None:
        super().__init__(sys.argv)

        self.window = MainWindow()
        self.window.show()


if __name__ == "__main__":
    app = Application()
    sys.exit(app.exec())
