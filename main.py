import chromapinyin

def main():
	sample_list = "shén me shí hòu".split()
	for syllable in sample_list:
		tone_num = chromapinyin.get_tone_num(syllable)
		stripped = chromapinyin.strip_tone_marker(syllable)
		print(chromapinyin.place_tone_marker(stripped, tone_num), end=" ")
	print("\n")

	hanzi = "我买雨伞。"
	pinyin = "wǒ mǎi yǔsǎn."
	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	html, css = chromapinyin.create_stylized_sentence(
		syllables, ["hanzi", ("pinyin", "merge_punctuation")], generate_css=False
	)

	hanzi = "我比你小。"
	pinyin = "wǒ bǐ nǐ xiǎo."
	syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
	html, css = chromapinyin.create_stylized_sentence(
		syllables, ["hanzi", ("pinyin", "merge_punctuation")], generate_css=False
	)

	'''
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