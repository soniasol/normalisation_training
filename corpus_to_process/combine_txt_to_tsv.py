import csv

# File paths
orig_file = "/Users/sonia/Documents/GitHub/normalisation_training/corpus_to_process/to_process/test-orig.txt"
norm_file = "/Users/sonia/Documents/GitHub/normalisation_training/corpus_to_process/to_process/test-norm.txt"
output_file = "/Users/sonia/Documents/GitHub/normalisation_training/corpus_to_process/processed/combined_output.tsv"

# Read the original and normalized files
with open(orig_file, "r", encoding="utf-8") as f_orig, open(norm_file, "r", encoding="utf-8") as f_norm:
    orig_lines = f_orig.readlines()
    norm_lines = f_norm.readlines()

# Ensure both files have the same number of lines
if len(orig_lines) != len(norm_lines):
    print("Warning: The files have different numbers of lines. Extra lines will be ignored.")
    min_length = min(len(orig_lines), len(norm_lines))
    orig_lines = orig_lines[:min_length]
    norm_lines = norm_lines[:min_length]

# Write to TSV file
with open(output_file, "w", encoding="utf-8", newline="") as f_out:
    tsv_writer = csv.writer(f_out, delimiter="\t")
    
    # Write line by line
    for orig, norm in zip(orig_lines, norm_lines):
        tsv_writer.writerow([orig.strip(), norm.strip()])

print(f"TSV file created: {output_file}")


# N.B. Run the script with : python3 combine_txt_to_tsv.py