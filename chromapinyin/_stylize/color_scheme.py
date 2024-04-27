from ._inflection import TO_INFLECTION

_inflection_to_RGB = None
_CHROMA_TONES = None

def set_to_default():
	global _inflection_to_RGB
	HIGH_COLOR = (255, 157, 18)
	RISING_COLOR = (0, 190, 36)
	LOW_COLOR = (0, 87, 190)
	FALLING_COLOR = (176, 111, 219)
	NEUTRAL_COLOR = (128, 128, 128)

	_set_inflection_to_RGB(
		HIGH_COLOR, RISING_COLOR, LOW_COLOR, FALLING_COLOR, NEUTRAL_COLOR 
	)
	_inflection_to_RGB[TO_INFLECTION["rising_low"]] = (7, 169, 250)
	_rebuild_colors()

def set_to_dummit():
	HIGH_COLOR = (244, 29, 47)
	RISING_COLOR = (249, 118, 27)
	LOW_COLOR = (151, 205, 93)
	FALLING_COLOR = (88, 155, 200)
	NEUTRAL_COLOR = (128, 128, 128)

	_set_inflection_to_RGB(
		HIGH_COLOR, RISING_COLOR, LOW_COLOR, FALLING_COLOR, NEUTRAL_COLOR 
	)
	_rebuild_colors()

def _set_inflection_to_RGB(
	HIGH_COLOR, RISING_COLOR, LOW_COLOR, FALLING_COLOR, NEUTRAL_COLOR
):
	global _inflection_to_RGB
	_inflection_to_RGB = {
		TO_INFLECTION["apostrophe"]: (0, 0, 0),
		TO_INFLECTION["none"]: (0, 0, 0), # punctuation
		TO_INFLECTION["neutral"]: NEUTRAL_COLOR,
		TO_INFLECTION["high"]: HIGH_COLOR,
		TO_INFLECTION["rising"]: RISING_COLOR,
		TO_INFLECTION["low"]: LOW_COLOR,
		TO_INFLECTION["falling"]: FALLING_COLOR,
		TO_INFLECTION["full_low"]:  LOW_COLOR,
		TO_INFLECTION["half_falling"]: FALLING_COLOR,
		TO_INFLECTION["neutral_high"]: _mid_RGB(NEUTRAL_COLOR, HIGH_COLOR, 0.2),
		TO_INFLECTION["neutral_rising"]: _mid_RGB(NEUTRAL_COLOR, RISING_COLOR, 0.2),
		TO_INFLECTION["neutral_low"]: _mid_RGB(NEUTRAL_COLOR, LOW_COLOR, 0.2),
		TO_INFLECTION["neutral_falling"]: _mid_RGB(NEUTRAL_COLOR, FALLING_COLOR, 0.2),
		TO_INFLECTION["rising_low"]: _mid_RGB(LOW_COLOR, RISING_COLOR),
		TO_INFLECTION["rising_yi"]: RISING_COLOR,
		TO_INFLECTION["falling_yi"]: FALLING_COLOR,
		TO_INFLECTION["rising_bu"]: RISING_COLOR,
	}

def _rebuild_colors():
	global _CHROMA_TONES
	_CHROMA_TONES = {
		inflection: {
			"class": "chroma-tone-" + inflection_str.replace("_", "-"),
			"style": (f"color: {_RGB_to_hex(_inflection_to_RGB[inflection])};",),
		} for inflection_str, inflection in TO_INFLECTION.items()
	}

# returns an RGB tuple that's interpolated between two given colors.
def _mid_RGB(a_RGB, b_RGB, factor=0.5):
	d_RGB = tuple([b_RGB[i] - a_RGB[i] for i in range(3)])
	return tuple([int(a_RGB[i] + d_RGB[i] * factor) for i in range(3)])

# returns a string of an RGB tuple converted to a hex code.
def _RGB_to_hex(rgb):
	return '#{:02x}{:02x}{:02x}'.format(*rgb)

set_to_default()
