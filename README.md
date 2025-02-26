# Normalization Training

## 1. Generate a Metadata Table
- Create a CSV file (`table.csv`) listing all texts and their associated metadata.
- Ensure that one column contains the filename of each text (e.g., `CRRPV16_Chansons_nouvelles.tsv`).

## 2. Build the Corpus
- Collect and process all texts to create the final corpus.
- Each processed text should be stored in a TSV file (`.tsv`).
- Each TSV file must contain two columns:
  - One column for the original lines of text.
  - One column for the normalized lines.

## 3. Create the Data Split
- Use one or more scripts to divide the corpus into appropriate training, validation, and test sets as needed.
