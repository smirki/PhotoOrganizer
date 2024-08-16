# Photo Organizer

A powerful and user-friendly tool to organize your photos by extracting EXIF data, renaming files based on dates, and sorting them into structured directories.

## Table of Contents

1. [Installation](#installation)
   - [Requirements](#requirements)
   - [Installation on Windows](#installation-on-windows)
   - [Installation on macOS](#installation-on-macos)
   - [Installation on Linux](#installation-on-linux)
2. [Usage](#usage)
   - [Starting the Application](#starting-the-application)
   - [Using the Interface](#using-the-interface)
   - [Configuring the Application](#configuring-the-application)
3. [Debugging](#debugging)
   - [Common Issues and Solutions](#common-issues-and-solutions)
   - [Logging](#logging)
4. [Contributing](#contributing)
5. [License](#license)

## Installation

### Requirements

- Python 3.8 or higher
- `pip` for managing Python packages
- `exiftool` (for extracting EXIF data from images)

### Installation on Windows

1. **Download and Install Python:**

   Download Python from the [official Python website](https://www.python.org/downloads/). Ensure that the option to add Python to your PATH is selected during installation.

2. **Install Required Python Packages:**

   Open a command prompt and navigate to your project directory. Run the following command to install the necessary packages:

   ```sh
   pip install -r requirements.txt
   ```

3. **Install `exiftool`:**

   - Download the Windows executable from the [ExifTool website](https://exiftool.org/).
   - Follow the instructions on the website to install `exiftool` and ensure it is added to your system PATH.

### Installation on macOS

1. **Download and Install Python:**

   Python is typically pre-installed on macOS. To ensure you have the latest version, you can use [Homebrew](https://brew.sh/) to install it:

   ```sh
   brew install python
   ```

2. **Install Required Python Packages:**

   Open Terminal and navigate to your project directory. Run:

   ```sh
   pip install -r requirements.txt
   ```

3. **Install `exiftool`:**

   Install `exiftool` using Homebrew:

   ```sh
   brew install exiftool
   ```

### Installation on Linux

1. **Download and Install Python:**

   Python is usually pre-installed on most Linux distributions. To install or update Python, use your package manager. For example, on Ubuntu:

   ```sh
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   ```

2. **Install Required Python Packages:**

   Open a terminal and navigate to your project directory. Run:

   ```sh
   pip3 install -r requirements.txt
   ```

3. **Install `exiftool`:**

   Install `exiftool` using your package manager. For example, on Ubuntu:

   ```sh
   sudo apt-get install libimage-exiftool-perl
   ```

## Usage

### Starting the Application

1. **Open a Terminal or Command Prompt.**
2. **Navigate to your project directory.**
3. **Run the application:**

   ```sh
   python main.py
   ```

   This will open the Photo Organizer GUI.

### Using the Interface

1. **Select Source and Destination Directories:**
   - Use the "Browse" buttons to select the source directory (where your photos are currently stored) and the destination directory (where the organized photos will be moved).

2. **Configure Folder Structure:**
   - Add or remove folder structure levels based on how you want to organize your photos.

3. **Select File Types:**
   - Choose which file types to include in the processing.

4. **Choose Renaming Strategy:**
   - Select how you want to rename your files.

5. **Start Processing:**
   - Click "Start" to begin processing. The progress will be displayed on the progress bar.

6. **Exit Application:**
   - Click "Exit" to close the application.

### Configuring the Application

- **Folder Structure Levels:**
  Define how the folders are structured based on photo metadata (e.g., year, month).

- **File Renaming Strategy:**
  Choose between options like adding date prefixes, suffixes, or replacing filenames with dates.

- **File Types:**
  Select which file types (e.g., `.jpg`, `.png`, `.mp4`) to include in the processing.

- **Delete Empty Source Folder:**
  Optionally delete the source folder if it is empty after processing.

## Debugging

### Common Issues and Solutions

1. **Missing Dependencies:**

   Ensure all required dependencies are installed. Run `pip install -r requirements.txt` to install missing packages.

2. **EXIF Data Not Extracted:**

   Make sure `exiftool` is correctly installed and available in your system PATH.

3. **File Not Moving:**

   Verify that the source and destination directories are correct and that you have the necessary permissions.

### Logging

- The application prints log messages to the console. These messages include errors and status updates. Check the console for information if something goes wrong.

- For more detailed debugging, you can add additional logging statements to the code or run the application in an IDE with debugging capabilities.

## Contributing

If you'd like to contribute to the development of this project:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and test them.
4. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to modify this template to better fit your project's needs and structure!