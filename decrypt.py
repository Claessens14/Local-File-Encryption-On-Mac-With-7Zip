import sys
import os
import subprocess
import secure_delete
import shutil
print("---------- DECRYPTION -----------")

target_file = ""
if len(sys.argv) != 2:
    target_file = input("Please enter the file or folder name: ")
else:
    target_file  = sys.argv[1]

# Check if it exists
if os.path.exists(target_file) == False:
    print(f"The file or folder '{target_file}' does not exist.")
    exit()

password = input("Enter your password: ")


# Construct the command
seven_zip_path = "/Users/jacobclaessens/Desktop/code/utils/7z2408-mac/7zz"
command = f"{seven_zip_path} x -p{password} {target_file}"

# Execute the command
try:
    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    print("\n\n   7-zip executed successfully!\n\n")
    print("     7-zip Output:", result.stdout + "\n")
except subprocess.CalledProcessError as e:
    print("An error occurred:", e.stderr)
    print("\n\nExiting Program\n\n")
    exit()

# Function to remove the .7z extension
def remove_extension(filename):
    # Check if the filename ends with .7z
    if filename.endswith('.7z'):
        # Remove the extension
        new_filename = filename[:-3]  # Removes the last 3 characters (.7z)
        return new_filename
    return filename  # Return the original filename if it doesn't have the .7z extension
# remove the .7z extension
decrypted_file_name = remove_extension(target_file)

# Derive the destination filename
def remove_encrypted(filename):
    # Split the filename into base and extension
    base, ext = os.path.splitext(filename)
    # Remove "ENCRYPTED" from the base name
    new_base = base.replace("_ENCRYPTED", "")
    # Create the new filename
    new_filename = f"{new_base}{ext}"
    # Check if the new filename already exists
    counter = 1
    while os.path.exists(new_filename):
        # If it exists, increment the counter and create a new filename
        new_filename = f"{new_base}_{counter}{ext}"
        counter += 1
    return new_filename
import ipdb; ipdb.set_trace()
# remove the word ENCRYPTED from the output file
destination = remove_encrypted(decrypted_file_name)

# create a normal output filename
#os.rename(decrypted_file_name, destination)

# Delete the old {name}_ENCRYPTED.7z file
secure_delete.secure_delete_path(target_file)

print("---------------------------------")
