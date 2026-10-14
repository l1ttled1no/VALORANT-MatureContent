import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import shutil
import glob
import threading
import webbrowser
from pathlib import Path
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class VALORANTMatureContentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VALORANT Mature Content Manager")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variables
        self.destination_path = tk.StringVar()
        self.is_running = False
        
        # Set default destination path to VALORANT installation
        self.destination_path.set("C:/Riot Games/VALORANT/live/ShooterGame/Content/Paks")
        
        self.setup_menu()
        self.setup_ui()
        
    def setup_menu(self):
        """Setup the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select VALORANT Path...", command=self.browse_destination)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Check Files", command=self.check_files)
        tools_menu.add_command(label="Clear Output", command=self.clear_output)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def show_about(self):
        """Show about dialog"""
        about_text = """VALORANT Mature Content Manager

A GUI tool for managing VALORANT mature content files.

Created by: L11tled1no
Version: 1.0

This tool helps you apply mature content modifications
to your VALORANT installation safely and easily."""
        
        messagebox.showinfo("About", about_text)
        
    def setup_ui(self):
        """Setup the user interface"""
        # Set window icon to VALORANT emblem
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'logo', 'vlr.jpg')
            if os.path.exists(icon_path):
                if PIL_AVAILABLE:
                    # Use PIL to handle JPG format
                    pil_image = Image.open(icon_path)
                    
                    # Get original dimensions
                    width, height = pil_image.size
                    
                    # Resize to appropriate icon size while maintaining aspect ratio
                    target_size = 32  # Standard icon size
                    if width > height:
                        new_width = target_size
                        new_height = int((height * target_size) / width)
                    else:
                        new_height = target_size
                        new_width = int((width * target_size) / height)
                    
                    # Resize the image maintaining aspect ratio
                    resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage for tkinter
                    icon = ImageTk.PhotoImage(resized_image)
                    
                    self.root.iconphoto(True, icon)
                    # Keep references to prevent garbage collection
                    self.root.icon = icon
                    self.root.pil_image = pil_image
                else:
                    # PIL not available, try with tkinter PhotoImage (limited format support)
                    original_icon = tk.PhotoImage(file=icon_path)
                    
                    # Get original dimensions
                    width = original_icon.width()
                    height = original_icon.height()
                    
                    # Resize to appropriate icon size while maintaining aspect ratio
                    target_size = 32  # Standard icon size
                    if width > height:
                        new_width = target_size
                        new_height = int((height * target_size) / width)
                    else:
                        new_height = target_size
                        new_width = int((width * target_size) / height)
                    
                    # Create resized icon maintaining aspect ratio
                    icon = original_icon.subsample(max(1, width // new_width), max(1, height // new_height))
                    
                    self.root.iconphoto(True, icon)
                    # Keep references to prevent garbage collection
                    self.root.icon = icon
                    self.root.original_icon = original_icon
        except Exception as e:
            # If icon loading fails, continue without icon
            print(f"Could not load icon: {e}")
            if not PIL_AVAILABLE:
                print("Tip: Install Pillow library for better image format support: pip install Pillow")
            
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="VALORANT Mature Content Manager", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Destination path selection
        ttk.Label(main_frame, text="VALORANT Installation Path:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        path_frame.columnconfigure(0, weight=1)
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.destination_path, width=60)
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(path_frame, text="Browse", command=self.browse_destination).grid(row=0, column=1)
        
        # Status frame with progress bar
        status_frame = ttk.LabelFrame(main_frame, text="Progress", padding="5")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        
        # Create a frame to overlay text on progress bar
        progress_container = ttk.Frame(status_frame)
        progress_container.grid(row=0, column=0, sticky=(tk.W, tk.E))
        progress_container.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_container, mode='determinate', maximum=100, length=400)
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=8, ipady=8)
        
        # Configure progress bar style to be green
        style = ttk.Style()
        style.configure("Green.Horizontal.TProgressbar", 
                       background='green',
                       troughcolor='lightgray',
                       borderwidth=1, 
                       relief='solid')
        self.progress.configure(style="Green.Horizontal.TProgressbar")
        
        # Status label overlayed on progress bar with transparent background
        self.status_label = tk.Label(progress_container, text="Ready", 
                                    fg='black', 
                                    font=("Arial", 10, "bold"),
                                    relief='flat', borderwidth=0,
                                    highlightthickness=0)
        
        # Make the background transparent by not setting any background color
        # This allows the text to appear directly over the progress bar without a background
        try:
            # On Windows, we can achieve transparency by matching the parent's background
            # But first try to not set any background at all for true transparency
            parent_bg = progress_container.cget('bg')
            if parent_bg and parent_bg != 'SystemButtonFace':
                self.status_label.config(bg=parent_bg)
            # If parent_bg is the default system color, don't set background for transparency
        except:
            # If we can't determine the background, leave it unset for transparency
            pass
        
        self.status_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Output text area
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="5")
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, width=70)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        self.check_button = ttk.Button(button_frame, text="Check Files", command=self.check_files)
        self.check_button.grid(row=0, column=0, padx=(0, 10))
        
        self.run_button = ttk.Button(button_frame, text="Apply Mature Content", 
                                    command=self.run_script, style="Accent.TButton")
        self.run_button.grid(row=0, column=1, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear Output", command=self.clear_output)
        self.clear_button.grid(row=0, column=2)
        
        # Developer credit at bottom right
        self.add_developer_credit(main_frame)
    
    def validate_valorant_path(self, path):
        """Validate if the given path is a valid VALORANT installation directory"""
        if not path or not os.path.exists(path):
            return False
        
        pakchunk_file = os.path.join(path, "pakchunk2-WindowsClient.pak")
        return os.path.exists(pakchunk_file)
    
    def add_developer_credit(self, parent_frame):
        """Add developer credit link at bottom right"""
        
        # Create a frame for the credit at the bottom right
        credit_frame = ttk.Frame(parent_frame)
        credit_frame.grid(row=6, column=2, sticky="se", pady=(5, 0))
        
        # Create clickable link label
        credit_label = tk.Label(credit_frame, text="Developed by: @l1ttled1no", 
                               fg="blue", cursor="hand2", 
                               font=("Arial", 8, "underline"))
        credit_label.pack()
        
        # Bind click event to open GitHub profile
        def open_github(event):
            webbrowser.open("https://github.com/l1ttled1no")
        
        credit_label.bind("<Button-1>", open_github)
        
        # Add hover effect
        def on_enter(event):
            credit_label.config(fg="darkblue")
        
        def on_leave(event):
            credit_label.config(fg="blue")
        
        credit_label.bind("<Enter>", on_enter)
        credit_label.bind("<Leave>", on_leave)
    
    def update_progress(self, value, status_text=None):
        """Update progress bar value and optionally status text"""
        self.progress['value'] = value
        
        # Update status text if provided
        if status_text:
            self.status_label.config(text=status_text)
        
        # Keep text always black and bold
        self.status_label.config(fg='black')
        
        self.root.update_idletasks()
    
    def reset_progress(self, status_text="Ready"):
        """Reset progress bar to 0 and update status"""
        self.progress['value'] = 0
        self.status_label.config(text=status_text, fg='black')
        self.root.update_idletasks()
    
    def set_status(self, text):
        """Update only the status text without changing progress"""
        self.status_label.config(text=text)
    
    def log_message(self, message):
        """Add a message to the output text area"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    


    def browse_destination(self):
        """Open file dialog to select destination folder"""
        folder = filedialog.askdirectory(
            title="Select VALORANT Installation Directory",
            initialdir=self.destination_path.get()
        )
        if folder:
            # Validate that this is a VALORANT installation directory
            if not self.validate_valorant_path(folder):
                messagebox.showerror(
                    "Invalid VALORANT Path", 
                    f"This is not a valid VALORANT installation directory.\n\n"
                    f"Please select the correct VALORANT Paks directory:\n"
                    f"C:/Riot Games/VALORANT/live/ShooterGame/Content/Paks"
                )
                return
            
            self.destination_path.set(folder)
            self.log_message(f"✅ VALORANT installation path selected: {folder}")
    

    
    def check_files(self):
        """Check if the required files exist"""
        self.log_message("Checking files...")
        self.update_progress(0, "Checking files...")
        
        # Step 1: Check data files (50% progress)
        self.update_progress(25, "Checking data files...")
        data_files = glob.glob('./data/MatureData-WindowsClient.*')
        if not data_files:
            self.log_message("❌ Error: No MatureData-WindowsClient files found in ./data/ directory")
            self.reset_progress("Error: Data files not found")
            return False
        
        self.log_message(f"✅ Found {len(data_files)} MatureData files:")
        for file in data_files:
            self.log_message(f"  - {os.path.basename(file)}")
        
        self.update_progress(50, "Validating path...")
        
        # Step 2: Check destination path (100% progress)
        dest_path = self.destination_path.get()
        if not dest_path:
            self.log_message("❌ Error: No destination path specified")
            self.reset_progress("Error: No destination path")
            return False
        
        self.update_progress(75, "Checking destination...")
        
        if not os.path.exists(dest_path):
            self.log_message(f"❌ Error: Destination path not found: {dest_path}")
            self.reset_progress("Error: Invalid destination path")
            return False
        
        self.update_progress(85, "Validating VALORANT installation path...")
        
        # Check if this is a valid VALORANT installation directory
        if not self.validate_valorant_path(dest_path):
            self.log_message(f"❌ Error: This is not a valid VALORANT installation path, please check again.")
            self.log_message(f"❌ The directory should be:")
            self.log_message(f"   [Installation_Path]/Riot Games/VALORANT/live/ShooterGame/Content/Paks")
            self.reset_progress("Error: Not a VALORANT installation")
            return False
        
        self.log_message(f"✅ Destination path is valid: {dest_path}")
        self.log_message(f"✅ VALORANT installation verified")
        self.update_progress(100, "All checks passed ✓")
        return True
    
    def copy_data_files(self, destination_path):
        """Copy all MatureData-WindowsClient files to the destination"""
        data_files = glob.glob('./data/MatureData-WindowsClient.*')
        copied_files = []
        
        if not data_files:
            return False
        
        try:
            total_files = len(data_files)
            for i, file_path in enumerate(data_files):
                filename = os.path.basename(file_path)
                dest_file = os.path.join(destination_path, filename)
                shutil.copy2(file_path, dest_file)
                copied_files.append(dest_file)
                self.log_message(f"✅ Copied: {filename}")
                
                # Update progress based on files copied (0-70% of total progress)
                progress = int((i + 1) / total_files * 70)
                self.update_progress(progress, f"Copying files... ({i + 1}/{total_files})")
            
            self.log_message(f"✅ Successfully copied {len(copied_files)} files to {destination_path}")
            return True
        except Exception as e:
            self.log_message(f"❌ Error copying files: {e}")
            return False
    
    def remove_vng_files(self, destination_path):
        """Remove all VNGLogo-WindowsClient files from the destination"""
        vng_pattern = os.path.join(destination_path, 'VNGLogo-WindowsClient.*')
        vng_files = glob.glob(vng_pattern)
        
        # Update progress to 70% (after copying files)
        self.update_progress(70, "Searching for VNG files...")
        
        removed_count = 0
        if vng_files:
            total_files = len(vng_files)
            for i, file_path in enumerate(vng_files):
                try:
                    os.remove(file_path)
                    filename = os.path.basename(file_path)
                    self.log_message(f"🗑️ Removed: {filename}")
                    removed_count += 1
                    
                    # Update progress from 70% to 95% based on files removed
                    progress = 70 + int((i + 1) / total_files * 25)
                    self.update_progress(progress, f"Removing VNG files... ({i + 1}/{total_files})")
                except Exception as e:
                    self.log_message(f"❌ Error removing {file_path}: {e}")
        else:
            # No files to remove, jump to 95%
            self.update_progress(95, "No VNG files found")
        
        if removed_count == 0:
            self.log_message("ℹ️ No VNGLogo-WindowsClient files found to remove")
        else:
            self.log_message(f"✅ Successfully removed {removed_count} VNGLogo files")
    
    def run_script_thread(self):
        """Run the main script logic in a separate thread"""
        try:
            self.log_message("=" * 50)
            self.log_message("Starting VALORANT Mature Content application...")
            self.update_progress(0, "Initializing...")
            
            # Check files first (progress: 0-10%)
            self.update_progress(5, "Validating files...")
            if not self.check_files():
                return
            
            destination_path = self.destination_path.get()
            self.update_progress(10, "Starting operation...")
            
            # Copy MatureData files (progress: 10-70%)
            self.log_message("\n📁 Copying MatureData files...")
            if not self.copy_data_files(destination_path):
                return
            
            # Remove VNGLogo files (progress: 70-95%)
            self.log_message("\n🗑️ Removing VNGLogo files...")
            self.remove_vng_files(destination_path)
            
            # Complete (progress: 100%)
            self.update_progress(100, "🎉 Operation completed successfully!")
            self.log_message("\n🎉 Operation completed successfully!")
            
            # Show success message
            messagebox.showinfo("Success", "VALORANT Mature Content has been applied successfully!")
            
        except Exception as e:
            self.log_message(f"❌ Unexpected error: {e}")
            self.reset_progress("❌ Error occurred")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.is_running = False
            self.run_button.config(state="normal")
            self.check_button.config(state="normal")
    
    def run_script(self):
        """Start the script execution"""
        if self.is_running:
            return
        
        if not self.destination_path.get():
            messagebox.showerror("Error", "Please select a destination path first!")
            return
        
        # Confirm action
        result = messagebox.askyesno(
            "Confirm Action", 
            "This will modify your VALORANT installation.\n\nAre you sure you want to continue?"
        )
        if not result:
            return
        
        self.is_running = True
        self.update_progress(0, "Starting...")
        self.run_button.config(state="disabled")
        self.check_button.config(state="disabled")
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.run_script_thread)
        thread.daemon = True
        thread.start()

def main():
    """Main function to start the GUI"""
    root = tk.Tk()
    
    # Set up the style for better appearance
    style = ttk.Style()
    
    # Try to use a modern theme if available
    available_themes = style.theme_names()
    if 'vista' in available_themes:
        style.theme_use('vista')
    elif 'clam' in available_themes:
        style.theme_use('clam')
    
    app = VALORANTMatureContentGUI(root)
    
    # Center the window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
