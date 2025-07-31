# VALORANT Mature Content Manager - GUI Version

## Requirements
- Python 3.6 or higher
- tkinter (usually comes with Python)

## How to Run

### Method 1: Double-click the batch file
1. Double-click `run_gui.bat`

### Method 2: Command line
1. Open Command Prompt or PowerShell
2. Navigate to this directory
3. Run: `python gui_script.py`

## Features

- **User-friendly GUI**: Easy-to-use interface with buttons and progress indicators
- **Path Selection**: Browse and select your VALORANT installation directory
- **File Checking**: Verify that all required files are present before proceeding
- **Real-time Output**: See the progress and results in the output window
- **Contribution Display**: Shows contribution message in a popup dialog
- **Error Handling**: Clear error messages and confirmations

## Usage

1. **Launch the application** using one of the methods above
2. **Read the contribution message** that appears in a popup window
3. **Select your VALORANT installation path** using the Browse button
4. **Check files** to verify everything is ready
5. **Apply Mature Content** to copy the files and remove VNG logos

## GUI Components

- **Path Selection**: Browse for your VALORANT installation directory
- **Status Bar**: Shows current operation status
- **Progress Bar**: Indicates when operations are running
- **Output Window**: Displays detailed logs of all operations
- **Buttons**:
  - `Check Files`: Verify required files exist
  - `Apply Mature Content`: Run the main operation
  - `Clear Output`: Clear the output window

## Safety Features

- Confirmation dialog before making changes
- File existence verification
- Path validation
- Error handling with user-friendly messages
- Threading to prevent GUI freezing during operations

The GUI version provides the same functionality as the original script but with a much more user-friendly interface.
