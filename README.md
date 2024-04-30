# chromapinyin
A python script for creating HTML tables of various Mandarin transcriptions (IPA and zhuyin), with the option to color syllables by their tone.
These can be created by giving the program text in hanzi and its corresponding pinyin.
The program will take the necessary tone changes into account.

## Installation
```
pip install pillow
```
<br>

## Making a stylized table
```
import chromapinyin
```
<br>

## Information in each syllable dictionary
```
import chromapinyin

hanzi = "我买雨伞。"
pinyin = "wǒ mǎi yǔsǎn."
word_list = chromapinyin.create_syllable_list(hanzi, pinyin)
```
The ```word_list``` list will contain four lists, with each list representing a "word", a group of syllables.
- ```word_list[0]``` will contain one syllable dictionary object corresponding to "wǒ" 
- ```word_list[1]``` will contain one syllable dictionary object corresponding to "mǎi"
- ```word_list[2]``` will contain two syllable dictionary objects corresponding to "yǔ" and "sǎn"
- ```word_list[3]``` will contain one "syllable" dictionary object corresponding to the "."
<br>

The contained word list is occupied by dictionary objects which each represent a syllable.
<br>
For example, ```word_list[0][0]``` is a dictionary object with the following keys:
- ```"hanzi": "伞"```
- ```"pinyin": "sǎn"```
- ```"tone_str": "low"```
- ```"tone_num": 3```
- ```"spoken_tone_str": "low"```
- ```"spoken_tone_num": 3```
- ```"inflection_str": "full_low"```
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
GIF animations from the repository [chinese-char-animations](https://github.com/nmarley/chinese-char-animations) can be downloaded and exported to a subdirectory under chromapinyin's output directory, ```_chroma_res/_handwriting```, in order to let the HTML source these glyph animations.
