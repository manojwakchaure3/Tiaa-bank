import subprocess
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# --- Logger Configuration ---
def setup_logger():
    # Define log directory
    log_dir = os.path.join("C://Users//Wakch//OneDrive//Desktop//stoic salamander//Tiaa bank//loanrate//loanrate//spiders//data//log//run_scrapy.log")
    os.makedirs(log_dir, exist_ok=True)  # Ensure directory exists

    # Define full path to the single log file
    log_file_path = os.path.join(log_dir, "run_scrapy.log")

    logger = logging.getLogger("pipeline_logger")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8', mode='a')
        console_handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Initialize logger
logger = setup_logger()

# --- Set working directory to project root ---
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

logger.info("Running Scrapy spider...")

# --- Run Scrapy spider ---
try:
    result = subprocess.run(
        [sys.executable, "-m", "scrapy", "crawl", "bankrate_spider", "-s", "LOG_LEVEL=WARNING"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.stdout.strip():
        logger.info("Scrapy Output:\n" + result.stdout.strip())

    if result.stderr.strip():
        logger.warning("Scrapy Errors/Warnings:\n" + result.stderr.strip())

    if result.returncode != 0:
        logger.error(f"Scrapy spider failed with return code {result.returncode}")
        sys.exit(result.returncode)

    logger.info("Scraping complete.")

except Exception as e:
    logger.error(f"Scrapy execution error: {e}")
    sys.exit(1)

# --- Optional: Append JSON to CSV ---
script_path =  os.path.join("C://Users//Wakch//OneDrive//Desktop//stoic salamander//Tiaa bank//loanrate//loanrate//spiders//append_json_to_csv.py")

logger.info("Appending JSON to CSV...")

try:
    subprocess.run([sys.executable, str(script_path)], check=True)
    
    logger.info("Append complete.")
except subprocess.CalledProcessError as e:
    logger.error(f"Append failed: {e}")
    sys.exit(1)
