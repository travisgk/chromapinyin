# chromapinyin
A Python script for creating HTML tables of various Chinese transcriptions (IPA and zhuyin), with the option to color syllables by their tone.
These can be created by giving chromapinyin text in hanzi and text of its corresponding pinyin.
The program will take the necessary tone changes into account.

<br>

## Installation
```
pip install pillow imageio
```
[pillow](https://github.com/python-pillow/Pillow) is used for creating customized pitch graph components.

[imageio](https://github.com/imageio/imageio) is optional. Installing it will enable functionality to modify the GIF animations' speed and/or looping behavior.

<br>

## Resources

GIF animations from the repository [chinese-char-animations](https://github.com/nmarley/chinese-char-animations) can be downloaded and have its folders ```images``` and ```images_large``` placed under chromapinyin's output directory to be ```_chroma_res/handwriting/images``` and ```_chroma_res/handwriting/images_large``` respectively.

Then, the following can be run to change the speed and looping behavior of the GIFs:
```
import chromapinyin
chromapinyin.process_gifs(fps=5, start_freeze_ms=1000, end_freeze_ms=3500, loops=True)
```

```_chroma_res/handwriting/images``` will be the directory used to source handwriting animations.

The process GIFs function will also rename the files under ```_chroma_res/handwriting/images-large```,
so this directory can easily be renamed to ```_chroma_res/handwriting/images``` to be used instead.

<br>

# Making a stylized table
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

Every contained list is occupied by dictionary objects which represent each syllable in a word.
<br>
For example, ```word_list[2][1]``` is a dictionary object with the following keys:
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
