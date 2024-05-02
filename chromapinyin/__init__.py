from chromapinyin._words._word_list import create_word_list
from chromapinyin._syllable._vowel_chars import (
	get_tone_num, strip_tone_marker, place_tone_marker, is_pinyin_vowel
)
from chromapinyin._stylize._stylize import create_stylized_sentence, generate_CSS
import chromapinyin._stylize._color_scheme as color_scheme
from chromapinyin._stylize._table_css import (
	set_font_sizes, # str
	set_hanzi_font_size, # str
	set_hanzi_vertical_offset, # str
	set_pinyin_font_size, # str
	set_zhuyin_prefix_font_size, # str
	set_zhuyin_root_font_size, # str
	set_zhuyin_suffix_font_size, # str
	set_ipa_font_size, # str
	set_pitch_graph_height, # str
)
from chromapinyin._stylize._pitch_graphs._pitch_graphs import (
	create_inflection_graphs # graph_style_name, output_dir, fixed_width (bool)
)
from chromapinyin._stylize._handwriting_gifs import process_gifs

create_inflection_graphs(overwrite_images=False)