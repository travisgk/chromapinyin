# __init__.py
# ---
# this file imports functions to create a list of syllables,
# process a pinyin syllable,
# modify the color scheme,
# change element sizes,
# create new pitch graph components,
# modify the speed/looping behavior of all handwriting GIFs,
# and create a stylized chinese table.
#


from chromapinyin._syllable._vowel_chars import (
    get_tone_num,
    strip_tone_marker,
    place_tone_marker,
    is_pinyin_vowel,
)

import chromapinyin._stylize._color_scheme as color_scheme
from chromapinyin._stylize._table_css import (
    set_font_sizes,  # str
    set_hanzi_font_size,  # str
    set_hanzi_vertical_offset,  # str
    set_pinyin_font_size,  # str
    set_zhuyin_prefix_font_size,  # str
    set_zhuyin_root_font_size,  # str
    set_zhuyin_suffix_font_size,  # str
    set_ipa_font_size,  # str
    set_pitch_graph_height,  # str
    set_handwriting_height,  # str
)
from chromapinyin._stylize._graphics._pitch_graphs import (
    create_inflection_graphs,  # style_name, output_dir, fixed_width (bool)
)
from chromapinyin._stylize._graphics._handwriting_gifs import process_gifs
from chromapinyin._stylize._html_builder import create_stylized_sentence, generate_CSS
from chromapinyin._stylize._res_directories import get_output_dir
from chromapinyin._words._word_list import create_word_list

create_inflection_graphs(overwrite_images=False)
