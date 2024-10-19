import os
import random
import shutil

def secure_delete(file_path):
    """Securely delete a file by overwriting it."""
    if os.path.isfile(file_path):
        # Get the size of the file
        size = os.path.getsize(file_path)
        
        # Overwrite the file with random data
        with open(file_path, "r+b") as f:
            f.write(os.urandom(size))
        
        # Delete the file
        os.remove(file_path)
        print(f"Securely deleted: {file_path}")
    else:
        print(f"File not found: {file_path}")

def secure_delete_folder(folder_path):
    """Securely delete all files in a folder, including hidden files."""
    if os.path.isdir(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                secure_delete(file_path)
            # Remove directories after processing files
            for dirname in dirs:
                dir_path = os.path.join(root, dirname)
                shutil.rmtree(dir_path)  # Remove directories recursively
                print(f"Removed directory: {dir_path}")
        shutil.rmtree(folder_path)
        print(f"Securely deleted all files in: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")

def secure_delete_path(path):
    """Determine if the path is a file or folder and securely delete it."""
    if os.path.isfile(path):
        secure_delete(path)
    elif os.path.isdir(path):
        secure_delete_folder(path)
    else:
        print(f"Path not found: {path}")

