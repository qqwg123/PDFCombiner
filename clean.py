import os
import shutil
import sys
import argparse

def clean_directories(verbose=False):
    """Clean build artifacts and temporary files"""
    # Define directories to clean
    dirs_to_clean = [
        'uploads',
        'build',
        'dist',
        '__pycache__',
        'app/__pycache__',
        'app/services/__pycache__',
        'app/utils/__pycache__',
    ]
    
    # Define files to clean
    files_to_clean = [
        'app.spec',
        '*.pyc',
        'app/*.pyc',
        'app/services/*.pyc',
        'app/utils/*.pyc',
    ]
    
    cleaned = False
    
    # Clean directories
    for dir_pattern in dirs_to_clean:
        for dir_path in _find_matching_paths(dir_pattern):
            if os.path.exists(dir_path):
                try:
                    if os.path.isdir(dir_path):
                        # For uploads folder, remove contents but keep folder
                        if dir_path == 'uploads':
                            for item in os.listdir(dir_path):
                                item_path = os.path.join(dir_path, item)
                                if os.path.isfile(item_path):
                                    os.remove(item_path)
                                    if verbose:
                                        print(f"Removed file: {item_path}")
                                elif os.path.isdir(item_path):
                                    shutil.rmtree(item_path)
                                    if verbose:
                                        print(f"Removed directory: {item_path}")
                            if verbose:
                                print(f"Cleaned contents of {dir_path}")
                        else:
                            # For other folders, remove entire folder
                            shutil.rmtree(dir_path)
                            if verbose:
                                print(f"Removed directory: {dir_path}")
                        cleaned = True
                except Exception as e:
                    print(f"Error cleaning {dir_path}: {e}")
    
    # Clean files
    for file_pattern in files_to_clean:
        for file_path in _find_matching_paths(file_pattern):
            if os.path.exists(file_path) and os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    if verbose:
                        print(f"Removed file: {file_path}")
                    cleaned = True
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")
    
    if not cleaned:
        print("Nothing to clean")
    else:
        print("Clean completed successfully")
    
    return True

def _find_matching_paths(pattern):
    """Find paths matching the given pattern"""
    import glob
    return glob.glob(pattern, recursive=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean project artifacts and temporary files")
    parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose output')
    args = parser.parse_args()
    
    success = clean_directories(args.verbose)
    sys.exit(0 if success else 1)