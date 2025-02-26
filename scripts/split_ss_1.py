#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import csv, glob, os, re, sys  # Import necessary modules for file handling and system operations

# Get the absolute path of the directory where the script is located
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

# Define how to split lines from each text file
# "1-standard" is the only category in this case
# The list determines how each line should be assigned based on its index % 20 (the index is not % 10 in this case)
subcorpora = {
    "1-standard": [
        "train", "train", "train", "train", "test",   # First 5 lines: 4 to train, 1 to test
        "train", "train", "train", "dev", "train",    # Next 5 lines: 4 to train, 1 to dev
        "train", "train", "train", "test", "train",   # Next 5 lines: 4 to train, 1 to test
        "train", "dev", "train", "test"              # Last 5 lines: 2 to train, 1 to dev, 1 to test
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

testFolder = os.path.join(os.path.join(folder, "split"), "test")
os.system("mkdir " + testFolder)


# HERE


# Treat the corpus
fileNb = 0  # Initialize file counter

# Open the metadata file "TableOfContent.tsv" which contains information about the corpus
with open(os.path.join(folder, "TableOfContent.tsv"), newline='', encoding="utf-8") as metadataFile:
    reader = csv.DictReader(metadataFile, delimiter='\t', quotechar='"')  # Read as dictionary

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

                csvTestFile = open(os.path.join(testFolder, row["file"]), 'w', newline='', encoding="utf-8")
                testWriter = csv.writer(csvTestFile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                # Output files dictionary for easy reference
                outputFiles = {"train": trainWriter, "dev": devWriter, "test": testWriter}

                inputLineNb = 0  # Track the number of input lines processed
                outputLineNb = 0  # Track the number of output lines written

                # Process each line in the input file
                for line in spamreader:
                    inputLineNb += 1  # Increment input line count
                    
                    # Use the first column (original word) if no correction exists
                    subset = subcorpora[row["Sub-corpus"]][outputLineNb % len(subcorpora[row["Sub-corpus"]])]

                    # Write the original word and normalized second column
                    outputFiles[subset].writerow([line[0], line[1].replace("'", "’")])

                    outputLineNb += 1  # Increment output line count

                # Close all output files after processing
                csvTrainFile.close()
                csvDevFile.close()
                csvTestFile.close()

        except (OSError):
            # Handle errors if the file is not found
            print("Error: file not found")
            pass

