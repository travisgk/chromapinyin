# chromapinyin._stylize._formatting_helper.py
# ---
# this file contains functions that help
# choose formatting for the output HTML
# and a function to maintain consistent
# tabulations while producing the HTML.
#

from ._table_css import (
	CHROMA_DIV_PUSH_LEFT,
	CHROMA_DIV_PUSH_RIGHT,
	CHROMA_DIV_PUSH_CENTER,
	CHROMA_TD_ALIGN_CENTER,
	CHROMA_TD_ALIGN_TOP,
	CHROMA_TD_ALIGN_RIGHT,
	CHROMA_TD_ALIGN_BOTTOM,
	CHROMA_TD_ALIGN_LEFT
)

_n_tabs = 0

def reset_tabulation():
	global _n_tabs
	_n_tabs = 0

def return_td_align_style(alignment, vertical):
	if alignment == "start":
		return CHROMA_TD_ALIGN_BOTTOM if vertical else CHROMA_TD_ALIGN_RIGHT
	elif alignment == "end":
		return CHROMA_TD_ALIGN_TOP if vertical else CHROMA_TD_ALIGN_LEFT
	else:
		return CHROMA_TD_ALIGN_CENTER # UNCERTAIN

def return_div_h_align_style(alignment):
	if alignment == "start":
		return CHROMA_DIV_PUSH_RIGHT
	elif alignment == "end":
		return CHROMA_DIV_PUSH_LEFT
	else:
		return CHROMA_DIV_PUSH_CENTER # UNCERTAIN

# returns the text that goes after an HTML tag declaration
# to indicate that tag's styling.
def embed_styling(style_dicts, uses_css):
	if uses_css:
		class_names = " ".join(
			[style_dict["class"].split(".")[-1] for style_dict in style_dicts]
		)
		return f"class=\"{class_names}\""

	results = []
	for style_dict in style_dicts:
		is_svg_filter = any(
			"svg" in style_line for style_line in style_dict["style"]
		)

		if is_svg_filter:
			for style_line in style_dict["style"]:
				clean_line = style_line.replace("\\", "")
				clean_line = clean_line.replace("url(\"", "url(&quot;")
				clean_line = clean_line.replace(
					"#color-filter\")", "#color-filter&quot;)"
				)
				clean_line = clean_line.replace("\"", "'")
				clean_line = clean_line.replace(": ", ":")
				results.append(" ".join(clean_line.split()))
		else:
			for style_line in style_dict["style"]:
				clean_line = style_line.replace("\"", "'")
				clean_line = clean_line.replace(": ", ":")
				results.append("".join(clean_line.split()))

	return (
		"style=\"" 
		+ " ".join(results)
		+ "\""
	)

# returns a string of HTML formatting with the current tabulation applied.
# <tab_inc> will increase/decrease the current tabulation after/before
# the given <HTML> line depending on 
# if <tab_inc> is positive/negative respectively.
def HTML_line(HTML, tab_inc=0, tab="    ", end="\n"):
	global _n_tabs
	if tab_inc < 0:
		_n_tabs += tab_inc
		result = tab * _n_tabs + HTML + end

	elif tab_inc > 0:
		result = tab * _n_tabs + HTML + end
		_n_tabs += tab_inc

	else:
		result = tab * _n_tabs + HTML + end
	return result

def colspan_str(colspan):
	return "" if colspan <= 1 else f"colspan=\"{colspan}\" "