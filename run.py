import subprocess
import glob

# Get all config files in the configs/ directory
config_files = glob.glob("configs/*")

# Open out.txt for writing
for config in config_files:
    # Run main.py with the current config file
    process = subprocess.run(["python", "main.py", config], capture_output=False, text=True)