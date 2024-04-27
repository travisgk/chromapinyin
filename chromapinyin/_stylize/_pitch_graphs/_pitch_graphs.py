import os
import numpy as np
from PIL import Image
from chromapinyin._syllable._inflection import (
	TO_INFLECTION, INFLECTION_TO_SPOKEN_TONE, find_inflection_label
)
from chromapinyin._syllable._vowel_chars import (
	APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM
)
from chromapinyin._stylize.color_scheme import get_inflection_RGB

_prev_style_name = None
_thinned_templates = {}
_scale_image = None

def save_inflection_graphs(output_dir="_chroma_res", graph_style_name="simple"):
	global _thinned_templates
	_load_templates(graph_style_name)

	for inflection_str, inflection in TO_INFLECTION.items():
		if inflection in [APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM,]:
			continue

		spoken_tone = INFLECTION_TO_SPOKEN_TONE[inflection]
		rgb = get_inflection_RGB(inflection)
		graph = _make_color_copy(_thinned_templates[spoken_tone], rgb)

		graph.save(f"example_{inflection_str}.png")

def _load_templates(graph_style_name):
	# if the <graph_style_name> is the same one used
	# to previously load graph template images,
	# then the images don't need to be loaded again.
	global _prev_style_name
	if _prev_style_name and _prev_style_name == graph_style_name:
		return

	global _thinned_templates
	main_dir = os.path.dirname(os.path.abspath(__file__))
	style_dir = os.path.join(main_dir, f"_{graph_style_name}")
	template_inflections = set(INFLECTION_TO_SPOKEN_TONE.values())

	_thinned_templates = {
		template_inflection : _load_thinned_graph(
			os.path.join(
				style_dir,
				f"_{find_inflection_label(template_inflection)}.png"
			)
		) for template_inflection in template_inflections
		if template_inflection != PUNCTUATION_TONE_NUM
	}
	_scale_image = Image.open(os.path.join(style_dir, "_scale.png"))
	_scale_image = _scale_image.convert('RGBA')

def _load_thinned_graph(image_path):
	image = Image.open(image_path)
	image = image.convert('RGBA')
	height = image.size[1]
	left_x = _find_first_opaque_column(image, going_right=True)
	right_x = _find_first_opaque_column(image, going_right=False)
	return image.crop((left_x, 0, right_x, height))

def _find_first_opaque_column(image, going_right):
	width = image.size[0]
	span_x = (1 if going_right else -1) * width // 5
	result_x = _column_search(
		image, 0 if going_right else width - 1, span_x
	)
	if not going_right:
		result_x += 1
	return result_x

def _column_search(image, start_x, span_x):
	height = image.size[1]
	end_x = start_x + span_x
	for y in range(height - 1, -1, -1):
		if image.getpixel((end_x, y))[3] > 0:
			if abs(span_x) == 1:
				return end_x
			else:
				return _column_search(image, start_x, span_x // 2)
	return _column_search(image, start_x + span_x, span_x)

def _make_color_copy(image, color):
	data = np.array(image)
	new_color = np.array(color + (255,), dtype=np.uint8)
	alpha_strengths = data[..., 3:] / 255.0
	data = new_color * alpha_strengths
	new_image = Image.fromarray(data.astype(np.uint8))
	return new_image;

def maineee():
	image = _load_thinned_chart("_falling.png")
	image = _make_color_copy(image, (100, 0, 100,))
	image.save("new_example.png")
