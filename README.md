# E-Commerce Public Dataset — Dashboard Analisis Data

Dashboard interaktif hasil Proyek Analisis Data menggunakan **E-Commerce
Public Dataset**. Dashboard ini menjawab dua pertanyaan bisnis utama serta
menampilkan hasil Analisis Lanjutan (RFM Analysis).

## Struktur Proyek

```
submission/
├── dashboard/
│   ├── main_data.csv      # Data hasil wrangling, siap pakai untuk dashboard
│   └── dashboard.py       # Kode aplikasi Streamlit
├── data/                  # Dataset mentah (raw) yang digunakan di notebook
├── notebook.ipynb         # Proses analisis data lengkap
├── README.md
├── requirements.txt
└── url.txt                # Tautan dashboard yang sudah di-deploy
```

## Cara Menjalankan Dashboard di Local

1. **Clone atau ekstrak folder submission ini**, lalu masuk ke folder
   `dashboard/`:

   ```bash
   cd submission/dashboard
   ```

2. **(Opsional tapi disarankan) Buat virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate

   macOS / Linux (bash/zsh)	    source venv/bin/activate
   Windows PowerShell	            venv\Scripts\Activate.ps1
   Windows Command Prompt (cmd)	venv\Scripts\activate.bat
   ```

3. **Install seluruh dependency** yang tercantum di `requirements.txt`:

   ```bash
   pip install -r ../requirements.txt
   ```

4. **Jalankan dashboard:**

   ```bash
   streamlit run dashboard.py
   ```

5. Dashboard akan otomatis terbuka di browser pada alamat
   `http://localhost:8501`. Jika tidak terbuka otomatis, salin alamat
   tersebut secara manual ke browser.

## Fitur Dashboard

- **Filter interaktif** di sidebar: rentang tanggal pesanan dan provinsi
  (state) pelanggan.
- **KPI ringkas**: total pendapatan, jumlah pesanan, rata-rata skor ulasan,
  dan persentase pesanan terlambat — semuanya menyesuaikan filter yang
  dipilih.
- **Pertanyaan 1**: visualisasi lima kategori produk dengan pendapatan
  tertinggi.
- **Pertanyaan 2**: perbandingan rata-rata skor ulasan antara pesanan tepat
  waktu dan terlambat.
- **Analisis Lanjutan (RFM)**: kontribusi pendapatan per segmen pelanggan.

## Sumber Data

Dataset bersumber dari **E-Commerce Public Dataset (Olist)**. Data pada
`dashboard/main_data.csv` merupakan hasil proses *data wrangling* (lihat
`notebook.ipynb`) dari data mentah pada folder `data/`.

## Tautan Dashboard (Live Demo)

Lihat berkas [`url.txt`](./url.txt) untuk tautan dashboard yang telah
di-deploy ke Streamlit Community Cloud.
