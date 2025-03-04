# Normalization Training

## 1. Generate a Metadata Table
- Create a CSV file (`table.csv`) listing all texts and their associated metadata.
- Ensure that one column contains the filename of each text (e.g., `CRRPV16_Chansons_nouvelles.tsv`).

## 2. Build the Corpus
- Collect and process all texts to create the corpus: 15 texts.
  - with data split's option 3 (split ratio 90-10):
    - train+dev (90-10): 14 texts, 1.341 pages, 35.450 lines;
    - test (`CRRPV11_Moralite.tsv`): one text, 96 pages, 2.485 lines.
- Each processed text is stored in a TSV file (`.tsv`).
- Each TSV file contains two columns:
  - One column for the original lines of text.
  - One column for the normalized lines.

## 3. Create the Data Split
- Use the scripts to divide the corpus into appropriate training, validation, and test sets.
- In "data" you'll find the final split in the following format :
  - train.src and train.trg
  - dev.src and dev.trg
  - test.src and test.trg

**Option 1: Split Ratio 70-15-15**

| **Split** | **Proportion** | **Occurrences per 20 lines** |
|-----------|--------------|--------------------------|
| **Train** | 70%          | 14 lines                |
| **Dev**   | 15%          | 3 lines                 |
| **Test**  | 15%          | 3 lines                 |

```
python
subcorpora = {
    "1-standard": [
        "train", "train", "train", "train", "test",   # First 5 lines: 4 to train, 1 to test
        "train", "train", "train", "dev", "train",    # Next 5 lines: 4 to train, 1 to dev
        "train", "train", "train", "test", "train",   # Next 5 lines: 4 to train, 1 to test
        "train", "dev", "train", "test"              # Last 5 lines: 2 to train, 1 to dev, 1 to test
    ]
}
```

**Option 2: Split Ratio 80-10-10**

| **Split** | **Proportion** | **Occurrences per 10 lines** |
|-----------|--------------|--------------------------|
| **Train** | 80%          | 8 lines                |
| **Dev**   | 10%          | 1 lines                 |
| **Test**  | 10%          | 1 lines                 |

```
python
subcorpora = {
    "1-standard": [
        "train", "train", "train", "train", "train", "train", "train", "train", "dev", "test",
        "train", "train", "train", "train", "train", "train", "train", "train", "dev", "test"
    ]
}
```

**Option 3: Split Ratio 90-10**

- Train: 90% (18 lines per 20)
- Dev: 10% (2 lines per 20)

No "test" labels, ensuring only "train" and "dev" exist.

Every 10 lines contain 9 "train" and 1 "dev" for a consistent 90-10 split.

```
subcorpora = {
    "1-standard": [
        "train", "train", "train", "train", "train",  # First 5 lines: 5 to train
        "train", "train", "train", "dev", "train",    # Next 5 lines: 4 to train, 1 to dev
        "train", "train", "train", "train", "train",  # Next 5 lines: 5 to train
        "train", "train", "train", "dev", "train"     # Last 5 lines: 4 to train, 1 to dev
    ]
}
```
