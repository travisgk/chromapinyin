# chromapinyin._stylize._color_scheme.py
# ---
# this file creates and maintains internal dictionaries that provide
# a particular color for each possible inflection.
# these color schemes are designed to be modified by the user if they please.
#
# these functions can be accessed by the user, for example:
# 	chromapinyin.color_scheme.set_to_sinosplice()
#

from chromapinyin._syllable._inflection import TO_INFLECTION
from chromapinyin._syllable._vowel_chars import PUNCTUATION_TONE_NUM

_inflection_to_RGB = None
_chroma_tones = None
_chroma_gif_colors_white = None
_chroma_gif_colors_black = None
_nightmode_GIF_punctuation_RGB = None


def get_inflection_RGB(inflection):
    return _inflection_to_RGB[inflection]


def get_inflection_color_style(inflection):
    return _chroma_tones[inflection]


def get_chroma_tone_values():
    return _chroma_tones.values()


def get_inflection_img_color_style(inflection, white_background=True):
    if white_background:
        return _chroma_gif_colors_white[inflection]
    return _chroma_gif_colors_black[inflection]


def get_chroma_gif_colors_white_values():
    return _chroma_gif_colors_white.values()


def get_chroma_gif_colors_black_values():
    return _chroma_gif_colors_black.values()


def set_punctuation_RGB(rgb):
    global _inflection_to_RGB
    _inflection_to_RGB[PUNCTUATION_TONE_NUM] = rgb
    rebuild_colors()


# sets the color scheme to chromapinyin's default.
def set_to_default():
    global _inflection_to_RGB, _nightmode_GIF_punctuation_RGB
    HIGH_COLOR = (255, 157, 18)
    RISING_COLOR = (0, 190, 36)
    LOW_COLOR = (0, 87, 190)
    FALLING_COLOR = (176, 111, 219)
    NEUTRAL_COLOR = (128, 128, 128)
    set_inflection_to_RGB(
        HIGH_COLOR, RISING_COLOR, LOW_COLOR, FALLING_COLOR, NEUTRAL_COLOR
    )
    _inflection_to_RGB[TO_INFLECTION["rising_low"]] = (7, 169, 250)
    _nightmode_GIF_punctuation_RGB = (255, 255, 255)
    rebuild_colors()


# sets the color scheme to Nathan Dummitt's color scheme used
# in Chinese Through Tone & Color.
def set_to_dummit():
    HIGH_COLOR = (244, 29, 47)
    RISING_COLOR = (249, 118, 27)
    LOW_COLOR = (151, 205, 93)
    FALLING_COLOR = (88, 155, 200)
    NEUTRAL_COLOR = (128, 128, 128)
    set_inflection_to_RGB(
        HIGH_COLOR, RISING_COLOR, LOW_COLOR, FALLING_COLOR, NEUTRAL_COLOR
    )
    rebuild_colors()


# sets the color scheme to the MBDG Chinese Dictionary's color scheme.
def set_to_MDBG():
    HIGH_COLOR = (255, 0, 0)
    RISING_COLOR = (216, 144, 0)
    LOW_COLOR = (0, 160, 0)
    FALLING_COLOR = (0, 0, 255)
    NEUTRAL_COLOR = (0, 0, 0)
    set_inflection_to_RGB(
        HIGH_COLOR, RISING_COLOR, LOW_COLOR, FALLING_COLOR, NEUTRAL_COLOR
    )
    rebuild_colors()


# sets the color scheme to the Hanping Chinese Dictionary's color scheme.
def set_to_hanping():
    HIGH_COLOR = (100, 180, 255)
    RISING_COLOR = (48, 176, 48)
    LOW_COLOR = (240, 128, 0)
    FALLING_COLOR = (208, 0, 32)
    NEUTRAL_COLOR = (160, 160, 160)
    set_inflection_to_RGB(
        HIGH_COLOR, RISING_COLOR, LOW_COLOR, FALLING_COLOR, NEUTRAL_COLOR
    )
    rebuild_colors()


# sets the color scheme to Pleco Software's color scheme.
def set_to_pleco():
    HIGH_COLOR = (227, 0, 0)
    RISING_COLOR = (2, 179, 28)
    LOW_COLOR = (21, 16, 240)
    FALLING_COLOR = (137, 0, 191)
    NEUTRAL_COLOR = (119, 119, 119)
    set_inflection_to_RGB(
        HIGH_COLOR, RISING_COLOR, LOW_COLOR, FALLING_COLOR, NEUTRAL_COLOR
    )
    rebuild_colors()


# sets the color scheme to the proposed system formulated
# by John Pasden of the website Sinosplice.
def set_to_sinosplice():
    HIGH_COLOR = (244, 161, 50)
    RISING_COLOR = (95, 204, 47)
    LOW_COLOR = (32, 92, 181)
    FALLING_COLOR = (217, 56, 33)
    NEUTRAL_COLOR = (128, 128, 128)
    set_inflection_to_RGB(
        HIGH_COLOR, RISING_COLOR, LOW_COLOR, FALLING_COLOR, NEUTRAL_COLOR
    )
    rebuild_colors()


