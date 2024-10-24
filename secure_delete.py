import os
import random
import shutil


def secure_delete(file_path):
    """Securely delete a file by overwriting it."""
    if os.path.isfile(file_path):
        try:
            # Try to change permissions first
            subprocess.run(f"sudo chmod 777 {file_path}", shell=True, check=True)

            # Get the size of the file
            size = os.path.getsize(file_path)

            # Overwrite the file with random data
            with open(file_path, "r+b") as f:
                f.write(os.urandom(size))

            # Delete the file
            os.remove(file_path)
            print(f"Securely deleted: {file_path}")
        except PermissionError:
            # If permission error occurs, try secure deletion with sudo
            try:
                # First overwrite the file
                subprocess.run(f"sudo dd if=/dev/urandom of={file_path} bs={size} count=1",
                             shell=True, check=True)
                # Then remove it
                subprocess.run(f"sudo rm -f {file_path}", shell=True, check=True)
                print(f"Securely deleted with elevated privileges: {file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error securely deleting {file_path} with elevated privileges: {str(e)}")
        except Exception as e:
            print(f"Error securely deleting {file_path}: {str(e)}")
    else:
        print(f"File not found: {file_path}")

def secure_delete_folder(folder_path):
    """Securely delete all files in a folder and its subdirectories."""
    if os.path.isdir(folder_path):
        try:
            # First try to change permissions on the entire directory
            subprocess.run(f"sudo chmod -R 777 {folder_path}", shell=True, check=True)

            # Create a list of all files and directories first
            items_to_process = []
            for root, dirs, files in os.walk(folder_path, topdown=False):
                # Add all files to be processed
                for filename in files:
                    items_to_process.append(os.path.join(root, filename))
                # Add all directories to be processed
                for dirname in dirs:
                    items_to_process.append(os.path.join(root, dirname))

            # Process all files first
            for item in items_to_process:
                if os.path.isfile(item):
                    secure_delete(item)
                elif os.path.isdir(item):
                    try:
                        os.rmdir(item)
                        print(f"Removed empty directory: {item}")
                    except OSError:
                        # If regular removal fails, try with sudo
                        try:
                            subprocess.run(f"sudo rm -d {item}", shell=True, check=True)
                            print(f"Removed empty directory with elevated privileges: {item}")
                        except subprocess.CalledProcessError as e:
                            print(f"Error removing directory {item} with elevated privileges: {str(e)}")

            # Finally remove the root folder
            try:
                os.rmdir(folder_path)
                print(f"Removed root directory: {folder_path}")
            except OSError:
                # If regular removal fails, try with sudo
                try:
                    subprocess.run(f"sudo rm -d {folder_path}", shell=True, check=True)
                    print(f"Removed root directory with elevated privileges: {folder_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error removing root directory {folder_path} with elevated privileges: {str(e)}")

        except Exception as e:
            # If all above fails, try the nuclear option with rm -rf
            try:
                subprocess.run(f"sudo rm -rf {folder_path}", shell=True, check=True)
                print(f"Removed directory tree with elevated privileges: {folder_path}")
            except subprocess.CalledProcessError as e:
                print(f"Fatal error processing folder {folder_path}: {str(e)}")

def secure_delete_path(path):
    """Determine if the path is a file or folder and securely delete it."""
    try:
        # Resolve any symlinks to get the real path
        real_path = str(Path(path).resolve())
        if os.path.isfile(real_path):
            secure_delete(real_path)
        elif os.path.isdir(real_path):
            secure_delete_folder(real_path)
        else:
            print(f"Path not found: {real_path}")
    except Exception as e:
        print(f"Error processing path {path}: {str(e)}")
