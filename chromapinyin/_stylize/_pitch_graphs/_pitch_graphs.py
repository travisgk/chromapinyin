import os
import numpy as np
from PIL import Image
from chromapinyin._syllable._inflection import (
	TO_INFLECTION, INFLECTION_TO_SPOKEN_TONE, find_inflection_label
)
from chromapinyin._syllable._vowel_chars import (
	APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM
)
from chromapinyin._stylize._color_scheme import get_inflection_RGB
from chromapinyin._stylize._res_directories import get_pitch_graphs_dir

_prev_style_name = None
_thinned_templates = {}
_scale_image = None
_PITCH_GRAPH_PADDING_PX = 5
_PUNCTUATION_GRAPH_WIDTH_PX = 100
_inflection_to_graph_path = {}

def inflection_to_graph_path(inflection_num):
	return _inflection_to_graph_path[inflection_num]

def create_inflection_graphs(
	graph_style_name="simple",
	output_dir=get_pitch_graphs_dir(),
	fixed_width=False
):
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	_load_templates(graph_style_name)
	max_width = max([image.size[0] for image in _thinned_templates.values()])

	punctuation_graph_created = False
	for inflection_str, inflection in TO_INFLECTION.items():
		if inflection in [APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM,]:
			if not punctuation_graph_created:
				result = _scale_image.resize(
					(_PUNCTUATION_GRAPH_WIDTH_PX, _scale_image.size[1],),
					Image.NEAREST
				)
				output_path = f"{output_dir}/_punctuation.png"
				result.save(output_path)
				_inflection_to_graph_path[inflection] = output_path
				punctuation_graph_created = True
			continue

		spoken_tone = INFLECTION_TO_SPOKEN_TONE[inflection]
		rgb = get_inflection_RGB(inflection)
		graph = _make_color_copy(_thinned_templates[spoken_tone], rgb)
		graph_width = max_width if fixed_width else graph.size[0]
		result = _scale_image.resize(
			(graph_width + _PITCH_GRAPH_PADDING_PX * 2, graph.size[1],),
			Image.NEAREST
		)

		result.paste(
			graph, (int(result.size[0] / 2 - graph.size[0] / 2), 0,), graph
		)
		output_path = f"{output_dir}/_{inflection_str}.png"
		result.save(output_path)
		_inflection_to_graph_path[inflection] = output_path

def _load_templates(graph_style_name):
	if _prev_style_name and _prev_style_name == graph_style_name:
		# the <graph_style_name> is the same one used
		# to previously load graph template images,
		# so the images don't need to be loaded again.
		return

	global _thinned_templates, _scale_image
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