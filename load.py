import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine, text

def store_to_google_sheets(data, spreadsheet_id, range_name):
    """Fungsi untuk menyimpan data ke Google Sheets menggunakan Google Sheets API"""
    try:
        # Tentukan kredensial dan akses scope
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = './my-project-fashion-studio-73416d9e7b84.json'  # Path ke file service account Anda
        
        # Autentikasi menggunakan file service account
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        # Membangun service Sheets API
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        # Hapus data yang ada di range sebelum menambahkan data baru
        sheet.values().clear(spreadsheetId=spreadsheet_id, range=range_name).execute()
        
        # Menyiapkan data dalam format list of lists, dengan header
        values = [data.columns.tolist()] + data.values.tolist()  # Menambahkan header ke data

        # Menentukan body request untuk update data
        body = {
            'values': values
        }

        # Memperbarui nilai pada spreadsheet
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',  # Menyimpan nilai secara langsung
            body=body
        ).execute()

        print("Data berhasil disimpan ke Google Sheets!")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke Google Sheets: {e}")

def store_to_postgre(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL tanpa menghapus tabel yang sudah ada"""
    try:
        # Membuat engine database
        engine = create_engine(db_url)
        
        with engine.connect() as con:
            # Menyimpan data ke tabel 'productstoscrape' jika tabel sudah ada, data akan ditambahkan (append)
            data.to_sql('productstoscrape', con=con, if_exists='append', index=False)
            print("Data berhasil disimpan ke PostgreSQL!")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")
        # Lemparkan exception setelah mencetak error
        raise Exception(f"Error in saving to PostgreSQL: {e}")

def store_to_csv(data, file_path):
    """Fungsi untuk menyimpan data ke file CSV"""
    try:
        data.to_csv(file_path, index=False)
        print(f"Data berhasil disimpan ke file CSV di {file_path}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke CSV: {e}")




