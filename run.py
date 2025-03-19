import subprocess
import glob

# Get all config files in the configs/ directory
config_files = glob.glob("configs/*")

# Open out.txt for writing
with open("out.txt", "w") as outfile:
    for config in config_files:
        # Run main.py with the current config file
        process = subprocess.run(["python", "main.py", config], capture_output=False, text=True)
        # Write the output to out.txt
        # outfile.write(f"Output for {config}:\n")
        # outfile.write(process.stdout + "\n")
        # outfile.write("-" * 40 + "\n")
