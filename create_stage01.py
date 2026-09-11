import os
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

flag = os.getenv("STAGE1_FLAG")

if not flag:
    raise RuntimeError(
        "STAGE1_FLAG is missing from .env"
    )


output_directory = (
    BASE_DIR
    / "challenges"
    / "stage01"
)

output_directory.mkdir(
    parents=True,
    exist_ok=True
)

output_file = (
    output_directory
    / "welcome.png"
)


# ==================================================
# IMAGE SETTINGS
# ==================================================

width = 1600
height = 900

image = Image.new(
    "RGB",
    (width, height),
    (7, 17, 31)
)

draw = ImageDraw.Draw(image)


# ==================================================
# BACKGROUND
# ==================================================

for y in range(height):

    ratio = y / height

    r = int(7 + (10 * ratio))
    g = int(17 + (25 * ratio))
    b = int(31 + (35 * ratio))

    draw.line(
        [(0, y), (width, y)],
        fill=(r, g, b)
    )


# ==================================================
# FONTS
# ==================================================

try:

    title_font = ImageFont.truetype(
        "arial.ttf",
        72
    )

    subtitle_font = ImageFont.truetype(
        "arial.ttf",
        34
    )

    small_font = ImageFont.truetype(
        "arial.ttf",
        24
    )

except OSError:

    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    small_font = ImageFont.load_default()


# ==================================================
# VISIBLE IMAGE CONTENT
# ==================================================

draw.text(
    (120, 250),
    "CyberLearn CTF",
    font=title_font,
    fill=(113, 230, 176)
)

draw.text(
    (125, 350),
    "Group 18 Security Quest",
    font=subtitle_font,
    fill=(240, 245, 250)
)

draw.text(
    (125, 430),
    "Stage 01 - Hidden in Plain Sight",
    font=small_font,
    fill=(165, 185, 205)
)

draw.text(
    (125, 490),
    "Not everything inside a file can be seen.",
    font=small_font,
    fill=(165, 185, 205)
)


# ==================================================
# HIDDEN PNG METADATA
# ==================================================

metadata = PngInfo()

metadata.add_text(
    "Title",
    "CyberLearn CTF Stage 01"
)

metadata.add_text(
    "Description",
    "Hidden in Plain Sight"
)

metadata.add_text(
    "Comment",
    (
        f"{flag} | "
        "NEXT CLUE: The next gate trusts "
        "the browser more than it should."
    )
)


# ==================================================
# SAVE PNG
# ==================================================

image.save(
    output_file,
    "PNG",
    pnginfo=metadata
)

print(
    "Stage 01 challenge created successfully:"
)

print(
    output_file
)