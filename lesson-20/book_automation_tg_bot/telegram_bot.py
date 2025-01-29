import os
import requests
import pandas as pd
import fitz  # PyMuPDF
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
BOOKS_DIR = 'books'
COVERS_DIR = 'covers'
MAX_FILE_SIZE_MB = 50  # Telegram's document size limit

# Create necessary directories
os.makedirs(BOOKS_DIR, exist_ok=True)
os.makedirs(COVERS_DIR, exist_ok=True)

report = []

for filename in os.listdir(BOOKS_DIR):
    if not filename.lower().endswith('.pdf'):
        continue  # Skip non-PDF files

    book_path = os.path.join(BOOKS_DIR, filename)
    book_name = filename
    book_id = os.path.splitext(filename)[0]
    send_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check file size
    file_size_mb = os.path.getsize(book_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        report.append({
            'book_id': book_id,
            'book_name': book_name,
            'successfully_sent': False,
            'send_date': send_date
        })
        print(f"Skipped {book_name} due to size exceeding 50MB.")
        continue

    # Generate cover image
    cover_path = os.path.join(COVERS_DIR, f'{book_id}.jpg')
    try:
        doc = fitz.open(book_path)
        if len(doc) == 0:
            raise ValueError("PDF has no pages.")
        page = doc.load_page(0)
        pix = page.get_pixmap()
        pix.save(cover_path)
        doc.close()
    except Exception as e:
        print(f"Error generating cover for {book_name}: {e}")
        report.append({
            'book_id': book_id,
            'book_name': book_name,
            'successfully_sent': False,
            'send_date': send_date
        })
        continue

    # Send cover image to Telegram
    photo_success = False
    try:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
        data = {'chat_id': CHANNEL_ID}
        with open(cover_path, 'rb') as photo_file:
            files = {'photo': (f'{book_id}_cover.jpg', photo_file)}
            response = requests.post(url, data=data, files=files, verify=False)  # verify=False temp fix
        if response.status_code == 200:
            response_json = response.json()
            photo_success = response_json.get('ok', False)
            if not photo_success:
                print(f"Failed to send cover for {book_name}: {response_json.get('description')}")
        else:
            print(f"Failed to send cover for {book_name}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error sending cover for {book_name}: {e}")

    # Send PDF to Telegram
    doc_success = False
    try:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'
        data = {'chat_id': CHANNEL_ID}
        with open(book_path, 'rb') as doc_file:
            files = {'document': (book_name, doc_file)}
            response = requests.post(url, data=data, files=files, verify=False)
        if response.status_code == 200:
            response_json = response.json()
            doc_success = response_json.get('ok', False)
            if not doc_success:
                print(f"Failed to send PDF for {book_name}: {response_json.get('description')}")
        else:
            print(f"Failed to send PDF for {book_name}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error sending PDF for {book_name}: {e}")

    # Determine overall success
    successfully_sent = photo_success and doc_success
    report.append({
        'book_id': book_id,
        'book_name': book_name,
        'successfully_sent': successfully_sent,
        'send_date': send_date
    })
    print(f"Processed {book_name}: {'Success' if successfully_sent else 'Failed'}")

# Generate report
df = pd.DataFrame(report)
df.to_csv('telegram_books_report.csv', index=False)
print("Report generated: telegram_books_report.csv")
print(df)