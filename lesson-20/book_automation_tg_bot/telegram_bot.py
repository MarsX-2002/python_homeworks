import os
import requests
import pandas as pd
import fitz
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Optional
import urllib3
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Disable SSL warnings
urllib3.disable_warnings()

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
BOOKS_DIR = 'books'
COVERS_DIR = 'covers'
MAX_FILE_SIZE_MB = 50
TIMEOUT = 120
MAX_RETRIES = 5
BACKOFF_FACTOR = 1.5

# Create directories
os.makedirs(BOOKS_DIR, exist_ok=True)
os.makedirs(COVERS_DIR, exist_ok=True)

class TelegramSender:
    def __init__(self, token: str, channel_id: str):
        self.token = token
        self.channel_id = channel_id
        self.base_url = f'https://api.telegram.org/bot{token}'
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=[408, 429, 500, 502, 503, 504],
        )
        
        # Create session with retry strategy
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def send_file(self, file_path: str, file_type: str) -> Optional[Dict]:
        """Send a file to Telegram channel with retry mechanism"""
        for attempt in range(MAX_RETRIES):
            try:
                endpoint = '/sendDocument' if file_type == 'document' else '/sendPhoto'
                url = f'{self.base_url}{endpoint}'
                
                with open(file_path, 'rb') as file:
                    files = {file_type: (os.path.basename(file_path), file)}
                    response = self.session.post(
                        url,
                        files=files,
                        data={'chat_id': self.channel_id},
                        verify=False,
                        timeout=TIMEOUT
                    )
                
                if response.status_code == 200:
                    return response.json()
                
                # If we get a rate limit error, wait before retrying
                if response.status_code == 429:
                    if attempt < MAX_RETRIES - 1:
                        retry_after = int(response.headers.get('Retry-After', 30))
                        time.sleep(retry_after)
                        continue
                        
            except requests.exceptions.Timeout:
                if attempt < MAX_RETRIES - 1:
                    wait_time = BACKOFF_FACTOR * (2 ** attempt)
                    print(f"Timeout occurred. Retrying in {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                    continue
            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    wait_time = BACKOFF_FACTOR * (2 ** attempt)
                    print(f"Error: {str(e)}. Retrying in {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                    continue
                print(f"Error sending {file_type} after {MAX_RETRIES} attempts: {str(e)}")
                return None
        
        return None

def extract_cover(pdf_path: str, cover_path: str) -> bool:
    """Extract cover page from PDF"""
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        pix.save(cover_path)
        doc.close()
        return True
    except Exception as e:
        print(f"Cover extraction failed: {str(e)}")
        return False

def process_books():
    sender = TelegramSender(BOT_TOKEN, CHANNEL_ID)
    report = []

    for filename in os.listdir(BOOKS_DIR):
        if not filename.lower().endswith('.pdf'):
            continue

        book_path = os.path.join(BOOKS_DIR, filename)
        file_size_mb = os.path.getsize(book_path) / (1024 * 1024)
        
        record = {
            'book_name': filename,
            'send_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_size_mb': round(file_size_mb, 2),
            'cover_sent': False,
            'doc_sent': False,
            'error': None
        }

        # Skip large files
        if file_size_mb > MAX_FILE_SIZE_MB:
            record['error'] = f"File too large ({record['file_size_mb']}MB)"
            report.append(record)
            continue

        # Extract and send cover
        cover_path = os.path.join(COVERS_DIR, f'{os.path.splitext(filename)[0]}.jpg')
        if extract_cover(book_path, cover_path):
            cover_result = sender.send_file(cover_path, 'photo')
            record['cover_sent'] = bool(cover_result)

        # Send PDF document
        doc_result = sender.send_file(book_path, 'document')
        record['doc_sent'] = bool(doc_result)
        
        report.append(record)
        print(f"Processed: {filename} | Cover: {record['cover_sent']} | Doc: {record['doc_sent']}")

    return report

def main():
    # Process books and generate report
    report = process_books()
    
    # Save report to CSV
    df = pd.DataFrame(report)
    csv_path = 'telegram_books_report.csv'
    df.to_csv(csv_path, index=False)
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"Total books processed: {len(df)}")
    print(f"Successfully sent: {df['doc_sent'].sum()}")
    print(f"Success rate: {df['doc_sent'].mean():.1%}")
    
    # Show failed documents
    failed = df[~df['doc_sent']]
    if not failed.empty:
        print("\nFailed documents:")
        for _, row in failed.iterrows():
            print(f"- {row['book_name']}: {row.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()