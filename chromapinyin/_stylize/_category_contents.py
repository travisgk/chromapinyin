from ._table_css import *
from ._html_builder import *
from .color_scheme import get_inflection_color_style

def return_hanzi_contents(syllable, category, generate_css, vertical):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [CATEGORY_TO_TD_STYLE[category_name],]
	if vertical:
		td_styling_classes.append(return_td_align_style(alignment, vertical))
	td_styling = embed_styling(td_styling_classes, generate_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	# opens the <div> container element.
	div_styling_classes = [CHROMA_DIV_HANZI_CONTAINER,]
	if not vertical:
		div_styling_classes.append(return_div_h_align_style(alignment))
	div_styling = embed_styling(div_styling_classes, generate_css)
	result += HTML_line(f"<div {div_styling}>", 1)

	# opens and closes the <span> container element.
	color_css = get_inflection_color_style(syllable["inflection_num"])
	span_styling_classes = [color_css, CHROMA_HANZI_OFFSET,]
	span_styling = embed_styling(span_styling_classes, generate_css)
	hanzi = syllable["hanzi"]
	result += HTML_line(f"<span {span_styling}>{hanzi}</span>")

	# closes elements.
	result += HTML_line("</div>", -1)
	result += HTML_line("</td>", -1)

	return result

def return_pinyin_contents(
	syllable, category, generate_css, vertical, add_punct
):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [CATEGORY_TO_TD_STYLE[category_name],]
	td_styling_classes.append(return_td_align_style(alignment, vertical))
	td_styling = embed_styling(td_styling_classes, generate_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	# opens and closes the <span> container element.
	color_css = get_inflection_color_style(syllable["inflection_num"])
	span_styling = embed_styling([color_css,], generate_css)
	pinyin = syllable["pinyin"]
	result += HTML_line(f"<span {span_styling}>{pinyin}</span>" + add_punct)

	# closes elements.
	result += HTML_line("</td>", -1)

	return result

def return_zhuyin_contents(syllable, category, generate_css, vertical):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [CATEGORY_TO_TD_STYLE[category_name],]
	td_styling_classes.append(return_td_align_style(alignment, vertical))
	td_styling = embed_styling(td_styling_classes, generate_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	# opens and closes the <span> container element.
	span_line = ""
	color_css = get_inflection_color_style(syllable["inflection_num"])
	span_styling = embed_styling([color_css,], generate_css)
	span_line += f"<span {span_styling}>"

	prefix = syllable["zhuyin_prefix"]
	if len(prefix) > 0:
		span_styling = embed_styling([CHROMA_ZHUYIN_PREFIX,], generate_css)
		span_line += f"<span {span_styling}>{prefix}</span>"
	
	root = syllable["zhuyin_root"]
	span_styling = embed_styling([CHROMA_ZHUYIN_ROOT,], generate_css)
	span_line += f"<span {span_styling}>{root}</span>"

	suffix = syllable["zhuyin_suffix"]
	if len(suffix) > 0:
		span_styling = embed_styling([CHROMA_ZHUYIN_SUFFIX,], generate_css)
		span_line += f"<span {span_styling}>{suffix}</span>"
	
	span_line += "</span>"

	result += HTML_line(span_line)

	# closes elements.
	result += HTML_line("</td>", -1)

	return result

def return_vertical_zhuyin_contents(
	syllable, category, generate_css, vertical
):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [CATEGORY_TO_TD_STYLE[category_name],]
	if vertical:
		td_styling_classes.append(return_td_align_style(alignment, vertical))
	td_styling = embed_styling(td_styling_classes, generate_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	# opens the <div> container element.
	div_styling = embed_styling([CHROMA_DIV_ZHUYIN_CONTAINER,], generate_css)
	result += HTML_line(f"<div {div_styling}>", 1)

	# opens the nested <table> element.
	table_styling = embed_styling([CHROMA_TABLE,], generate_css)
	result += HTML_line(f"<table {table_styling}>", 1)

	# opens the nested <tr> and <td> elements.
	nested_styling = embed_styling([CHROMA_NESTED_ZHUYIN], generate_css)
	result += HTML_line(f"<tr {nested_styling}>", 1)

	# creates the spans for the prefix and root.
	result += HTML_line(f"<td {nested_styling}>", 1)
	
	color_css = get_inflection_color_style(syllable["inflection_num"])
	color_styling = embed_styling([color_css,], generate_css)
	result += HTML_line(f"<div {color_styling}>", 1)

	span_line = ""
	prefix = syllable["zhuyin_prefix"]
	if len(prefix) > 0:
		span_styling = embed_styling(
			[CHROMA_ZHUYIN_PREFIX, CHROMA_ZHUYIN_PREFIX_OFFSET,], generate_css
		)
		span_line += f"<span {span_styling}>{prefix}</span>"

	root = syllable["zhuyin_root"]
	span_styling = embed_styling(
		[CHROMA_ZHUYIN_ROOT, CHROMA_VERTICAL_ZHUYIN], generate_css
	)
	span_line += f"<span {span_styling}>{root}</span>"

	result += HTML_line(span_line)
	result += HTML_line("</div>", -1)
	result += HTML_line("</td>", -1)

	# creates the spans for the suffix.
	result += HTML_line(f"<td {nested_styling}>", 1)
	result += HTML_line(f"<div {color_styling}>", 1)

	span_line = ""
	suffix = syllable["zhuyin_suffix"]
	span_styling = embed_styling(
		[CHROMA_ZHUYIN_SUFFIX, CHROMA_ZHUYIN_SUFFIX_OFFSET,], generate_css
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

def return_ipa_contents(
	syllable, category, generate_css, vertical, add_punct
):
	category_is_tuple = isinstance(category, tuple)
	category_name = category[0] if category_is_tuple else category
	category_is_grouped = category_is_tuple and "grouped" in category
	alignment = syllable["alignment"] if category_is_grouped else "center"

	# opens the <td> element.
	td_styling_classes = [CATEGORY_TO_TD_STYLE[category_name],]
	td_styling_classes.append(return_td_align_style(alignment, vertical))
	td_styling = embed_styling(td_styling_classes, generate_css)
	result = HTML_line(f"<td {td_styling}>", 1)

	# opens and closes the <span> container element.
	color_css = get_inflection_color_style(syllable["inflection_num"])
	span_styling = embed_styling([color_css,], generate_css)
	ipa_root = syllable["ipa_root"]
	ipa_suffix = syllable["ipa_suffix"]
	ipa = ipa_root + ipa_suffix
	result += HTML_line(f"<span {span_styling}>{ipa}</span>" + add_punct)

	# closes elements.
	result += HTML_line("</td>", -1)

	return result