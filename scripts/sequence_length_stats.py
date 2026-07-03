"""Print min / max / mean sequence length for the sample FASTA file.

Run it from the repo root:
    python scripts/sequence_length_stats.py
"""

from pathlib import Path

FASTA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_sequences.fasta"


def read_fasta(path):
    """Read a FASTA file into a dict: {sequence_id: sequence_string}."""
    sequences = {}
    current_id = None
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            current_id = line[1:].split()[0]
            sequences[current_id] = ""
        else:
            sequences[current_id] += line.upper()
    return sequences


def main():
    sequences = read_fasta(FASTA_PATH)
    lengths = [len(seq) for seq in sequences.values()]

    if not lengths:
        print("No sequences found.")
        return

    # Basic summary statistics (kept as plain Python for readability).
    minimum = min(lengths)
    maximum = max(lengths)
    mean = sum(lengths) / len(lengths)

    print(f"Sequence length stats for {len(lengths)} sequences:\n")
    print(f"  min  : {minimum}")
    print(f"  max  : {maximum}")
    print(f"  mean : {mean:.1f}")


if __name__ == "__main__":
    main()
