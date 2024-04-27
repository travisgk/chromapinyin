__all__ = [
	"CHROMA_DIV_PUSH_LEFT",
	"CHROMA_DIV_PUSH_RIGHT",
	"CHROMA_DIV_PUSH_CENTER",
	"CHROMA_TD_ALIGN_CENTER",
	"CHROMA_TD_ALIGN_TOP",
	"CHROMA_TD_ALIGN_RIGHT",
	"CHROMA_TD_ALIGN_BOTTOM",
	"CHROMA_TD_ALIGN_LEFT",
	"CHROMA_TABLE",
	"CHROMA_TR",
	"CHROMA_TD",
	"CHROMA_TD_HANZI",
	"CHROMA_DIV_HANZI_CONTAINER",
	"CHROMA_HANZI_OFFSET",
	"CHROMA_TD_PINYIN",
	"CHROMA_TD_ZHUYIN",
	"CHROMA_DIV_ZHUYIN_CONTAINER",
	"CHROMA_NESTED_ZHUYIN",
	"CHROMA_ZHUYIN_PREFIX",
	"CHROMA_ZHUYIN_ROOT",
	"CHROMA_ZHUYIN_SUFFIX",
	"CHROMA_ZHUYIN_PREFIX_OFFSET",
	"CHROMA_ZHUYIN_SUFFIX_OFFSET",
	"CHROMA_VERTICAL_ZHUYIN",
	"CHROMA_APOSTROPHE_OFFSET",
	"CHROMA_TD_IPA",
	"CHROMA_TD_PITCH_GRAPH",
	"CATEGORY_TO_TD_STYLE",
]

_HANZI_FONT_SIZE = "64px"
_HANZI_VERTICAL_OFFSET = "-20%";
_PINYIN_FONT_SIZE = "13px"
_ZHUYIN_PREFIX_FONT_SIZE = "21px"
_ZHUYIN_ROOT_FONT_SIZE = "13px"
_ZHUYIN_SUFFIX_FONT_SIZE = "21px"
_IPA_FONT_SIZE = "13px"

CHROMA_DIV_PUSH_LEFT = {
	"class": "div.chroma-push-left",
	"style": (
		"margin-right: auto;",
	),
}

CHROMA_DIV_PUSH_RIGHT = {
	"class": "div.chroma-push-right",
	"style": (
		"margin-left: auto;",
	),
}

CHROMA_DIV_PUSH_CENTER = {
	"class": "div.chroma-push-center",
	"style": (
		"margin-left: auto;",
		"margin-right: auto;",
	),
}

CHROMA_TD_ALIGN_CENTER = {
	"class": "td.chroma-align-center",
	"style": (
		"text-align: center;",
		"vertical-align: center;",
	),
}

CHROMA_TD_ALIGN_TOP = {
	"class": "td.chroma-align-top",
	"style": (
		"text-align: center;",
		"vertical-align: top;",
	),
}

CHROMA_TD_ALIGN_RIGHT = {
	"class": "td.chroma-align-right",
	"style": (
		"text-align: right;",
		"vertical-align: center;",
	),
}

CHROMA_TD_ALIGN_BOTTOM = {
	"class": "td.chroma-align-bottom",
	"style": (
		"text-align: center;",
		"vertical-align: bottom;",
	),
}

CHROMA_TD_ALIGN_LEFT = {
	"class": "td.chroma-align-left",
	"style": (
		"text-align: left;",
		"vertical-align: center;",
	),
}

CHROMA_TABLE = {
	"class": "table.chroma",
	"style": (
		"border-collapse: collapse;",
		"border: 0;",
		"margin: 0;",
		"padding: 0;",
	),
}

CHROMA_TR = {
	"class": "tr.chroma",
	"style": (
		"margin: 0;",
		"padding: 0;",
	),
}

CHROMA_TD = {
	"class": "td.chroma",
	"style": (
		"margin: 0;",
		"padding: 0;",
	),
}

