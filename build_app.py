import PyInstaller.__main__
import os
import sys

# Get the directory containing this script
root_dir = os.path.dirname(os.path.abspath(__file__))

# Define icon path
icon_file = os.path.join(root_dir, 'resources', 'icon.png')

PyInstaller.__main__.run([
    'run.py',  # Your main script
    '--name=DataLens',  # Name of the application
    '--onefile',  # Create a single file
    '--windowed',  # GUI mode
    '--add-data=src:src',  # Include source files
    f'--icon={icon_file}',  # Application icon
    '--noconfirm',  # Replace existing build
    '--clean',  # Clean cache
    '--hidden-import=gpt4all',  # Include AI module
    '--hidden-import=PyQt6',
    '--collect-data=gpt4all',  # Include AI model data
])
