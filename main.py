import os
import subprocess
from pathlib import Path
from datetime import datetime
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
import queue
import time

def get_file_date(file_path):
    try:
        result = subprocess.run(
            ["exiftool", "-DateTimeOriginal", "-s", "-s", "-s", str(file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        date_str = result.stdout.strip()
        if date_str:
            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error getting date for {file_path}: {e}")
    return None

def generate_target_directory(file_date, levels):
    parts = []
    for level in levels:
        if level == "Year":
            parts.append("Year")
        elif level == "year":
            parts.append("year")
        elif level == "YYYY":
            parts.append(str(file_date.year))
        elif level == "YY":
            parts.append(file_date.strftime("%y"))
        elif level == "Month":
            parts.append(file_date.strftime("%B"))
        elif level == "month":
            parts.append(file_date.strftime("%B").lower())
        elif level == "Mon":
            parts.append(file_date.strftime("%b"))
        elif level == "mon":
            parts.append(file_date.strftime("%b").lower())
        elif level == "MM":
            parts.append(file_date.strftime("%m"))
        elif level == "DD":
            parts.append(file_date.strftime("%d"))
        elif level == "YYYY-MM-DD":
            parts.append(file_date.strftime("%Y-%m-%d"))

    return "/".join(parts)

def rename_file(file_path, strategy, file_date):
    if strategy == "Add Date Prefix":
        new_name = file_date.strftime("%Y%m%d_") + file_path.name
    elif strategy == "Add Date Suffix":
        new_name = file_path.stem + "_" + file_date.strftime("%Y%m%d") + file_path.suffix
    elif strategy == "Replace with Date":
        new_name = file_date.strftime("%Y%m%d") + file_path.suffix
    elif strategy == "Original Name":
        new_name = file_path.name

    return new_name

def move_file(file_path, destination_dir, duplicates_dir, unknown_dir, levels, rename_strategy, q):
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    
    file_date = get_file_date(file_path)
    
    if file_date:
        target_dir = destination_dir / generate_target_directory(file_date, levels)
    else:
        target_dir = unknown_dir

    target_dir.mkdir(parents=True, exist_ok=True)

    new_name = rename_file(file_path, rename_strategy, file_date) if file_date else file_path.name
    target_file = target_dir / new_name
    
    if target_file.exists():
        print(f"Duplicate found: {file_path.name}")
        target_file = duplicates_dir / new_name
        counter = 1
        while target_file.exists():
            target_file = duplicates_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1

    try:
        shutil.move(str(file_path), str(target_file))
        print(f"Moved: {file_path} -> {target_file}")
    except Exception as e:
        print(f"Error moving file {file_path}: {e}")
    finally:
        q.put(1)  # Increment the queue by 1 to indicate progress

def process_files(source_dir, destination_dir, levels, selected_extensions, progress_var, progress_label, q, delete_empty, duplicates_dir, unknown_dir, rename_strategy):
    file_list = []
    total_files = 0
    processed_files = 0
    start_time = time.time()

    for root, dirs, files in os.walk(source_dir):
        # Skip the Recycle Bin and system directories
        dirs[:] = [d for d in dirs if d not in ["$RECYCLE.BIN", "System Volume Information"]]
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in selected_extensions:
                file_list.append(file_path)
                total_files += 1

    for file_path in file_list:
        move_file(file_path, destination_dir, duplicates_dir, unknown_dir, levels, rename_strategy, q)
        processed_files += q.get()

        # Time estimation
        elapsed_time = time.time() - start_time
        if processed_files > 0 and total_files > 0:
            remaining_time = (elapsed_time / processed_files) * (total_files - processed_files)
            hours, rem = divmod(remaining_time, 3600)
            minutes, seconds = divmod(rem, 60)
            time_left = f"Time left: {int(hours)}h {int(minutes)}m {int(seconds)}s"
        else:
            time_left = "Time left: Calculating..."

        progress_var.set((processed_files / total_files) * 100 if total_files > 0 else 100)
        progress_label.config(text=f"Processed: {processed_files}/{total_files} files | {time_left}")
        print(f"Processed {file_path.name}")

    if delete_empty and not any(os.scandir(source_dir)):
        try:
            shutil.rmtree(source_dir)
            print(f"Deleted empty source folder: {source_dir}")
        except Exception as e:
            print(f"Error deleting source folder: {e}")

    messagebox.showinfo("Completed", "File processing completed successfully!")

def add_level(default_value="YYYY"):
    level_var = tk.StringVar(value=default_value)
    levels_frame = ttk.Frame(levels_container)
    levels_frame.grid(sticky=(tk.W, tk.E))
    ttk.Label(levels_frame, text="Level:").grid(row=0, column=0, sticky=tk.W)
    level_dropdown = ttk.Combobox(levels_frame, textvariable=level_var, values=[
        "Year", "year", "YYYY", "YY", "Month", "month", "Mon", "mon", "MM", "DD", "YYYY-MM-DD"
    ])
    level_dropdown.grid(row=0, column=1, sticky=(tk.W, tk.E))
    ttk.Button(levels_frame, text="Remove", command=levels_frame.destroy).grid(row=0, column=2, sticky=tk.W)
    level_vars.append(level_var)

def start_processing():
    source_dir = Path(source_dir_entry.get())
    destination_dir = Path(dest_dir_entry.get())
    selected_extensions = [ext for ext, var in filetype_vars.items() if var.get()]
    delete_empty = delete_empty_var.get()

    levels = [var.get() for var in level_vars]
    rename_strategy = rename_strategy_var.get()

    # Ensure Duplicates and Unknown folders are top-level in the destination directory
    duplicates_dir = destination_dir / "Duplicates"
    unknown_dir = destination_dir / "Unknown"

    if not source_dir.exists() or not destination_dir.exists():
        messagebox.showerror("Error", "Please select valid source and destination directories.")
        return

    q = queue.Queue()

    thread = Thread(target=process_files, args=(source_dir, destination_dir, levels, selected_extensions, progress_var, progress_label, q, delete_empty, duplicates_dir, unknown_dir, rename_strategy))
    thread.start()

def exit_application():
    root.quit()
    root.destroy()

# UI setup
root = tk.Tk()
root.title("Photo Organizer")
root.geometry("800x600")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Source directory selection
ttk.Label(frame, text="Source Directory:").grid(row=0, column=0, sticky=tk.W)
source_dir_entry = ttk.Entry(frame, width=40)
source_dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
ttk.Button(frame, text="Browse", command=lambda: source_dir_entry.delete(0, tk.END) or source_dir_entry.insert(0, filedialog.askdirectory())).grid(row=0, column=2, sticky=tk.W)

# Destination directory selection
ttk.Label(frame, text="Destination Directory:").grid(row=1, column=0, sticky=tk.W)
dest_dir_entry = ttk.Entry(frame, width=40)
dest_dir_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
ttk.Button(frame, text="Browse", command=lambda: dest_dir_entry.delete(0, tk.END) or dest_dir_entry.insert(0, filedialog.askdirectory())).grid(row=1, column=2, sticky=tk.W)

# Dynamic folder structure levels
ttk.Label(frame, text="Folder Structure Levels:").grid(row=2, column=0, sticky=tk.W)
levels_container = ttk.Frame(frame)
levels_container.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
ttk.Button(frame, text="Add Level", command=add_level).grid(row=4, column=0, sticky=tk.W)
level_vars = []

# Add initial levels for YYYY/Month/YYYY-MM-DD
add_level("YYYY")
add_level("Month")
add_level("YYYY-MM-DD")

# File renaming strategy
ttk.Label(frame, text="File Renaming Strategy:").grid(row=5, column=0, sticky=tk.W)
rename_strategy_var = tk.StringVar(value="Original Name")
rename_strategy_dropdown = ttk.Combobox(frame, textvariable=rename_strategy_var, values=["Original Name", "Add Date Prefix", "Add Date Suffix", "Replace with Date"])
rename_strategy_dropdown.grid(row=5, column=1, sticky=(tk.W, tk.E))

# File type selection
ttk.Label(frame, text="Select File Types:").grid(row=6, column=0, sticky=tk.W)
filetype_vars = {}
filetypes = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".raw", ".cr2", ".nef", ".orf", ".sr2", ".heic", ".arw", ".mp4", ".mov", ".avi", ".mkv", ".mts", ".m2ts", ".3gp"]

filetype_frame = ttk.Frame(frame)
filetype_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))
for i, ext in enumerate(filetypes):
    var = tk.BooleanVar(value=True)
    chk = ttk.Checkbutton(filetype_frame, text=ext, variable=var)
    chk.grid(row=i//5, column=i%5, sticky=tk.W)
    filetype_vars[ext] = var

# Duplicates and Unknown folders location (Top-level in the destination directory by default)
ttk.Label(frame, text="Duplicates Folder Location:").grid(row=8, column=0, sticky=tk.W)
duplicates_dir_entry = ttk.Entry(frame, width=40)
duplicates_dir_entry.grid(row=8, column=1, sticky=(tk.W, tk.E))
duplicates_dir_entry.insert(0, "Duplicates")  # Default to "Duplicates" in the destination directory
ttk.Button(frame, text="Browse", command=lambda: duplicates_dir_entry.delete(0, tk.END) or duplicates_dir_entry.insert(0, filedialog.askdirectory())).grid(row=8, column=2, sticky=tk.W)

ttk.Label(frame, text="Unknown Folder Location:").grid(row=9, column=0, sticky=tk.W)
unknown_dir_entry = ttk.Entry(frame, width=40)
unknown_dir_entry.grid(row=9, column=1, sticky=(tk.W, tk.E))
unknown_dir_entry.insert(0, "Unknown")  # Default to "Unknown" in the destination directory
ttk.Button(frame, text="Browse", command=lambda: unknown_dir_entry.delete(0, tk.END) or unknown_dir_entry.insert(0, filedialog.askdirectory())).grid(row=9, column=2, sticky=tk.W)

# Option to delete empty source folder
delete_empty_var = tk.BooleanVar(value=False)
delete_empty_chk = ttk.Checkbutton(frame, text="Delete Source Folder if Empty", variable=delete_empty_var)
delete_empty_chk.grid(row=10, column=0, columnspan=3, sticky=tk.W)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100)
progress_bar.grid(row=11, column=0, columnspan=3, sticky=(tk.W, tk.E))

# Progress label
progress_label = ttk.Label(frame, text="Ready to start")
progress_label.grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E))

# Start button
start_button = ttk.Button(frame, text="Start", command=start_processing)
start_button.grid(row=13, column=0, sticky=tk.W)

# Exit button
exit_button = ttk.Button(frame, text="Exit", command=exit_application)
exit_button.grid(row=13, column=2, sticky=tk.E)

# Adjust grid weights for proper resizing
frame.columnconfigure(1, weight=1)
frame.rowconfigure(0, weight=1)

# Start the main loop
root.mainloop()
