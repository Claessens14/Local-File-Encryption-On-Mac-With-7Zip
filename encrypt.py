import sys
import os
import subprocess
import secure_delete
import getpass
from dotenv import load_dotenv
load_dotenv()

print("---------- ENCRYPTION -----------")

# Get the target folder name
target_file = ""
if len(sys.argv) != 2:
    target_file = input("Please enter the file or folder name: ")
else:
    target_file  = sys.argv[1]

# Check if it exists
if os.path.exists(target_file) == False:
    print(f"The file or folder '{target_file}' does not exist.")
    exit()

# get the destination folder name
def append_encrypted(filename):
    # Split the filename into name and extension
    base, ext = os.path.splitext(filename)
    # Create the new filename with "ENCRYPTED"
    new_filename = f"{base}_ENCRYPTED{ext}"
    # Check if the new filename already exists
    counter = 1
    while os.path.exists(new_filename):
        # If it exists, increment the counter and create a new filename
        new_filename = f"{base}_ENCRYPTED_{counter}{ext}"
        counter += 1
    return new_filename
destination = append_encrypted(target_file)
destination = f"{destination}.7z"
# Check if destination exists
if os.path.exists(destination):
    print(f"The file or folder '{destination}' already exists.")
    print(f"Exiting program")
    exit()

# Get the password
password = getpass.getpass("Enter your password: ")
verification2 = getpass.getpass("(2nd Entry) Verify the correct spelling: ")
if verification2 != password:
    print("\n\n Passwords do not match! Exiting Program\n\n")
    exit()
verification3 = getpass.getpass("(3rd Entry) Verify the correct spelling: ")
if verification3 != password:
    print("\n\n Passwords (3rd Entry) do not match! Exiting Program\n\n")
    exit()

# Run 7-zip
seven_zip_path = os.getenv("SEVEN_ZIP_PATH")
command = f"{seven_zip_path} a -t7z -mhe=on  -p{password} {destination} {target_file}"
print(command)
try:
    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    print("\n\n   7-zip executed successfully!\n\n")
    print("     7-zip Output:", result.stdout + "\n")
except subprocess.CalledProcessError as e:
    print("An error occurred:", e.stderr)
    print("\n\nExiting Program\n\n")
    exit()

# overwrite and delete
if os.path.exists(destination):
    secure_delete.secure_delete_path(target_file)

print("--------------------------------")
