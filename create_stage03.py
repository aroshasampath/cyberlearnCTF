import base64
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    BASE_DIR / ".env"
)


stage3_flag = os.getenv(
    "STAGE3_FLAG"
)

if not stage3_flag:
    raise RuntimeError(
        "STAGE3_FLAG is missing from .env"
    )


OUTPUT_DIR = (
    BASE_DIR
    / "challenges"
    / "stage03"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "message.txt"
)


# =========================================================
# CAESAR CIPHER
# =========================================================

def caesar_encrypt(
    text,
    shift=5
):

    result = []

    for character in text:

        if character.isupper():

            encrypted = chr(
                (
                    ord(character)
                    - ord("A")
                    + shift
                )
                % 26
                + ord("A")
            )

            result.append(
                encrypted
            )

        elif character.islower():

            encrypted = chr(
                (
                    ord(character)
                    - ord("a")
                    + shift
                )
                % 26
                + ord("a")
            )

            result.append(
                encrypted
            )

        else:

            result.append(
                character
            )

    return "".join(
        result
    )


# =========================================================
# ORIGINAL PLAINTEXT
# =========================================================

plaintext = (
    f"{stage3_flag}"
    "|"
    "NEXT_CLUE="
    "Logs remember what users forget."
)


# =========================================================
# FIRST LAYER - CAESAR +5
# =========================================================

caesar_text = caesar_encrypt(
    plaintext,
    shift=5
)


# =========================================================
# SECOND LAYER - BASE64
# =========================================================

base64_text = base64.b64encode(
    caesar_text.encode(
        "utf-8"
    )
).decode(
    "utf-8"
)


# =========================================================
# SAVE CHALLENGE FILE
# =========================================================

OUTPUT_FILE.write_text(
    base64_text + "\n",
    encoding="utf-8"
)


print(
    "Stage 03 challenge created successfully:"
)

print(
    OUTPUT_FILE
)