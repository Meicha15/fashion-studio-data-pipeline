import pandas as pd

def transform_data(df):
    print(f"Jumlah data sebelum transformasi: {len(df)}")

    # 1. Mengonversi kolom 'Price' menjadi angka dan mengonversinya ke Rupiah (Rp16.000)
    def convert_price(x):
        try:
            # Menghapus simbol '$' dan koma, kemudian mengonversi menjadi angka
            price = x.replace('$', '').replace(',', '').strip()
            # Mengonversi ke Rupiah dengan nilai tukar Rp16.000
            return float(price) * 16000 if price.replace('.', '', 1).isdigit() else None
        except ValueError:
            return None

    # Menerapkan konversi harga ke kolom 'Price'
    df['Price'] = df['Price'].apply(lambda x: convert_price(x) if isinstance(x, str) else None)

    # 2. Menghapus data duplikat
    df = df.drop_duplicates()

    # 3. Menghapus baris yang memiliki nilai null (termasuk 'Price')
    df = df.dropna(subset=['Price'])

    # 4. Menghapus data yang tidak valid, misalnya "Unknown Product" di kolom 'Price'
    df = df[~df['Price'].isin(['Unknown Product', 'Price Unavailable'])]

    # 5. Mengonversi kolom 'Rating' menjadi tipe data float dengan pengecekan untuk rating invalid
    def clean_rating(rating):
        if isinstance(rating, str):
            # Menghapus simbol '⭐' dan memisahkan angka dari teks
            if '⭐' in rating:
                rating = rating.replace('⭐', '').split(' ')[1] if '⭐' in rating else rating.split(' ')[0]
                if rating.replace('.', '', 1).isdigit():
                    return float(rating)
            # Menangani kasus 'Invalid Rating' atau Rating yang kosong
            if 'Invalid Rating' in rating or rating.strip() == "":
                return None
        return None

    # Menerapkan konversi rating ke kolom 'Rating'
    df['Rating'] = df['Rating'].apply(clean_rating)

    # 6. Mengonversi kolom 'Colors' menjadi angka (mengambil angka saja)
    df['Colors'] = df['Colors'].apply(lambda x: ''.join(filter(str.isdigit, x)) if isinstance(x, str) else '0')
    df['Colors'] = df['Colors'].astype(int)  # Pastikan menjadi tipe int

    # 7. Memastikan 'Size' dan 'Gender' bertipe string
    df['Size'] = df['Size'].astype(str)
    df['Gender'] = df['Gender'].astype(str)

    # 8. Menampilkan tipe data kolom setelah transformasi untuk memastikan sudah sesuai
    print("\nTipe data kolom setelah transformasi:")
    print(df.dtypes)

    # 9. Menampilkan baris yang memiliki nilai Rating null untuk mengecek masalah lebih lanjut
    print("\nMenampilkan baris dengan rating null:")
    print(df[df['Rating'].isnull()])  # Menampilkan baris yang memiliki rating null

    # 10. Memeriksa data null dan nilai rating yang invalid setelah transformasi
    print("\nJumlah data dengan rating null setelah transformasi:")
    print(df[df['Rating'].isnull()].shape[0])

    # 11. Menghapus rating yang null
    df = df.dropna(subset=['Rating'])

    return df
