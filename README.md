# chromapinyin
A python script for creating HTML tables of various Mandarin transcriptions (IPA and zhuyin), with the option to color syllables by their tone.
These can be created by giving the program text in hanzi and its corresponding pinyin.
The program will take the necessary tone changes into account.

## Installation
```
pip install pillow
```

## Getting syllable information
```
import chromapinyin

hanzi = "我买雨伞。"
pinyin = "wǒ mǎi yǔsǎn."
syllables = chromapinyin.create_syllable_list(hanzi, pinyin)
```
The ```syllables``` list will contain four lists, with each list representing a "word", a group of syllables.
- ```syllables[0]``` will contain one syllable corresponding to "wǒ" 
- ```syllables[1]``` will contain one syllable corresponding to "mǎi"
- ```syllables[2]``` will contain two syllables corresponding to "yǔ" and "sǎn"
- ```syllables[3]``` will contain one "syllable" corresponding to the "."
<br>

The contained word list is occupied by dictionary objects which each represent a syllable.
<br>
For example, ```syllables[0][0]``` is a dictionary object with the following keys:
- ```"hanzi": "伞"```
- ```"pinyin": "sǎn"```
- ```"tone": "low"```
- ```"tone_num": 3```
- ```"spoken_tone": "low"```
- ```"spoken_tone_num": 3```
- ```"inflection": "full_low"```
- ```"inflection_num": 6```
- ```"ipa_root": "san"```
- ```"ipa_suffix": "˨˩˦"```
- ```"ipa": "san˨˩˦"```
- ```"zhuyin_prefix": ""```
- ```"zhuyin_root": "ㄙㄢ"```
- ```"zhuyin_suffix": "ˇ"```
- ```"zhuyin": "ㄙㄢˇ"```
<br>

## Resources
SVG animations from the ```svgs``` directory in the repository [makemeahanzi](https://github.com/skishore/makemeahanzi/tree/master) can be downloaded and exported to ```_chroma_res/_makemeahanzi``` in order to let the HTML source these glyph animations.
