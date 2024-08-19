import os

# Set the directory path
directory = "."

# Set the output file name
output_file = "concatenated_code.txt"

# Get a list of all files in the directory
files = os.listdir(directory)

# Open the output file in write mode
with open(output_file, "w", encoding="utf-8") as output:
    # Iterate over each file in the directory
    for file in files:
        # Get the full file path
        file_path = os.path.join(directory, file)
        
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(file_path):
            try:
                # Open the file in read mode with UTF-8 encoding
                with open(file_path, "r", encoding="utf-8") as f:
                    # Write the file name as a comment
                    output.write(f"// File: {file}\n")
                    
                    # Write the file content
                    output.write(f.read())
                    
                    # Add a newline separator
                    output.write("\n\n")
            except UnicodeDecodeError:
                print(f"Skipping file '{file}' due to encoding error.")

print("Concatenation complete. Output file:", output_file)