import os
import shutil
import sys
import argparse

def clean_directories():
    """Clean build artifacts and temporary files"""
    # Define directories to clean
    dirs_to_clean = [
        os.path.join('backend', 'uploads'),
        'build',
        'dist'
    ]
    
    # Define files to clean
    files_to_clean = [
        'app.spec'
    ]
    
    cleaned = False
    
    # Clean directories
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            try:
                if os.path.isdir(dir_path):
                    # For uploads folder, remove contents but keep folder
                    if dir_path == os.path.join('backend', 'uploads'):
                        for item in os.listdir(dir_path):
                            item_path = os.path.join(dir_path, item)
                            if os.path.isfile(item_path):
                                os.remove(item_path)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                        print(f"Cleaned contents of {dir_path}")
                    else:
                        # For other folders, remove entire folder
                        shutil.rmtree(dir_path)
                        print(f"Removed {dir_path}")
                cleaned = True
            except Exception as e:
                print(f"Error cleaning {dir_path}: {e}")
                return False
    
    # Clean files
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed {file_path}")
                cleaned = True
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
                return False
    
    if not cleaned:
        print("Nothing to clean")
    else:
        print("Clean completed successfully")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean project artifacts and temporary files")
    parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose output')
    args = parser.parse_args()
    
    success = clean_directories()
    sys.exit(0 if success else 1)