import ctypes
import datetime
import enum
import json
import logging
import multiprocessing
import os
import platform
import queue
import re
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass, field
from multiprocessing.connection import Connection
from random import randint
from threading import Thread
from typing import Any, List, Optional, Tuple, Union

import ffmpeg
import numpy as np
import sounddevice
import whisper
from PyQt6.QtCore import QObject, QProcess, pyqtSignal, pyqtSlot, QThread
from sounddevice import PortAudioError

# Catch exception from whisper.dll not getting loaded.
# TODO: Remove flag and try-except when issue with loading
# the DLL in some envs is fixed.
LOADED_WHISPER_DLL = False
try:
    import whisper_cpp

    LOADED_WHISPER_DLL = True
except ImportError:
    logging.exception('')


@dataclass
class Segment:
    start: int  # start time in ms
    end: int  # end time in ms
    text: str

def whisper_cpp_params(
        language: str, word_level_timings: bool,
        print_realtime=False, print_progress=False, ):
    params = whisper_cpp.whisper_full_default_params(
        whisper_cpp.WHISPER_SAMPLING_GREEDY)
    params.print_realtime = print_realtime
    params.print_progress = print_progress
    params.language = whisper_cpp.String(language.encode('utf-8'))
    params.translate = False
    params.max_len = ctypes.c_int(1)
    params.max_len = 1 if word_level_timings else 0
    params.token_timestamps = word_level_timings
    return params

class WhisperCpp:
    def __init__(self, model: str) -> None:
        self.ctx = whisper_cpp.whisper_init_from_file(model.encode('utf-8'))

    def transcribe(self, audio: Union[np.ndarray, str], params: Any):
        if isinstance(audio, str):
            audio = whisper.audio.load_audio(audio)

        logging.debug('Loaded audio with length = %s', len(audio))

        whisper_cpp_audio = audio.ctypes.data_as(
            ctypes.POINTER(ctypes.c_float))
        result = whisper_cpp.whisper_full(
            self.ctx, params, whisper_cpp_audio, len(audio))
        if result != 0:
            raise Exception(f'Error from whisper.cpp: {result}')

        segments: List[Segment] = []

        n_segments = whisper_cpp.whisper_full_n_segments((self.ctx))
        for i in range(n_segments):
            txt = whisper_cpp.whisper_full_get_segment_text((self.ctx), i)
            t0 = whisper_cpp.whisper_full_get_segment_t0((self.ctx), i)
            t1 = whisper_cpp.whisper_full_get_segment_t1((self.ctx), i)

            segments.append(
                Segment(start=t0 * 10,  # centisecond to ms
                        end=t1 * 10,  # centisecond to ms
                        text=txt.decode('utf-8')))

        return {
            'segments': segments,
            'text': ''.join([segment.text for segment in segments])}

    def __del__(self):
        whisper_cpp.whisper_free(self.ctx)
