import os
import hashlib
import json
import subprocess
from pathlib import Path

HASH_STORE_FILE = '.beautified_hashes.json'


def format_java_file(file_path, jar_path):
    try:
        # Run the google-java-format JAR to format the Java file
        subprocess.run(["java", "-jar", jar_path, "-i", file_path], check=True)
        print(f"Formatted: {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: Could not format {file_path}\n{e}")

def calculate_file_hash(filepath):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def load_hashes():
    """Load stored hashes from disk."""
    if not os.path.exists(HASH_STORE_FILE):
        return {}
    with open(HASH_STORE_FILE, 'r') as f:
        return json.load(f)

def save_hashes(hashes):
    """Save updated hashes to disk."""
    with open(HASH_STORE_FILE, 'w') as f:
        json.dump(hashes, f, indent=2)

def process_folder(folder_path, jar_path):
    hashes = load_hashes()
    folder_path = Path(folder_path)

    for filepath in folder_path.rglob("*.java"):  # Adjust extensions if needed
        if filepath.is_file():
            relative_path = str(filepath.relative_to(folder_path))
            current_hash = calculate_file_hash(filepath)

            if hashes.get(relative_path) != current_hash:
                print(f"Beautifying {relative_path}...")
                format_java_file(str(filepath), jar_path)  # Replace with actual beautification logic
                new_hash = calculate_file_hash(filepath)
                hashes[relative_path] = new_hash
            else:
                print(f"Skipping {relative_path} (no changes)")

    save_hashes(hashes)

jar_path = "google-java-format-1.23.0-all-deps.jar"

directory_path = "/home/gran-jacob/Projects/beecob/src/main/java/"

process_folder(directory_path, jar_path)
