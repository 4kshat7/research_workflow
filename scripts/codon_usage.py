"""Count codon usage for a sequence in the sample FASTA file.

A codon is a group of 3 DNA bases (e.g. ATG). This script splits a
sequence into non-overlapping codons and counts how often each appears.

Run it from the repo root:
    python scripts/codon_usage.py            # uses the first sequence
    python scripts/codon_usage.py seq3       # pick a sequence by its ID
"""

import sys
from collections import Counter
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


def count_codons(sequence):
    """Split a sequence into 3-base codons and count each one.

    Any trailing 1-2 bases that don't form a full codon are ignored.
    """
    codons = [sequence[i:i + 3] for i in range(0, len(sequence) - 2, 3)]
    return Counter(codons)


def main():
    sequences = read_fasta(FASTA_PATH)

    # Optional command-line argument: which sequence to analyse.
    # Default to the first sequence in the file.
    if len(sys.argv) > 1:
        seq_id = sys.argv[1]
        if seq_id not in sequences:
            print(f"Sequence '{seq_id}' not found. Available: {', '.join(sequences)}")
            return
    else:
        seq_id = next(iter(sequences))

    counts = count_codons(sequences[seq_id])

    print(f"Codon usage for '{seq_id}' ({sum(counts.values())} codons total):\n")
    # Sort by count (most frequent first), then alphabetically for ties.
    for codon, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {codon}  {count}")


if __name__ == "__main__":
    main()
