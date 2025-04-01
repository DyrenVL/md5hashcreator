import hashlib
import os
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm

def md5_of_file(file_path):
    """Generate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def hash_folder(folder_path, output_file):
    """Generate MD5 hashes for all files in a folder and save them to a text file with progress bar"""
    hashes = []
    files_list = []

    # Collect all files in the folder (including subfolders)
    for root, _, files in os.walk(folder_path):
        for file in files:
            files_list.append(os.path.join(root, file))
    
    # Sort files for consistency
    files_list.sort()

    with open(output_file, "w") as f, tqdm(total=len(files_list), desc="Hashing files", unit="file") as pbar:
        for file_path in files_list:
            file_hash = md5_of_file(file_path)
            relative_path = os.path.relpath(file_path, folder_path)
            hashes.append(f"{file_hash}  {relative_path}")
            f.write(f"{file_hash}  {relative_path}\n")
            pbar.update(1)

    # Generate a single MD5 for the entire folder based on its contents
    folder_md5 = hashlib.md5("\n".join(hashes).encode()).hexdigest()
    
    with open(output_file, "a") as f:
        f.write(f"\nFolder MD5: {folder_md5}\n")

    print(f"\nMD5 hashes saved to {output_file}")
    print(f"Folder MD5: {folder_md5}")

def select_folder():
    """Open a folder selection dialog and return the selected path"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory(title="Select Folder to Hash")
    return folder_selected

if __name__ == "__main__":
    print("Select the folder to hash...")
    folder_path = select_folder()
    
    if not folder_path:
        print("No folder selected. Exiting.")
    else:
        output_file = os.path.join(folder_path, "hashes.md5")
        hash_folder(folder_path, output_file)
