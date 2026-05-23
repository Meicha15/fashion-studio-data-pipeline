from utils.extract import scrape_product  # Mengimpor fungsi scrape_product dari extract.py
from utils.transform import transform_data  # Mengimpor fungsi transform_data dari transform.py
from utils.load import store_to_postgre, store_to_google_sheets, store_to_csv  # Mengimpor fungsi dari load.py

def main():
    # URL dasar untuk halaman yang akan diekstrak
    BASE_URL = "https://fashion-studio.dicoding.dev/"
    PAGE_URL_PATTERN = "https://fashion-studio.dicoding.dev/page{}"
    
    try:
        # Memanggil fungsi scrape_product untuk mengekstrak data dari halaman 1 hingga 50
        print("Memulai proses ekstraksi data...")
        raw_df = scrape_product(BASE_URL, PAGE_URL_PATTERN, start_page=1, end_page=50)

        # Menampilkan data sebelum transformasi untuk referensi
        print("\nData sebelum transformasi:")
        print(raw_df.head())  # Menampilkan 5 baris pertama sebelum transformasi

        # Memanggil fungsi transformasi untuk membersihkan dan mengubah data
        print("\nMemulai proses transformasi data...")
        transformed_df = transform_data(raw_df)

        # Menampilkan data yang sudah ditransformasi
        print("\nData setelah transformasi:")
        print(transformed_df.head())  # Menampilkan 5 baris pertama setelah transformasi
        
        # Menampilkan informasi tipe data kolom setelah transformasi untuk memastikan sudah sesuai
        print("\nInformasi Data Setelah Transformasi:")
        transformed_df.info()  # Menampilkan informasi tentang jumlah data dan tipe data kolom

        # Menyimpan data yang sudah ditransformasi ke PostgreSQL
        print("\nMenyimpan data ke PostgreSQL...")
        db_url = 'postgresql+psycopg2://developer:meicha15@localhost:5432/productsdb'
        store_to_postgre(transformed_df, db_url)  # Memanggil fungsi untuk menyimpan ke PostgreSQL

        # Menyimpan data yang sudah ditransformasi ke Google Sheets
        print("\nMenyimpan data ke Google Sheets...")
        SPREADSHEET_ID = '1a20oW2CHLPMPpFtIJGZk5Y-ERt63aCXymBOhZ6xBb6g'
        RANGE_NAME = 'Sheet1!A1:G'  # Tentukan range untuk data yang akan diinputkan
        store_to_google_sheets(transformed_df, SPREADSHEET_ID, RANGE_NAME)  # Memanggil fungsi untuk menyimpan ke Google Sheets

        # Menyimpan data yang sudah ditransformasi ke CSV (tambahkan jika diperlukan)
        print("\nMenyimpan data ke file CSV...")
        file_path = "products_data.csv"  # Tentukan path file CSV
        store_to_csv(transformed_df, file_path)  # Memanggil fungsi untuk menyimpan ke CSV

    except Exception as e:
        print(f"Terjadi kesalahan dalam proses ETL: {e}")
        
if __name__ == "__main__":
    main()