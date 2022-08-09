import pprint
import re
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

EMOJI_FILE = "emoji.html"

info = re.compile(
    r"""<tr><td class='rchars'>\d+</td>
<td class='code'><a href='[^']+' name='[^']+'>[^<]+</a></td>
<td class='andr'><a href='[^']+' target='full'><img alt='([^']+)' title='([^']+)' class='imga' src='[^']+'></a></td>
<td class='name'>([^<]+)</td>
<td class='name'>([^<]+)</td>
</tr>"""
)


def get_info(fn: str) -> List[Tuple[str, str, str, str]]:
    contents = open(fn).read()
    return info.findall(contents)


def parse_info(info: List[Tuple[str, str, str, str]]) -> List[Tuple[str, str]]:
    ret: List[Tuple[str, str]] = []
    for item in info:
        tags = get_tags(item)
        tags.append(item[2])
        tags = set(" ".join(tags).split(" "))  # remove duplicate words
        tags_str = (
            " ".join(tags)
            .replace("flag: ", "")
            .replace("&amp; ", "")
            .replace("flag:", "")
            .replace("keycap:", "")
        )
        ret.append((item[0], tags_str))

    return ret


def get_tags(t: Tuple[str, str, str, str]) -> List[str]:
    return t[-1].split(" | ")


def emojis(info: List[Tuple[str, str]]) -> List[str]:
    return [e[0] for e in info]


def titles(info: List[Tuple[str, str, str, str]]) -> List[str]:
    return [e[2].capitalize() for e in info]


def titles_slice(info: List[Tuple[str, str, str, str]]) -> str:
    return ",\n".join(f'"{t}"' for t in titles(info)) + ","


def emoji_slice(info: List[Tuple[str, str]]) -> str:
    return ",\n".join(f"`{e[0]}`" for e in info)


def desc_slice(info: List[Tuple[str, str]]) -> str:
    return ",\n".join(f"`{e[1]}`" for e in info)


def render_emoji(unicode_text: str, i: int):
    back_ground_color = (0, 0, 0, 0)
    im = Image.new("RGBA", (64, 64), back_ground_color)
    draw = ImageDraw.Draw(im)

    font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 64)

    draw.text((0, 0), unicode_text, font=font, embedded_color=True)
    im.save(f"images/{i}.png")


def render_all():
    info = parse_info(get_info("emoji.html"))
    items = emojis(info)
    for i, item in tqdm(enumerate(items), total=len(items)):
        render_emoji(item, i)


print(titles_slice(get_info(EMOJI_FILE)))
