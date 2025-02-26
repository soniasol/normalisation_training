import os
import pandas as pd
from itertools import cycle

# fill in the path to the folder
folder = "/Users/sonia/..."
folder = "..."

# Read metadata file using pandas
table_of_content_path = os.path.join(folder, "table.csv")
metadata_df = pd.read_csv(table_of_content_path, delimiter='\t', quotechar='"')

fileNb = 0  # File counter to keep track of processed files

# Define a fixed cycle pattern for assigning lines to train, dev, and test sets
subset_cycle = cycle(
    [
    "train", "train", "train", "train", "test", "train", "train", "train", "dev",
    "train", "train", "train", "train", "test", "train", "train", "dev", "train", "test"
    ]
    )

# Iterate through each row in the metadata file
for _, row in metadata_df.iterrows():
    fileNb += 1  # Increment file counter
    print(f"Treating file #{fileNb} ({row['file']})")
    
    try:
        # Read the corresponding text file using pandas
        text_file_path = os.path.join(folder, "corpus", row["file"])
        text_df = pd.read_csv(text_file_path, delimiter='\t', quotechar='"', header=None)
        
        # Define output file paths for train, dev, and test sets
        train_file_path = os.path.join(trainFolder, row["file"])
        dev_file_path = os.path.join(devFolder, row["file"])
        test_file_path = os.path.join(testFolder, row["file"])
        
        # Prepare lists to store processed data for different sets
        # we will transform these lists to Pandas Dataframes later
        train_data, dev_data, test_data = [], [], []
        
        inputLineNb = 0  # Counter for tracking number of input lines processed

        # Iterate through each line in the input text file
        # here, line is a row of the table (with 2 or more columns)
        # so that line[0] is the first column, line[1] is the second, and so on
        for _, line in text_df.iterrows():
            inputLineNb += 1  # Increment input line count
            
            # Get the next subset (train/dev/test) in a simplified way
            subset = next(subset_cycle)
            
            # no need for if-else (Simon's script) since we have only two columns
            processed_line = [line[0], line[1].replace("'", "’")]  # Use original word
            
            # Store the processed line in the appropriate dataset
            if subset == "train":
                train_data.append(processed_line)
            elif subset == "dev":
                dev_data.append(processed_line)
            elif subset == "test":
                test_data.append(processed_line)
        
        # Write processed data to respective output files
        # transform the lists into dataframes ready to be saved
        pd.DataFrame(train_data).to_csv(train_file_path, sep='\t', index=False, header=False, quotechar='"')
        pd.DataFrame(dev_data).to_csv(dev_file_path, sep='\t', index=False, header=False, quotechar='"')
        pd.DataFrame(test_data).to_csv(test_file_path, sep='\t', index=False, header=False, quotechar='"')
    
    except FileNotFoundError:
        # Handle missing file errors gracefully
        print("Error: file not found")
        pass
