"""Print the GC content of every sequence in the sample FASTA file.

GC content = percentage of bases that are G or C. It's a common,
easy-to-compute summary statistic in genomics.

Run it from the repo root:
    python scripts/gc_content.py
"""

from pathlib import Path

# Path to the FASTA file, worked out relative to THIS script so the
# command works no matter which folder you run it from.
FASTA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_sequences.fasta"


def read_fasta(path):
    """Read a FASTA file into a dict: {sequence_id: sequence_string}.

    A FASTA file looks like:
        >seq1 some description
        ATGC...
        ATGC...
        >seq2 ...
    Lines starting with '>' are headers; everything else is sequence data.
    """
    sequences = {}
    current_id = None
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue  # skip blank lines
        if line.startswith(">"):
            # The ID is the first word after '>' (drop the description).
            current_id = line[1:].split()[0]
            sequences[current_id] = ""
        else:
            sequences[current_id] += line.upper()
    return sequences


def gc_content(sequence):
    """Return the GC percentage of a single DNA sequence."""
    if not sequence:
        return 0.0
    gc = sequence.count("G") + sequence.count("C")
    return gc / len(sequence) * 100


def main():
    sequences = read_fasta(FASTA_PATH)
    print(f"GC content for {len(sequences)} sequences in {FASTA_PATH.name}:\n")
    for seq_id, seq in sequences.items():
        print(f"  {seq_id:12s}  {gc_content(seq):5.1f} %   (length {len(seq)})")


if __name__ == "__main__":
    main()
