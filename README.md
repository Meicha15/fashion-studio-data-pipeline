# Fashion-studio-data-pipeline

Proyek ini adalah sebuah data pipeline otomatis berbasis **ETL (Extract, Transform, Load)** yang mengekstrak data produk dari platform *Fashion Studio*, melakukan pembersihan dan standardisasi data, lalu memuatnya ke berbagai target penyimpanan data sekaligus untuk kebutuhan analisis lebih lanjut.

## 🛠️ Alur Kerja ETL

1. **Extract:** Melakukan web scraping data produk (dari halaman 1 sampai 50) menggunakan `BeautifulSoup` dan `requests`.
2. **Transform:** Menggunakan `Pandas` untuk membersihkan data mentah, menyesuaikan tipe data, menangani nilai kosong, serta memformat kolom (seperti *Price, Rating, Size, Gender*, dan *Timestamp*).
3. **Load:** Menyimpan data yang telah bersih dan terstruktur ke tiga target penyimpanan:
   - **Database Relasional:** PostgreSQL (`psycopg2` & `SQLAlchemy`)
   - **Cloud Spreadsheet:** Google Sheets API
   - **Lokal File:** Berkas CSV (`products_data.csv`)
---
## Panduan Penggunaan & Pengujian Pipeline

# Menjalankan Skrip
python main.py

# URL google sheet
https://docs.google.com/spreadsheets/d/1a20oW2CHLPMPpFtIJGZk5Y-ERt63aCXymBOhZ6xBb6g/edit?gid=0#gid=0

# Menjalankan unit test pada folder test
coverage run -m pytest test

# Menjalankan test coverage pada folder tests (coverage report)
coverage report

### Hasil Laporan Cakupan Pengujian (Coverage Report)

```text
Name                     Stmts   Miss  Cover
--------------------------------------------
test\test_extract.py        45      1    98%
test\test_load.py           15      0   100%
test\test_transform.py      13      1    92%
utils\extract.py            58      8    86%
utils\load.py               28     14    50%
utils\transform.py          35      5    86%
--------------------------------------------
TOTAL                      194     29    85%

```
## 📁 Struktur Proyek

```text
├── test/
│   ├── test_extract.py       # Unit testing untuk modul ekstraksi
│   ├── test_load.py          # Unit testing untuk modul pemuatan data
│   └── test_transform.py     # Unit testing untuk modul transformasi
├── utils/
│   ├── extract.py            # Logika ekstraksi data / Web Scraping (Halaman 1-50)
│   ├── load.py               # Logika pemuatan data (PostgreSQL, Google Sheets, CSV)
│   └── transform.py          # Logika pembersihan dan penyesuaian format data
├── main.py                   # Skrip utama untuk menjalankan seluruh alur ETL
├── my-project-fashion-studio-73416d9e7b84.json  # Kredensial Google Sheets API
├── products_data.csv         # Output data hasil ETL dalam bentuk lokal CSV
└── requirements.txt          # Daftar dependensi pustaka Python proyek
