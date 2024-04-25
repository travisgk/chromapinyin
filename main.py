import chromapinyin

def main():
	'''sample_list = "shén me shí hòu".split()
	for syllable in sample_list:
		tone_num = chromapinyin.get_tone_num(syllable)
		stripped = chromapinyin.strip_tone_marker(syllable)
		print(chromapinyin.place_tone_marker(stripped, tone_num), end=" ")
	print("\n")

	hanzi = "我比你小。"
	pinyin = "wǒ bǐ nǐ xiǎo."
	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	html, css = chromapinyin.create_stylized_sentence(
		syllables, 
		[("pinyin", "merge_punctuation"), "hanzi_with_zhuyin"], 
		generate_css=False, 
		exclude_punctuation=True
	)'''

	phrases = [
		#{"hanzi": "你好吗？" 			, "pinyin": "nǐhǎo ma?"},
		#{"hanzi": "早上好"				, "pinyin": "zǎoshang hǎo."},
		#{"hanzi": "晚上好"				, "pinyin": "wǎnshàng hǎo."},
		#{"hanzi": "晚安"					, "pinyin": "wǎn'ān."},
		#{"hanzi": "不太好"				, "pinyin": "bù tài hǎo."},
		#{"hanzi": "你叫什么名字？"		, "pinyin": "nǐ jiào shénme míngzi?"},
		#{"hanzi": "你多大？"				, "pinyin": "nǐ duōdà?"},
		#{"hanzi": "你来自哪里？"			, "pinyin": "nǐ láizì nǎli?"},
		#{"hanzi": "我来自中国"			, "pinyin": "wǒ láizì zhōngguó."},
		#{"hanzi": "你是哪国人？"			, "pinyin": "nǐ shì nǎ guó rén?"},
		#{"hanzi": "我是中国人"			, "pinyin": "wǒ shì zhōngguó rén."},
		#{"hanzi": "很高兴认识你"			, "pinyin": "hěn gāoxìng rènshi nǐ."},
		#{"hanzi": "不用谢"				, "pinyin": "bù yòng xiè."},
		#{"hanzi": "不好意思"				, "pinyin": "bù hǎoyìsi."},
		#{"hanzi": "对不起"				, "pinyin": "duìbuqǐ."},
		{"hanzi": "对不起。 我不会说中文。", "pinyin": "duìbùqǐ. wǒ bù huì shuō zhōngwén."}
	]

	phrase = {"hanzi": "长安。", "pinyin": "cháng'ān."}
	syllables = chromapinyin.create_syllable_list(
		phrase["hanzi"], phrase["pinyin"]
	)
	html, css = chromapinyin.create_stylized_sentence(
		syllables, 
		[
			["hanzi", "ipa"], 
			[("pinyin", "merge_punctuation",),],
		], 
		generate_css=False,
		vertical=True
	)
	print(html)
	print("\n<br>\n<br>")

	'''html, css = chromapinyin.create_stylized_sentence(
		syllables, 
		[
			["hanzi", "ipa",], 
			[("pinyin", "merge_punctuation",),],
		], 
		generate_css=True,
		vertical=False
	)
	print(html)

	
	phrase = {"hanzi": "很高兴认识你。", "pinyin": "hěn gāoxìng rènshi nǐ."}
	syllables = chromapinyin.create_syllable_list(
		phrase["hanzi"], phrase["pinyin"]
	)
	html, css = chromapinyin.create_stylized_sentence(
		syllables, 
		[
			["hanzi",],
			["zhuyin",],
		],
		generate_css=True,
		vertical=True
	)
	print(html)
	print("<br>\n<br>")

	phrase = {"hanzi": "我也很好。", "pinyin": "wǒ yě hěn hǎo."}
	syllables = chromapinyin.create_syllable_list(
		phrase["hanzi"], phrase["pinyin"]
	)
	html, css = chromapinyin.create_stylized_sentence(
		syllables, 
		[["vertical_zhuyin", ("pinyin"), "hanzi"]], 
		generate_css=True,
		vertical=True
	)
	print(html)
	print("\n<br>\n<br>")

	
	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	html, css = chromapinyin.create_stylized_sentence(
		syllables, 
		["hanzi", "pinyin"], 
		generate_css=False
	)

	print("\n<br>\n<br>")

	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	html, css = chromapinyin.create_stylized_sentence(
		syllables, 
		["hanzi", "pinyin"], 
		generate_css=False,
		vertical=True
	)

	html, css = chromapinyin.create_stylized_sentence(
		syllables, ["hanzi", "pinyin"], generate_css=True, vertical=True
	)

	html, css = chromapinyin.create_stylized_sentence(
		syllables, ["hanzi", "pinyin"], generate_css=False
	)

	html, css = chromapinyin.create_stylized_sentence(
		syllables, ["hanzi", "pinyin"], generate_css=False, vertical=True
	)
	for word in syllables:
		for syllable in word:
			print(syllable["zhuyin"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "李老板想找你演讲。"
	pinyin = "lǐ lǎobǎn xiǎng zhǎo nǐ yǎnjiǎng."
	inflections = [[3], [3, 3], [3], [3], [3], [3, 3]]
	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "我比你小。"
	pinyin = "wǒ bǐ nǐ xiǎo."
	inflections = [[3], [3], [3], [3]]
	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "我买雨伞。"
	pinyin = "wǒ mǎi yǔsǎn."
	inflections = [[3], [3], [3, 3]]
	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "我很好。"
	pinyin = "wǒ hěn hǎo."
	inflections = [[3], [3], [3]]
	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")

	hanzi = "很勇敢。"
	pinyin = "hěn yǒnggǎn."
	inflections = [[3], [3, 3]]
	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	for word in syllables:
		for syllable in word:
			print(syllable["hanzi"], end="")
		print("\n", end="")
	print("\n")
	'''

main()