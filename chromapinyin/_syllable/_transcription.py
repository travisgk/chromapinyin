_TO_ZHUYIN_INITIALS = {
	"b": ("ㄅ", "p"),
	"p": ("ㄆ", "pʰ"),
	"m": ("ㄇ", "m"),
	"f": ("ㄈ", "f"),
	"d": ("ㄉ", "t"),
	"t": ("ㄊ", "tʰ"),
	"n": ("ㄋ", "n"),
	"l": ("ㄌ", "l"),
	"g": ("ㄍ", "k"),
	"k": ("ㄎ", "kʰ"),
	"h": ("ㄏ", "x"),
	"j": ("ㄐ", "tɕ"),
	"q": ("ㄑ", "tɕʰ"),
	"x": ("ㄒ", "ɕ"),
	"zh": ("ㄓ", "tʂ"),
	"ch": ("ㄔ", "tʂʰ"),
	"sh": ("ㄕ", "ʂ"),
	"r": ("ㄖ", "ʐ"),
	"z": ("ㄗ", "ts"),
	"c": ("ㄘ", "tsʰ"),
	"s": ("ㄙ", "s"),
}

_ZHUYIN_EXCEPTIONS = {
	"zhi": ("ㄓ", "tʂɚ"),
	"chi": ("ㄔ", "tʂʰɚ"),
	"shi": ("ㄕ", "ʂɚ"),
	"ju": ("ㄩ", "y"),
	"jue": ("ㄩㄝ", "y̯œ"),
	"juan": ("ㄩㄢ", "y̯ɛn"),
	"jun": ("ㄩㄣ", "yn"),
}

_TO_ZHUYIN_FINALS = {
	"a": ("ㄚ", "ɑ"),
	"o": ("ㄛ", "u̯ɔ"),
	"e": ("ㄜ", "ɯ̯ʌ"),
	"ai": ("ㄞ", "aɪ̯"),
	"ei": ("ㄟ", "eɪ̯"),
	"ao": ("ㄠ", "ɑʊ̯"),
	"ou": ("ㄡ", "ɤʊ̯"),
	"an": ("ㄢ", "an"),
	"en": ("ㄣ", "ən"),
	"ang": ("ㄤ", "ɑŋ"),
	"ong": ("ㄨㄥ", "u̯ʊŋ"),
	"eng": ("ㄥ", "əŋ"),
	"er": ("ㄦ", "ɑɻ"),
	
	"i": ("ㄧ", "i"),
	"ia": ("ㄧㄚ", "i̯ɑ"),
	"io": ("ㄧㄛ", "iu̯ɔ"),
	"ie": ("ㄧㄝ", "iɛ"),
	"iai": ("ㄧㄞ", "i̯aɪ̯"),
	"iao": ("ㄧㄠ", "i̯ɑʊ̯"),
	"iu": ("ㄧㄡ", "i̯ɤʊ̯"),
	"iou": ("ㄧㄡ", "i̯ɤʊ̯"),
	"ian": ("ㄧㄢ", "iɛn"),
	"in": ("ㄧㄣ", "in"),
	"iang": ("ㄧㄤ", "i̯ɑŋ"),
	"ing": ("ㄧㄥ", "iŋ"),

	"u": ("ㄨ", "u"),
	"ua": ("ㄨㄚ", "u̯ɑ"),
	"uo": ("ㄨㄛ", "u̯ɔ"),
	"uai": ("ㄨㄞ", "u̯aɪ̯"),
	"uei": ("ㄨㄟ", "u̯eɪ̯"),
	"ui": ("ㄨㄟ", "u̯eɪ̯"),
	"uan": ("ㄨㄢ", "u̯an"),
	"uen": ("ㄨㄣ", "u̯ən"),
	"un": ("ㄨㄣ", "u̯ən"),
	"uang": ("ㄨㄤ", "u̯ɑŋ"),
	"uong": ("ㄨㄥ", "u̯ʊŋ"),
	"ueng": ("ㄨㄥ", "u̯əŋ"),

	"ü": ("ㄩ", "y"),
	"üe": ("ㄩㄝ", "y̯œ"),
	"üan": ("ㄩㄢ", "y̯ɛn"),
	"ün": ("ㄩㄣ", "yn"),
	"iong": ("ㄩㄥ", "i̯ʊŋ"),
}

_PINYIN_TO_FINAL = {
	"a": "a",
	"o": "o",
	"e": "e",
	"ai": "ai",
	"ei": "ei",
	"ao": "ao",
	"ou": "ou",
	"an": "an",
	"en": "en",
	"ang": "ang",
	"ong": "ong",
	"eng": "eng",
	"er": "er",

	"yi": "i",
	"ya": "ia",
	"yo": "io",
	"ye": "ie",
	"yai": "iai",
	"yao": "iao",
	"you": "iou",
	"yan": "ian",
	"yin": "in",
	"yang": "iang",
	"ying": "ing",

	"wu": "u",
	"wa": "ua",
	"wo": "uo",
	"wai": "uai",
	"wei": "uei",
	"wan": "uan",
	"wen": "uen",
	"wang": "uang",
	"wong": "uong",
	"weng": "ueng",

	"yu": "ü",
	"yue": "üe",
	"yuan": "üan",
	"yun": "ün",
	"yong": "iong",
}

def pinyin_to_zhuyin_and_ipa(stripped_pinyin):
	exception_syllable = _ZHUYIN_EXCEPTIONS.get(stripped_pinyin)
	if exception_syllable:
		return exception_syllable

	double_initial = _TO_ZHUYIN_INITIALS.get(stripped_pinyin[:2])
	single_initial = _TO_ZHUYIN_INITIALS.get(stripped_pinyin[:1])
	initial = ("", "")
	ending = ("", "")
	if double_initial and len(stripped_pinyin) > 2:
		initial = double_initial
		#print(stripped_pinyin + "\t" + stripped_pinyin[2:])
		ending = _TO_ZHUYIN_FINALS.get(stripped_pinyin[2:])
	elif single_initial and len(stripped_pinyin) > 1:
		initial = single_initial
		#print(stripped_pinyin + "\t" + stripped_pinyin[1:])
		ending = _TO_ZHUYIN_FINALS.get(stripped_pinyin[1:])
	else:
		ending = _TO_ZHUYIN_FINALS[_PINYIN_TO_FINAL[stripped_pinyin]]

	#print(initial)
	#print(ending)
	zhuyin = initial[0] + ending[0]
	ipa = initial[1] + ending[1]
	return zhuyin, ipa