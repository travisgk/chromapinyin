# chromapinyin._stylize._category_contents.py
# ---
# this file defines functions which return HTML of a <td> element
# containing syllable information for the given <category>.
#

from chromapinyin._syllable._inflection import (
	TO_INFLECTION, TO_INFLECTED_NEUTRAL, INFLECTION_TO_SPOKEN_TONE
)
from chromapinyin._syllable._vowel_chars import (
	NEUTRAL_TONE_NUM, PRIMARY_TONES, strip_tone_marker
)
from ._color_scheme import get_inflection_color_style
from ._table_css import *
from ._html_builder import *
from ._pitch_graphs._pitch_graphs import inflection_to_graph_path

_SIMPLIFY_SPOKEN_TONE = {
	TO_INFLECTION["punctuation"]: TO_INFLECTION["punctuation"],
	TO_INFLECTION["high"]: TO_INFLECTION["high"],
	TO_INFLECTION["rising"]: TO_INFLECTION["rising"],
	TO_INFLECTION["low"]: TO_INFLECTION["low"],
	TO_INFLECTION["falling"]: TO_INFLECTION["falling"],
	TO_INFLECTION["full_low"]: TO_INFLECTION["low"],
	TO_INFLECTION["half_falling"]: TO_INFLECTION["falling"],
	TO_INFLECTION["neutral_high"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["neutral_rising"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["neutral_low"]: TO_INFLECTION["neutral"],
	TO_INFLECTION["neutral_falling"]: TO_INFLECTION["neutral"],
}

def return_hanzi_contents(syllable, category, use_css, vertical):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [category_to_td_style(category_name),]
	if vertical:
		td_styling_classes.append(return_td_align_style(alignment, vertical))
	td_styling = embed_styling(td_styling_classes, use_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	# opens the <div> container element.
	div_styling_classes = [get_content_style("CHROMA_DIV_HANZI_CONTAINER"),]
	if not vertical:
		div_styling_classes.append(return_div_h_align_style(alignment))
	div_styling = embed_styling(div_styling_classes, use_css)
	result += HTML_line(f"<div {div_styling}>", 1)

	# opens and closes the <span> container element.
	color_css = get_inflection_color_style(syllable["inflection_num"])
	span_styling_classes = [color_css, get_content_style("CHROMA_HANZI_OFFSET"),]
	span_styling = embed_styling(span_styling_classes, use_css)
	hanzi = syllable["hanzi"]
	result += HTML_line(f"<span {span_styling}>{hanzi}</span>")

	# closes elements.
	result += HTML_line("</div>", -1)
	result += HTML_line("</td>", -1)

	return result

def return_pinyin_contents(syllable, category, use_css, vertical, add_punct):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [category_to_td_style(category_name),]
	td_styling_classes.append(return_td_align_style(alignment, vertical))
	td_styling = embed_styling(td_styling_classes, use_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	# opens and closes the <span> container element.
	color_css = get_inflection_color_style(syllable["inflection_num"])
	span_styling = embed_styling([color_css,], use_css)
	
	# determines the pinyin to display.
	pinyin = syllable["pinyin"]
	if category_is_tuple:
		if "number_tones" in category:
			tone_num = syllable["tone_num"]
			pinyin = strip_tone_marker(pinyin)
			if tone_num in PRIMARY_TONES:
				pinyin += str(tone_num)

		elif "no_tones" in category:
			pinyin = strip_tone_marker(pinyin)

	result += HTML_line(f"<span {span_styling}>{pinyin}</span>" + add_punct)
	result += HTML_line("</td>", -1)

	return result

def return_zhuyin_contents(
	syllable, category, use_css, vertical_table, vertical_zhuyin
):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [category_to_td_style(category_name),]
	if vertical_table:
		td_styling_classes.append(return_td_align_style(alignment, vertical_table))
	td_styling = embed_styling(td_styling_classes, use_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	# opens the <div> container element.
	div_styling_classes = [CHROMA_DIV_ZHUYIN_CONTAINER,]
	div_styling_classes.append(return_div_h_align_style(alignment))
	div_styling = embed_styling(div_styling_classes, use_css)
	result += HTML_line(f"<div {div_styling}>", 1)

	# opens the nested <table> element.
	table_styling = embed_styling([CHROMA_TABLE_NESTED,], use_css)
	result += HTML_line(f"<table {table_styling}>", 1)

	# opens the nested <tr> and <td> elements.
	nested_styling = embed_styling([CHROMA_NESTED_ZHUYIN], use_css)
	result += HTML_line(f"<tr {nested_styling}>", 1)
	result += HTML_line(f"<td {nested_styling}>", 1)
	
	# open the coloring span for the prefix and root.
	color_css = get_inflection_color_style(syllable["inflection_num"])
	color_styling = embed_styling([color_css,], use_css)
	result += HTML_line(f"<span {color_styling}>", 1)

	use_number_tones = False
	use_no_tones = False
	if category_is_tuple:
		if "number_tones" in category:
			use_number_tones = True
		elif "no_tones" in category:
			use_no_tones = True

	# creates the formatting for the prefix.
	span_line = ""
	prefix = syllable["zhuyin_prefix"]
	uses_prefix = False
	if len(prefix) > 0 and not use_number_tones and not use_no_tones:
		uses_prefix = True
		if vertical_zhuyin:
			offset_styling = embed_styling(
				[CHROMA_VERTICAL_ZHUYIN_PREFIX_OFFSET,], use_css
			)
			span_line += f"<span {offset_styling}>"
		else:
			inline_styling = embed_styling(
				[get_content_style("CHROMA_INLINE_ZHUYIN"),], use_css
			)
			span_line += f"<span {inline_styling}>"

		span_style_dicts = [
			get_content_style("CHROMA_ZHUYIN_PREFIX"),
			CHROMA_ZHUYIN_PREFIX_CONTAINER,
		]
		span_styling = embed_styling(span_style_dicts, use_css)
		span_line += f"<span {span_styling}>{prefix}</span>"

		if vertical_zhuyin:
			span_line += "</span>"

	# creates the formatting for the root.
	root = syllable["zhuyin_root"]
	style_dicts = [get_content_style("CHROMA_ZHUYIN_ROOT"),]
	if vertical_zhuyin and len(root) > 1:
		style_dicts.append(get_content_style("CHROMA_VERTICAL_ZHUYIN"))
	else:
		style_dicts.append(get_content_style("CHROMA_INLINE_ZHUYIN"))
	span_styling = embed_styling(style_dicts, use_css)
	span_line += f"<span {span_styling}>{root}</span>"
	if not vertical_zhuyin and uses_prefix:
		span_line += f"</span>"
	
	result += HTML_line(span_line)
	result += HTML_line("</span>", -1)
	result += HTML_line("</td>", -1)

	# creates the formatting for the suffix.
	result += HTML_line(f"<td {nested_styling}>", 1)
	div_styling = embed_styling([CHROMA_ZHUYIN_SUFFIX_OFFSET,], use_css)
	result += HTML_line(f"<div {div_styling}>", 1)

	span_line = ""
	suffix = syllable["zhuyin_suffix"]
	if category_is_tuple:
		if "number_tones" in category:
			tone_num = _SIMPLIFY_SPOKEN_TONE[syllable["spoken_tone_num"]]
			suffix = str(tone_num) if tone_num in PRIMARY_TONES else ""
		elif "no_tones" in category:
			suffix = ""

	span_styling = embed_styling(
		[
			color_css,
			get_content_style("CHROMA_ZHUYIN_SUFFIX"), 
			CHROMA_ZHUYIN_SUFFIX_CONTAINER,
		], use_css
	)
	span_line += f"<span {span_styling}>{suffix}</span>"

	result += HTML_line(span_line)
	result += HTML_line("</div>", -1)
	result += HTML_line("</td>", -1)

	# closes the rest of the elements.
	result += HTML_line("</tr>", -1)
	result += HTML_line("</table>", -1)
	result += HTML_line("</div>", -1)
	result += HTML_line("</td>", -1)

	return result

def return_ipa_contents(syllable, category, use_css, vertical, add_punct):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [category_to_td_style(category_name),]
	td_styling_classes.append(return_td_align_style(alignment, vertical))
	td_styling = embed_styling(td_styling_classes, use_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	# opens and closes the <span> container element.
	color_css = get_inflection_color_style(syllable["inflection_num"])
	span_styling = embed_styling([color_css,], use_css)
	root = syllable["ipa_root"]
	suffix = syllable["ipa_suffix"]
	if category_is_tuple:
		if "number_tones" in category:
			tone_num = _SIMPLIFY_SPOKEN_TONE[syllable["spoken_tone_num"]]
			suffix = str(tone_num) if tone_num in PRIMARY_TONES else ""
		elif "no_tones" in category:
			suffix = ""
	ipa = root + suffix

	result += HTML_line(f"<span {span_styling}>{ipa}</span>" + add_punct)
	result += HTML_line("</td>", -1)

	return result

def return_pitch_graph_contents(syllable, category, use_css, vertical):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [category_to_td_style(category_name),]
	td_styling_classes.append(return_td_align_style(alignment, vertical))
	td_styling = embed_styling(td_styling_classes, use_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	image_stylings = embed_styling(
		[get_content_style("CHROMA_IMG_PITCH_GRAPH",),], use_css
	)
	graph_path = inflection_to_graph_path(syllable["inflection_num"])
	result += HTML_line(f"<img {image_stylings} src=\"{graph_path}\" />")
	result += HTML_line("</td>", -1)

	return result