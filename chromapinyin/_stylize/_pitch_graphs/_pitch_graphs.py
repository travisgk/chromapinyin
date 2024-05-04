# chromapinyin._stylize._pitch_graphs.py
# ---
# this file contains functions which create pitch graph components
# that will be sourced by the produced HTML.
#

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
from chromapinyin._stylize._res_directories import get_pitch_graphs_path

_prev_style_name = None
_thinned_templates = {}
_scale_image = None
_GRAPH_PADDING_PX = 2
_PUNCTUATION_GRAPH_WIDTH_PX = 100
_punctuation_graph_path = None
_inflection_to_graph_path = {}

# returns a path to the pitch graph component image
# for the given inflection and alignment ("left", "center", "right").
def inflection_to_graph_path(inflection_num, alignment):
	if inflection_num in [APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM,]:
		return _punctuation_graph_path
	return _inflection_to_graph_path[inflection_num][alignment]

# saves pitch graph components (images) that the produced HTML will use.
# - <graph_style_name> will select a directory under 
#   chromapinyin/_stylize/_pitch_graphs/_<graph_style_name>
# - <output_dir> is the directory where the created components will be saved.
# - <fixed_width> being True will make each saved image the exact same size.
#   this will align the line component inside its respective image accordingly.
# - <overwrite_images> being False will preserve any existing graph components.
def create_inflection_graphs(
	graph_style_name="fancy",
	output_dir=get_pitch_graphs_path(),
	fixed_width=False,
	overwrite_images=True
):
	global _inflection_to_graph_path, _punctuation_graph_path

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	_load_templates(graph_style_name)
	max_width = max([image.size[0] for image in _thinned_templates.values()])

	punctuation_graph_created = False
	for inflection_str, inflection in TO_INFLECTION.items():
		# creates a graph image for a punctuation mark.
		if inflection in [APOSTROPHE_TONE_NUM, PUNCTUATION_TONE_NUM,]:
			if not punctuation_graph_created:
				output_path = f"{output_dir}/_punctuation.png"
				_punctuation_graph_path = output_path
				punctuation_graph_created = True

				if not overwrite_images and os.path.exists(output_path):
					continue

				graph_width = (
					max_width if fixed_width else _PUNCTUATION_GRAPH_WIDTH_PX
				)
				scale_img_size = (graph_width, _scale_image.size[1],)
				result = _scale_image.resize(scale_img_size, Image.NEAREST)
				result.save(output_path)
			continue

		# creates pitch graph images for the <inflection>.
		spoken_tone = INFLECTION_TO_SPOKEN_TONE[inflection]
		rgb = get_inflection_RGB(inflection)
		graph = _make_color_copy(_thinned_templates[spoken_tone], rgb)
		graph_width = max_width if fixed_width else graph.size[0]
		stretched_scale = _scale_image.resize(
			(graph_width + _GRAPH_PADDING_PX * 2, graph.size[1],),
			Image.NEAREST
		)

		if not _inflection_to_graph_path.get(inflection):
			_inflection_to_graph_path[inflection] = {}

		if fixed_width:
			# aligns the graph line component on the stretched grid
			# and saves its image accordingly.
			for i, align in enumerate(["left", "center", "right",]):
				output_path = f"{output_dir}/_{inflection_str}_{align}.png"
				_inflection_to_graph_path[inflection][align] = output_path
				if not overwrite_images and os.path.exists(output_path):
					continue

				result = stretched_scale.copy()
				if i == 0:
					offset_x = _GRAPH_PADDING_PX
				elif i == 1:
					offset_x = int(result.size[0] / 2 - graph.size[0] / 2)
				else:
					offset_x = result.size[0] - graph.size[0] - _GRAPH_PADDING_PX

				result.paste(graph, (offset_x, 0,), graph)
				result.save(output_path)
		
		else:
			# the graph component doesn't need to be aligned on the grid,
			# so the same image is saved under each alignment image name.
			offset_x = int(stretched_scale.size[0] / 2 - graph.size[0] / 2)
			stretched_scale.paste(graph, (offset_x, 0,), graph)
			for align in ["left", "center", "right",]:
				output_path = f"{output_dir}/_{inflection_str}_{align}.png"
				_inflection_to_graph_path[inflection][align] = output_path
				if not overwrite_images and os.path.exists(output_path):
					continue

				stretched_scale.save(output_path)

# loads template image components 
# from the directory chromapinyin/_stylize/_pitch_graphs/_<graph_style_name>
# to the file's global dictionaries <_inflection_to_graph_path>.
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

	# PIL is used to load images from the style directory.
	_thinned_templates = {
		template_inflection : _load_thinned_graph(
			os.path.join(
				style_dir,
				f"_{find_inflection_label(template_inflection)}.png"
			)
		) for template_inflection in template_inflections
		if template_inflection != PUNCTUATION_TONE_NUM
	}

	# the pitch scale image is loaded.
	_scale_image = Image.open(os.path.join(style_dir, "_scale.png"))
	_scale_image = _scale_image.convert('RGBA')

# returns an image loaded from the given <image_path> and cropped horizontally
# so that any entirely transparent columns are absent.
def _load_thinned_graph(image_path):
	image = Image.open(image_path)
	image = image.convert('RGBA')
	height = image.size[1]
	left_x = _find_first_opaque_column(image, going_right=True)
	right_x = _find_first_opaque_column(image, going_right=False)
	return image.crop((left_x, 0, right_x, height))

# returns the X-coordinate of the first column of pixels that isn't entirely
# transparent while moving across the image either left or right.
def _find_first_opaque_column(image, going_right):
	width = image.size[0]
	span_x = (1 if going_right else -1) * width // 5
	result_x = _column_search(
		image, 0 if going_right else width - 1, span_x
	)
	if not going_right:
		result_x += 1
	return result_x

# returns the X-coordinate of the first column of pixels that isn't entirely
# transparent while moving across the image using recursion.
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

# returns a copy of the given <image> with all of its pixels
# changed to the given <color> while maintaining the original alpha channel.
def _make_color_copy(image, color):
	data = np.array(image)
	new_color = np.array(color + (255,), dtype=np.uint8)
	alpha_strengths = data[..., 3:] / 255.0
	data = new_color * alpha_strengths
	new_image = Image.fromarray(data.astype(np.uint8))
	return new_image;