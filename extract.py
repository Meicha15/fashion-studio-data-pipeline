import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# Menambahkan header User-Agent untuk permintaan HTTP
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# Fungsi untuk mengambil konten dari URL
def fetching_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Akan memunculkan exception jika status kode tidak 200
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Fungsi untuk mengekstrak data produk dari card
def extract_product_data(card):
    try:
        title = card.find("h3", class_="product-title")
        price = card.find("span", class_="price")
        details = card.find_all("p")

        # Menghapus kata "Rating:", "Size:", "Gender:" dari masing-masing kolom
        rating = details[0].text.strip() if len(details) > 0 else "Invalid Rating / 5"
        if "Rating:" in rating:
            rating = rating.replace("Rating:", "").strip()

        # Mengambil angka dari string "3 Colors"
        colors = details[1].text.strip() if len(details) > 1 else "-"
        if "Colors" in colors:
            colors = ''.join(filter(str.isdigit, colors))  # Ambil hanya angka dari "3 Colors"
        
        size = details[2].text.strip() if len(details) > 2 else "-"
        gender = details[3].text.strip() if len(details) > 3 else "-"

        # Menghilangkan kata "Size:" dan "Gender:" dari kolom Size dan Gender
        if "Size:" in size:
            size = size.replace("Size:", "").strip()
        if "Gender:" in gender:
            gender = gender.replace("Gender:", "").strip()

        # Mendapatkan timestamp untuk setiap produk yang diekstrak
        timestamp = datetime.now().isoformat(sep=' ', timespec='microseconds')

        return {
            "Title": title.text.strip() if title else "Unknown",
            "Price": price.text.strip() if price else "Price Unavailable",
            "Rating": rating,
            "Colors": colors,  # Pastikan warna hanya berisi angka
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp  # Menambahkan timestamp pada setiap produk
        }
    except Exception as e:
        print(f"Error extracting data from card: {e}")
        return None

# Fungsi untuk mengekstrak produk dari beberapa halaman
def scrape_product(page1, pages_url, start_page=1, end_page=50, delay=1):
    data = []

    for page in range(start_page, end_page + 1):  # Iterasi untuk halaman mulai dari start_page sampai end_page
        try:
            if page == 1:
                url = page1  # Jika halaman pertama, gunakan URL khusus
            else:
                url = pages_url.format(page)  # Gunakan pola URL untuk halaman-halaman selanjutnya

            print(f"Scraping: {url}")
            content = fetching_content(url)  # Mengambil konten halaman
            if not content:
                continue  # Jika tidak ada konten, lanjutkan ke halaman berikutnya

            soup = BeautifulSoup(content, "html.parser")  # Parse konten HTML
            cards = soup.find_all("div", class_="collection-card")  # Temukan semua kartu produk

            # Ekstraksi data untuk setiap produk di dalam kartu
            for card in cards:
                product = extract_product_data(card)
                if product:
                    data.append(product)

            # Memberikan delay antar permintaan untuk menghindari pemblokiran
            time.sleep(delay)
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            continue  # Tetap lanjutkan ke halaman berikutnya meskipun terjadi error pada halaman ini

    return pd.DataFrame(data)  # Mengembalikan hasil ekstraksi dalam bentuk DataFrame
