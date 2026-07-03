# Genomics Workshop Demo — Git & GitHub Collaboration

A tiny, **teaching-only** bioinformatics-flavoured repository used to practise
Git and GitHub in a live workshop. The DNA data here is fake and the analyses
are deliberately simple — this is a *teaching prop*, not real research.

The main collaborative activity is a **word cloud**: every participant adds a
small text file with their name, commits and pushes it, and then we regenerate
a shared word cloud from everyone's contributions. It's a fun way to see
branching, pull requests, and merging in action.

## Folder structure

```text
research_workflow/
├── names/                       # <- participants add their name files here (.txt)
├── images/                      # optional images for the notebook heading (logo/icon)
├── data/
│   └── sample_sequences.fasta   # 5-6 short dummy DNA sequences (fake!)
├── scripts/
│   ├── generate_wordcloud.py    # builds the collaborative word cloud PNG
│   ├── gc_content.py            # GC content per sequence
│   ├── sequence_length_stats.py # min / max / mean sequence length
│   └── codon_usage.py           # codon frequency counts for a sequence
├── notebooks/
│   └── wordcloud_demo.ipynb     # runs the word cloud + displays it inline
├── outputs/                     # generated word cloud images land here
├── requirements.txt
└── README.md
```

---

## Step 1 — Create a Python environment

This makes an isolated `.venv` folder so the workshop packages don't touch the
rest of your system. Run the block for **your** operating system.

```bash
# --- macOS / Linux ---
python3 -m venv .venv
source .venv/bin/activate

# --- Windows (PowerShell) ---
python -m venv .venv
.venv\Scripts\Activate.ps1

# --- Windows (Command Prompt / cmd.exe) ---
python -m venv .venv
.venv\Scripts\activate.bat
```

You'll know it worked when your prompt shows `(.venv)` at the start.
(To leave the environment later, just run `deactivate`.)

Tip: on Windows the command is usually `python`; on macOS/Linux it's often
`python3`. Use whichever one your system has.

## Step 2 — Install the dependencies

With the environment activated (same command on every OS):

```bash
pip install -r requirements.txt
```

---

## Step 3 — Run everything, step by step

Run these from the **repo root** (the folder containing this README). The
commands are identical on macOS, Linux, and Windows — use `python3` instead of
`python` if that's what your system uses.

1. GC content — GC % of each dummy sequence:

   ```bash
   python scripts/gc_content.py
   ```

2. Length stats — min / max / mean sequence length:

   ```bash
   python scripts/sequence_length_stats.py
   ```

3. Codon usage — codon counts for the first sequence (or pass a sequence ID):

   ```bash
   python scripts/codon_usage.py
   python scripts/codon_usage.py seq3
   ```

4. Word cloud — builds `outputs/wordcloud.png` from every name in `names/`:

   ```bash
   python scripts/generate_wordcloud.py
   ```

After the last step you'll find the image at `outputs/wordcloud.png`, and a
matplotlib window will also pop up showing it.

### Prefer a notebook?

```bash
pip install jupyter        # if you don't already have it
jupyter notebook notebooks/wordcloud_demo.ipynb
```

Run the cells top to bottom — it builds the word cloud and displays it inline.

---

## The collaborative word cloud activity (the fun part)

This is the part participants do together with Git & GitHub.

### Add your name

Create a text file in `names/` named after yourself, containing your name (or
any genomics-y word you like!). One name per file is perfect. Pick the command
for your OS, or just create the file in your editor:

```bash
# --- macOS / Linux ---
echo "Ada Lovelace" > names/ada.txt

# --- Windows (PowerShell) ---
"Ada Lovelace" | Out-File -Encoding utf8 names\ada.txt

# --- Windows (Command Prompt / cmd.exe) ---
echo Ada Lovelace> names\ada.txt
```

### Commit and share it with Git

```bash
git checkout -b add-ada-name       # make your own branch
git add names/ada.txt
git commit -m "Add Ada's name to the word cloud"
git push -u origin add-ada-name    # then open a Pull Request on GitHub
```

Once everyone's names are merged into the main branch, pull the latest changes:

```bash
git checkout main
git pull
```

### Regenerate the word cloud

```bash
python scripts/generate_wordcloud.py
```

This reads **every** `.txt` file in `names/`, combines the names, and saves a
green/blue, petri-dish-shaped word cloud to `outputs/wordcloud.png`. (If your
setup can't build the mask, it automatically falls back to a plain word cloud
so it always produces an image.)

Word names may be separated by a space, an underscore, or a hyphen
(`Ada Lovelace`, `Ada_Lovelace`, `Ada-Lovelace`) — the script normalises them
all and always shows a clean name with a real space.

For a fun finish, open `notebooks/wordcloud_demo.ipynb`: it shows the word cloud
with a celebration heading ("I learned how to use Git!") and an icon on top.

---

## About the mini "analysis" scripts

These run on the dummy FASTA file (`data/sample_sequences.fasta`) and are handy
for demonstrating commits, diffs, and running code together. They use only
plain Python — no bioinformatics library required.

## Resetting the demo names

`names/` ships with ~80 demo files so the word cloud works out of the box. To
start fresh for a real workshop, delete the `.txt` files but keep `.gitkeep`:

```bash
# --- macOS / Linux ---
rm names/*.txt

# --- Windows (PowerShell) ---
Remove-Item names\*.txt
```

## Disclaimer

All sequences and analyses in this repository are made up for teaching Git and
GitHub. Please don't use any of it for actual scientific work.