# sets the colors for every inflection using a handful of given colors.
# neutral colors will be interpolated between <NEUTRAL_COLOR>
# and corresponding primary tone colors.
def set_inflection_to_RGB(
    HIGH_COLOR,
    RISING_COLOR,
    LOW_COLOR,
    FALLING_COLOR,
    NEUTRAL_COLOR,
    NEUTRAL_INTERPOLATION=0.2,  # 0.0 for full neutral color.
):
    global _inflection_to_RGB
    _inflection_to_RGB = {
        TO_INFLECTION["apostrophe"]: (0, 0, 0),
        TO_INFLECTION["punctuation"]: (0, 0, 0),  # punctuation
        TO_INFLECTION["neutral"]: NEUTRAL_COLOR,
        TO_INFLECTION["high"]: HIGH_COLOR,
        TO_INFLECTION["rising"]: RISING_COLOR,
        TO_INFLECTION["low"]: LOW_COLOR,
        TO_INFLECTION["falling"]: FALLING_COLOR,
        TO_INFLECTION["full_low"]: LOW_COLOR,
        TO_INFLECTION["half_falling"]: FALLING_COLOR,
        TO_INFLECTION["neutral_high"]: _mid_RGB(
            NEUTRAL_COLOR, HIGH_COLOR, NEUTRAL_INTERPOLATION
        ),
        TO_INFLECTION["neutral_rising"]: _mid_RGB(
            NEUTRAL_COLOR, RISING_COLOR, NEUTRAL_INTERPOLATION
        ),
        TO_INFLECTION["neutral_low"]: _mid_RGB(
            NEUTRAL_COLOR, LOW_COLOR, NEUTRAL_INTERPOLATION
        ),
        TO_INFLECTION["neutral_falling"]: _mid_RGB(
            NEUTRAL_COLOR, FALLING_COLOR, NEUTRAL_INTERPOLATION
        ),
        TO_INFLECTION["rising_low"]: _mid_RGB(LOW_COLOR, RISING_COLOR),
        TO_INFLECTION["rising_yi"]: RISING_COLOR,
        TO_INFLECTION["falling_yi"]: FALLING_COLOR,
        TO_INFLECTION["rising_bu"]: RISING_COLOR,
    }


# creates dictionaries containing the internal color styling dicts used for HTML.
def rebuild_colors():
    global _chroma_tones, _chroma_gif_colors_white, _chroma_gif_colors_black
    _chroma_tones = {
        inflection: {
            "class": "chroma-tone-" + inflection_str.replace("_", "-"),
            "style": (f"color: {_RGB_to_hex(_inflection_to_RGB[inflection])};",),
        }
        for inflection_str, inflection in TO_INFLECTION.items()
    }

    _chroma_gif_colors_white = {
        inflection: {
            "class": "img.chroma-tone-" + inflection_str.replace("_", "-"),
            "style": _RGB_to_svg_filter(
                _inflection_to_RGB[inflection], white_background=True
            ),
        }
        for inflection_str, inflection in TO_INFLECTION.items()
    }

    _chroma_gif_colors_black = {
        inflection: {
            "class": ".nightMode img.chroma-tone-" + inflection_str.replace("_", "-"),
            "style": _RGB_to_svg_filter(
                (
                    _inflection_to_RGB[inflection]
                    if (
                        inflection != PUNCTUATION_TONE_NUM
                        or not _nightmode_GIF_punctuation_RGB
                    )
                    else _nightmode_GIF_punctuation_RGB
                ),
                white_background=False,
            ),
        }
        for inflection_str, inflection in TO_INFLECTION.items()
    }


# returns a styling filter which will convert the original black
# pixels in the image to the given <rgb> tuple.
# <white_background> is a boolean option.
def _RGB_to_svg_filter(rgb, white_background):
    r = f"{rgb[0] / 255:.3f}"
    g = f"{rgb[1] / 255:.3f}"
    b = f"{rgb[2] / 255:.3f}"
    GRAY = "0.27"

    if white_background:
        r = f"{1.0 - rgb[0] / 255:.3f}"
        g = f"{1.0 - rgb[1] / 255:.3f}"
        b = f"{1.0 - rgb[2] / 255:.3f}"

    tabs = "\t"
    result = (
        "filter: contrast(135%) invert(100%)",
        f'{tabs}url("\\',
        f"{tabs}data:image/svg+xml;utf8,\\",
        f"{tabs}<svg xmlns='http://www.w3.org/2000/svg' version='1.1'>\\",
        f"{tabs}<defs>\\",
        f"{tabs}<filter id='color-filter' color-interpolation-filters='sRGB'>\\",
        f"{tabs}<feComponentTransfer>\\",
        f"{tabs}<feFuncR type='table' tableValues='0 {GRAY} {r} {r}'/>\\",
        f"{tabs}<feFuncG type='table' tableValues='0 {GRAY} {g} {g}'/>\\",
        f"{tabs}<feFuncB type='table' tableValues='0 {GRAY} {b} {b}'/>\\",
        f"{tabs}</feComponentTransfer>\\",
        f"{tabs}</filter>\\",
        f"{tabs}</defs>\\",
        f'{tabs}</svg>#color-filter")'
        + (" invert(100%)" if white_background else "")
        + ";",
    )

    return result


# returns an RGB tuple that's interpolated between two given colors.
def _mid_RGB(a_RGB, b_RGB, factor=0.5):
    d_RGB = tuple([b_RGB[i] - a_RGB[i] for i in range(3)])
    return tuple([int(a_RGB[i] + d_RGB[i] * factor) for i in range(3)])


# returns a string of an RGB tuple converted to a hex code.
def _RGB_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


set_to_default()
