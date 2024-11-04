import sys
import qrcode
from dotenv import load_dotenv
import logging.config
from pathlib import Path
import os
import argparse
from datetime import datetime
import validators  # Import the validators package

# Load environment variables
load_dotenv()

# Environment Variables for Configuration
QR_DIRECTORY = os.getenv('QR_CODE_DIR')  # Directory for saving QR code
FILL_COLOR = os.getenv('FILL_COLOR')  # Fill color for the QR code
BACK_COLOR = os.getenv('BACK_COLOR')  # Background color for the QR code

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/app.log"),  # Log to a file named app.log
            logging.StreamHandler(sys.stdout),  # Optionally still log to console
        ]
    )

def create_directory(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        exit(1)

def is_valid_url(url):
    if validators.url(url):
        return True
    else:
        logging.error(f"Invalid URL provided: {url}")
        return False

def generate_qr_code(data, path, fill_color='red', back_color='white'):
    if not is_valid_url(data):
        return  # Exit the function if the URL is not valid

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        with path.open('wb') as qr_file:
            img.save(qr_file)
        logging.info(f"QR code successfully saved to {path}")

    except Exception as e:
        logging.error(f"An error occurred while generating or saving the QR code: {e}")

def main():
    
    # Initial logging setup
    setup_logging()

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Generate a QR code.')
    parser.add_argument('--url', help='The URL to encode in the QR code', default='https://github.com/Hk574')
    parser.add_argument('--back_color',help='Back Color', default= BACK_COLOR)
    parser.add_argument('--fill_color',help='FILL Color', default= FILL_COLOR)
    args = parser.parse_args()

    logging.info(f"URL : {args.url}")
    logging.info(f"BACK_COLOR : {args.back_color}")
    logging.info(f"FILL_COLOR : {args.fill_color}")

    
    # Generate a timestamped filename for the QR code
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QRCode_{timestamp}.png"

    # Create the full path for the QR code file
    qr_code_full_path = Path.cwd() / QR_DIRECTORY / qr_filename
    
    # Ensure the QR code directory exists
    create_directory(Path.cwd() / QR_DIRECTORY)
    
    logging.info("Generate and save the QR code Execution Started")
    
    generate_qr_code(args.url, qr_code_full_path, args.fill_color, args.back_color)

if __name__ == "__main__":
    main()