CHROMA_TD_HANZI = {
	"class": "td.chroma-hanzi",
	"style": (
		"margin: 0;",
		"padding: 1px;",
		f"font-size: {_HANZI_FONT_SIZE};",
	),
}

CHROMA_DIV_HANZI_CONTAINER = {
	"class": "div.chroma-hanzi-container",
	"style": (
		"display: block;",
		"overflow: hidden;",
		"position: relative;",
		f"height: {_HANZI_FONT_SIZE};",
	),
}

CHROMA_HANZI_OFFSET = {
	"class": "chroma-hanzi-offset",
	"style": (
		"display: block;",
		"position: relative;",
		f"top: {_HANZI_VERTICAL_OFFSET};",
	),
}

CHROMA_TD_PINYIN = {
	"class": "td.chroma-pinyin",
	"style": (
		"margin: 0;",
		"padding: 0;",
		f"font-size: {_PINYIN_FONT_SIZE};"
	),
}

CHROMA_TD_ZHUYIN = {
	"class": "td.chroma-zhuyin",
	"style": (
		"margin: 0;",
		"padding: 0;",
	),
}

CHROMA_DIV_ZHUYIN_CONTAINER = {
	"class": "div.chroma-zhuyin-container",
	"style": (
		"display: table;",
		"overflow: hidden;",
	),
}

CHROMA_NESTED_ZHUYIN = {
	"class": "chroma-nested-zhuyin",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"width: 5px;",
		"vertical-align: bottom;",
	),
}

CHROMA_ZHUYIN_PREFIX = {
	"class": "chroma-zhuyin-prefix",
	"style": (
		f"font-size: {_ZHUYIN_PREFIX_FONT_SIZE};",
	),
}

CHROMA_ZHUYIN_ROOT = {
	"class": "chroma-zhuyin-root",
	"style": (
		f"font-size: {_ZHUYIN_ROOT_FONT_SIZE};",
	),
}

CHROMA_ZHUYIN_SUFFIX = {
	"class": "chroma-zhuyin-suffix",
	"style": (
		f"font-size: {_ZHUYIN_SUFFIX_FONT_SIZE};",
	),
}

CHROMA_ZHUYIN_PREFIX_OFFSET = {
	"class": "chroma-zhuyin-prefix-offset",
	"style": (
		"display: block;",
		"position: relative;",
		"height: 5px;",
		"top: -4px;",
		"z-index: 3;"
	),
}

CHROMA_ZHUYIN_SUFFIX_OFFSET = {
	"class": "chroma-zhuyin-suffix-offset",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"position: relative;",
		"top: -2px;",
	),
}

CHROMA_VERTICAL_ZHUYIN = {
	"class": "chroma-vertical-zhuyin",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"display: flex;",
		"position: relative;",
		"text-orientation: upright;",
		"writing-mode: vertical-lr;",
		"white-space: nowrap;",
	),
}

CHROMA_APOSTROPHE_OFFSET = {
	"class": "chroma-apostrophe-offset",
	"style": (
		"margin: 0;",
		"padding: 0;",
		"position: relative;",
		"top: -2px;",
	),
}

CHROMA_TD_IPA = {
	"class": "td.chroma-ipa",
	"style": (
		"margin: 0;",
		"padding: 0;",
		f"font-size: {_IPA_FONT_SIZE};",
	),
}

CHROMA_TD_PITCH_GRAPH = {
	"class": "td.chroma-pitch-graph",
	"style": (
		"margin: 0;",
		"padding: 0;",
	),
}

CATEGORY_TO_TD_STYLE = {
	"hanzi": CHROMA_TD_HANZI,
	"pinyin": CHROMA_TD_PINYIN,
	"zhuyin": CHROMA_TD_ZHUYIN,
	"vertical_zhuyin": CHROMA_TD_ZHUYIN,
	"ipa": CHROMA_TD_IPA,
	"pitch_graph": CHROMA_TD_PITCH_GRAPH,
}