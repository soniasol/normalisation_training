#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

# Run the script with: python scripts/split_ss_3.py

# Import necessary modules for file handling and system operations
import csv, glob, os, re, sys

# Get the path of the directory
folder = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))

# Define how to split lines from each text file
# "1-standard" is the only category in this case
# The list determines how each line should be assigned based on its index % 20 (the index is not % 10 in this case)
subcorpora = {
    "1-standard": [
        "train", "train", "train", "train", "train",  # First 5 lines: 5 to train
        "train", "train", "train", "dev", "train",    # Next 5 lines: 4 to train, 1 to dev
        "train", "train", "train", "train", "train",  # Next 5 lines: 5 to train
        "train", "train", "train", "dev", "train"     # Last 5 lines: 4 to train, 1 to dev
    ]
}

# Create the necessary directories for splitting the corpus

# Create the main "split" folder inside the script's directory (not necessary in this case)
# os.system("mkdir " + os.path.join(folder, "split"))

# Create subfolders for train, dev, and test sets (no need for "out" in this case)

trainFolder = os.path.join(os.path.join(folder, "split"), "train")
os.system("mkdir " + trainFolder)

devFolder = os.path.join(os.path.join(folder, "split"), "dev")
os.system("mkdir " + devFolder)

# Treat the corpus
fileNb = 0  # Initialize file counter

# Open the metadata file "table.csv" which contains information about the corpus
with open(os.path.join(folder, "table.csv"), newline='', encoding="utf-8") as metadataFile:
    reader = csv.DictReader(metadataFile, delimiter=',', quotechar='"')  # Read as dictionary

    # Loop through each row in the metadata file (each row represents a text file to process)
    for row in reader:
        fileNb += 1  # Increment file counter
        
        # Display information about the file being processed
        print("Treating file #" + str(fileNb) + " (" + row["file"] + ") in category " + row["Sub-corpus"])

        try:
            # Open the corresponding text file from the corpus directory
            with open(os.path.join(os.path.join(folder, "corpus"), row["file"]), newline='', encoding="utf-8") as treatedFile:
                spamreader = csv.reader(treatedFile, delimiter='\t', quotechar='"')

                # Create corresponding empty train, dev, and test files for output
                csvTrainFile = open(os.path.join(trainFolder, row["file"]), 'w', newline='', encoding="utf-8")
                trainWriter = csv.writer(csvTrainFile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                csvDevFile = open(os.path.join(devFolder, row["file"]), 'w', newline='', encoding="utf-8")
                devWriter = csv.writer(csvDevFile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                # Output files dictionary for easy reference
                outputFiles = {"train": trainWriter, "dev": devWriter}

                inputLineNb = 0  # Track the number of input lines processed
                outputLineNb = 0  # Track the number of output lines written

                # Process each line in the input file
                for line in spamreader:
                    inputLineNb += 1  # Increment input line count
                    
                    if len(line) > 2 and len(line[2])>0 and line[2]!=" ":
                  # if there exist a third column which is neither empty nor a single whitespace
                  # it should contain a corrected version of the erroneous first column in the original edition:
                  # use this third column instead of the first column for this line!
                       print("Line " + str(inputLineNb) + " contains a typo in the original version: we will use the corrected version!")
                       outputFiles[subcorpora[row["Sub-corpus"]][outputLineNb%10]].writerow([line[2],line[1].replace("'","’")])
                       outputLineNb += 1

                    else:
                  # add the current line to the right file,
                  # replacing ' by ’ in the normalized column
                      outputFiles[subcorpora[row["Sub-corpus"]][outputLineNb%10]].writerow([line[0],line[1].replace("'","’")])
                      outputLineNb += 1

                    outputLineNb += 1  # Increment output line count

                # Close all output files after processing
                csvTrainFile.close()
                csvDevFile.close()

        except (OSError):
            # Handle errors if the file is not found
            print("Error: file not found")
            pass

