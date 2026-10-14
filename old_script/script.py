import os
import shutil
import glob
from pathlib import Path

def read_destination_path():
    """Read the destination path from path.txt file"""
    try:
        with open('./path.txt', 'r') as file:
            destination_path = file.read().strip()
            if not os.path.exists(destination_path):
                print(f"Error: Destination path not found: {destination_path}")
                return None
            return destination_path
    except FileNotFoundError:
        print("Error: path.txt file not found")
        return None
    except Exception as e:
        print(f"Error reading path.txt: {e}")
        return None

def check_data_files():
    """Check if the required MatureData files exist"""
    data_files = glob.glob('./data/MatureData-WindowsClient.*')
    if not data_files:
        print("Error: No MatureData-WindowsClient files found in ./data/ directory")
        return False
    
    print(f"Found {len(data_files)} MatureData files:")
    for file in data_files:
        print(f"  - {file}")
    return True 

def copy_data_files(destination_path):
    """Copy all MatureData-WindowsClient files to the destination"""
    data_files = glob.glob('./data/MatureData-WindowsClient.*')
    copied_files = []
    
    try:
        for file_path in data_files:
            filename = os.path.basename(file_path)
            dest_file = os.path.join(destination_path, filename)
            shutil.copy2(file_path, dest_file)
            copied_files.append(dest_file)
            print(f"Copied: {filename}")
        
        print(f"Successfully copied {len(copied_files)} files to {destination_path}")
        return True
    except Exception as e:
        print(f"Error copying files: {e}")
        return False

def remove_vng_files(destination_path):
    """Remove all VNGLogo-WindowsClient files from the destination"""
    vng_pattern = os.path.join(destination_path, 'VNGLogo-WindowsClient.*')
    vng_files = glob.glob(vng_pattern)
    
    removed_count = 0
    for file_path in vng_files:
        try:
            os.remove(file_path)
            filename = os.path.basename(file_path)
            print(f"Removed: {filename}")
            removed_count += 1
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
    
    if removed_count == 0:
        print("No VNGLogo-WindowsClient files found to remove")
    else:
        print(f"Successfully removed {removed_count} VNGLogo files")

def show_contribution():
    """Show contribution message if the file exists"""
    contribution_file = './data/Contribution'
    if os.path.exists(contribution_file):
        try:
            with open(contribution_file, 'r', encoding='utf-8') as file:
                content = file.read()
                print(content)
                print("\nDo you wish to continue? (Y/N - Y is default)")
                response = input().strip().lower()
                if response in ['n', 'no']:
                    print("Thank you for using the script. L11tled1no.")
                    return False
        except Exception as e:
            print(f"Error reading contribution file: {e}")
    return True

def main():
    """Main function to execute the script"""
    print("VALORANT Mature Content Script")
    print("=" * 40)
    
    # Show contribution message
    if not show_contribution():
        return
    
    # Check if data files exist
    if not check_data_files():
        return
    
    # Read destination path
    destination_path = read_destination_path()
    if not destination_path:
        return
    
    print(f"\nDestination path: {destination_path}")
    
    # Copy MatureData files
    print("\nCopying MatureData files...")
    if not copy_data_files(destination_path):
        return
    
    # Remove VNGLogo files
    print("\nRemoving VNGLogo files...")
    remove_vng_files(destination_path)
    
    print("\nOperation completed successfully!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

