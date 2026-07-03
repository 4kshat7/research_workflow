"""Generate a collaborative word cloud from participant name files.

This is the main *collaborative* activity for the Git/GitHub workshop:

  1. Each participant adds a small text file to  names/  (e.g. alice.txt)
     containing their name, and commits + pushes it.
  2. Anyone can then run this script to build a shared word cloud from
     everyone's names and save it as a PNG in  outputs/.

Styling: a round "petri-dish" mask and a green/blue genomics colour palette.
If anything about the masking/colours fails (e.g. numpy missing), the script
falls back to a plain rectangular word cloud so the demo always works.

Run it from the repo root:
    python scripts/generate_wordcloud.py
"""

import re
from collections import Counter
from pathlib import Path

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# A name's words may be separated by spaces, underscores, or hyphens in the
# .txt file. This matches any run of those so we can normalise to one space.
SEPARATORS = re.compile(r"[\s_-]+")

# --- Locations, worked out relative to this script -------------------------
ROOT = Path(__file__).resolve().parent.parent
NAMES_DIR = ROOT / "names"
OUTPUT_PATH = ROOT / "outputs" / "wordcloud.png"

# Green/blue "genomics" colour palette (hex). Used to colour the words.
GENOMICS_COLORS = ["#0b6e4f", "#08a045", "#16db93", "#0f8b8d", "#137a7f",
                   "#1e6091", "#168aad", "#34a0a4", "#52b69a", "#2c7da0"]


def read_names(names_dir):
    """Read every .txt file and return a {name: count} frequency map.

    The words in a name may be separated by spaces, underscores, or hyphens
    ("Ada Lovelace", "Ada_Lovelace", "Ada-Lovelace") — all are normalised to a
    single space. We return a frequency dict (not a text blob) so the word
    cloud draws each full name as ONE item *with a real space* — no ugly
    underscores on screen. Feeding frequencies also skips WordCloud's own
    tokenising step, which keeps generation fast.
    """
    counts = Counter()
    for txt_file in sorted(names_dir.glob("*.txt")):
        raw = txt_file.read_text(encoding="utf-8").strip()
        if not raw:
            continue
        name = SEPARATORS.sub(" ", raw).strip()
        if name:
            counts[name] += 1
    return counts


def petri_dish_mask(size=800):
    """Build a circular ('petri dish') mask array, or None if numpy is absent.

    The wordcloud library treats white (255) as 'do not draw here' and any
    other value as drawable. So we paint everything white, then carve out a
    black circle in the middle for the words to fill.
    """
    try:
        import numpy as np
    except ImportError:
        return None  # caller will fall back to a plain (unmasked) cloud

    # Start fully white (masked out everywhere).
    mask = np.full((size, size), 255, dtype=np.uint8)

    # Grid of coordinates; distance from centre for every pixel.
    y, x = np.ogrid[:size, :size]
    center = size / 2
    distance = np.sqrt((x - center) ** 2 + (y - center) ** 2)

    # Inside the circle -> 0 (drawable). Radius leaves a small margin.
    mask[distance <= center - 10] = 0
    return mask


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """Pick a colour from the genomics palette for each word."""
    # random_state is a random.Random instance supplied by wordcloud.
    return random_state.choice(GENOMICS_COLORS)


def main():
    counts = read_names(NAMES_DIR)

    if not counts:
        print("No names found in names/.")
        print("Add a file like  names/alice.txt  containing a name, then re-run.")
        return

    mask = petri_dish_mask()

    # Shared settings; add the mask only if we successfully built one.
    kwargs = dict(
        width=800,
        height=800,
        background_color="white",
        prefer_horizontal=0.9,
        color_func=color_func,
    )
    if mask is not None:
        kwargs["mask"] = mask
        print("Using round petri-dish mask.")
    else:
        print("numpy not available -> falling back to a plain word cloud.")

    # generate_from_frequencies draws each dict key verbatim (spaces kept)
    # and treats it as a single item — exactly what we want for full names.
    cloud = WordCloud(**kwargs).generate_from_frequencies(counts)

    # Make sure the outputs/ folder exists, then save the image.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cloud.to_file(OUTPUT_PATH)
    print(f"Saved word cloud to {OUTPUT_PATH.relative_to(ROOT)}")

    # Also show it in a matplotlib window / inline in a notebook.
    plt.figure(figsize=(8, 8))
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


if __name__ == "__main__":
    main()
