_pitch_graphs_dir = "_chroma_res"
_handwriting_dir = "_chroma_res/makemeahanzi"

def get_pitch_graphs_dir():
	return _pitch_graphs_dir

def set_pitch_graphs_dir(pitch_graphs_dir):
	global _pitch_graphs_dir
	_pitch_graphs_dir = pitch_graphs_dir

def get_handwriting_dir():
	return _handwriting_dir

def set_handwriting_dir(handwriting_dir):
	global _handwriting_dir
	_handwriting_dir = handwriting_dir