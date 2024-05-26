# chromapinyin._stylize._res_directories.py
# ---
# this file defines global variables that
# hold the directories to resources sourced by the produced HTML.
#

import os

_output_dir = "chromapinyin_output"
_output_res_dir = "_chroma_res"
_pitch_graphs_dir = "pitch_graphs"
_handwriting_dir = "handwriting"
_handwriting_gifs_dir = "images"


def get_output_dir():
    return _output_dir


def set_output_dir(_output_dir):
    global _output_res_dir
    _output_dir = _output_dir


def get_local_pitch_graphs_path():
    return os.path.join(_output_res_dir, _pitch_graphs_dir)


def get_local_handwriting_path():
    return os.path.join(_output_res_dir, _handwriting_dir)


def get_local_handwriting_gifs_path():
    return os.path.join(_output_res_dir, _handwriting_dir, _handwriting_gifs_dir)
