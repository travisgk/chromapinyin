# chromapinyin._stylize._res_directories.py
# ---
# this file defines global variables that
# hold the directories to resources sourced by the produced HTML.
#

import os

_output_dir = "_chroma_res"
_pitch_graphs_dir = "pitch_graphs"
_handwriting_dir = "handwriting"
_handwriting_gifs_dir = "images"


def get_output_dir():
    return _output_dir


def set_output_dir(output_dir):
    global _output_dir
    _output_dir = output_dir


def get_pitch_graphs_path():
    return os.path.join(_output_dir, _pitch_graphs_dir)


def set_pitch_graphs_dir(pitch_graphs_dir):
    global _pitch_graphs_dir
    _pitch_graphs_dir = pitch_graphs_dir


def get_handwriting_path():
    return os.path.join(_output_dir, _handwriting_dir)


def set_handwriting_dir(handwriting_dir):
    global _handwriting_dir
    _handwriting_dir = handwriting_dir


def get_handwriting_gifs_path():
    return os.path.join(_output_dir, _handwriting_dir, _handwriting_gifs_dir)


def set_handwriting_gifs_dir(gifs_dir):
    global _handwriting_gifs_dir
    _handwriting_gifs_dir = gifs_dir
