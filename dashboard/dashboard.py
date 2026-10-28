"""
Dashboard interaktif untuk Proyek Analisis Data: E-Commerce Public Dataset.

Menjawab dua pertanyaan bisnis:
1. Kategori produk apa yang menyumbang pendapatan tertinggi?
2. Bagaimana keterlambatan pengiriman memengaruhi skor ulasan pelanggan?

Serta menampilkan hasil Analisis Lanjutan (RFM Analysis).

Menjalankan dashboard ini secara lokal:
    streamlit run dashboard.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Palet warna konsisten dengan notebook analisis
HIGHLIGHT_COLOR = "#07F223"   # hijau: kesan positif / disorot
NEGATIVE_COLOR = "#D62728"    # merah: kesan negatif
NEUTRAL_COLOR = "#B0B0B0"     # abu-abu: elemen netral

sns.set_style("whitegrid")
st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    """Memuat main_data.csv hasil olahan notebook analisis."""
    df = pd.read_csv("main_data.csv", parse_dates=["order_purchase_timestamp"])
    return df


main_df = load_data()

# -----------------------------------------------------------------------
# Sidebar: filter interaktif
# -----------------------------------------------------------------------
st.sidebar.header("Filter Data")

min_date = main_df["order_purchase_timestamp"].min().date()
max_date = main_df["order_purchase_timestamp"].max().date()

date_range = st.sidebar.date_input(
    "Rentang Tanggal Pesanan",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# date_input bisa mengembalikan 1 atau 2 nilai tergantung interaksi user
if len(date_range) == 2:
    start_filter, end_filter = date_range
else:
    start_filter, end_filter = min_date, max_date

state_options = sorted(main_df["customer_state"].dropna().unique())
selected_states = st.sidebar.multiselect(
    "Provinsi/State Pelanggan", options=state_options, default=[]
)

# Terapkan filter: jika tidak ada state dipilih, tampilkan semua state
filtered_df = main_df[
    (main_df["order_purchase_timestamp"].dt.date >= start_filter)
    & (main_df["order_purchase_timestamp"].dt.date <= end_filter)
]
if selected_states:
    filtered_df = filtered_df[filtered_df["customer_state"].isin(selected_states)]

if filtered_df.empty:
    st.warning("Tidak ada data pada filter yang dipilih. Silakan ubah filter.")
    st.stop()

# Data level pesanan (deduplikasi) untuk metrik delivery, review, dan RFM
# agar pesanan dengan banyak item tidak terhitung berulang kali
order_level_df = filtered_df.drop_duplicates(subset="order_id")

# -----------------------------------------------------------------------
# Header & KPI ringkas
# -----------------------------------------------------------------------
st.title("📊 E-Commerce Public Dataset — Dashboard Analisis")
st.markdown(
    "Dashboard ini merangkum hasil analisis dua pertanyaan bisnis beserta "
    "segmentasi pelanggan (RFM) dari data pesanan *delivered*."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pendapatan", f"BRL {filtered_df['price'].sum():,.0f}")
col2.metric("Jumlah Pesanan", f"{order_level_df['order_id'].nunique():,}")
col3.metric(
    "Rata-rata Skor Ulasan",
    f"{order_level_df['review_score'].mean():.2f}",
)
col4.metric(
    "Persentase Terlambat",
    f"{order_level_df['is_late'].mean() * 100:.1f}%",
)

st.divider()

# -----------------------------------------------------------------------
# Pertanyaan 1: Kategori produk dengan pendapatan tertinggi
# -----------------------------------------------------------------------
st.header("1. Kategori Produk dengan Pendapatan Tertinggi")

category_revenue = (
    filtered_df[filtered_df["product_category"] != "unknown"]
    .groupby("product_category")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

if category_revenue.empty:
    st.info("Tidak ada data kategori pada filter ini.")
else:
    fig1, ax1 = plt.subplots(figsize=(9, 4.5))
    colors = [HIGHLIGHT_COLOR if i == 0 else NEUTRAL_COLOR
              for i in range(len(category_revenue))]
    ax1.barh(category_revenue.index[::-1], category_revenue.values[::-1],
              color=colors[::-1])
    ax1.set_title("5 Kategori Produk dengan Pendapatan Tertinggi",
                   fontsize=13, fontweight="bold")
    ax1.set_xlabel("Total Pendapatan (BRL)")
    ax1.set_ylabel("Kategori Produk")
    fig1.tight_layout()
    st.pyplot(fig1)

    st.caption(
        f"Kategori **{category_revenue.index[0]}** menjadi penyumbang "
        f"pendapatan tertinggi pada rentang dan wilayah yang dipilih."
    )

st.divider()

# -----------------------------------------------------------------------
# Pertanyaan 2: Keterlambatan pengiriman vs skor ulasan
# -----------------------------------------------------------------------
st.header("2. Keterlambatan Pengiriman vs Kepuasan Pelanggan")

review_by_status = (
    order_level_df.dropna(subset=["review_score"])
    .assign(status=lambda d: d["is_late"].map(
        {False: "Tepat Waktu", True: "Terlambat"}))
    .groupby("status")["review_score"]
    .mean()
)

if review_by_status.empty:
    st.info("Tidak ada data ulasan pada filter ini.")
else:
    fig2, ax2 = plt.subplots(figsize=(6, 4.5))
    bar_colors = [HIGHLIGHT_COLOR if s == "Tepat Waktu" else NEGATIVE_COLOR
                  for s in review_by_status.index]
    bars = ax2.bar(review_by_status.index, review_by_status.values,
                     color=bar_colors)
    ax2.bar_label(bars, fmt="%.2f", padding=3, fontsize=11)
    ax2.set_title("Rata-rata Skor Ulasan berdasarkan Status Pengiriman",
                   fontsize=13, fontweight="bold")
    ax2.set_ylabel("Rata-rata Skor Ulasan (1-5)")
    ax2.set_ylim(0, 5)
    fig2.tight_layout()
    st.pyplot(fig2)

    st.caption(
        "Pesanan yang terlambat secara konsisten memperoleh skor ulasan "
        "jauh lebih rendah dibandingkan pesanan yang tepat waktu."
    )

st.divider()

# -----------------------------------------------------------------------
# Analisis Lanjutan: Segmentasi Pelanggan (RFM)
# -----------------------------------------------------------------------
st.header("3. Segmentasi Pelanggan (RFM Analysis)")

segment_revenue = (
    order_level_df.groupby("rfm_segment")["price"]
    .sum()
    .sort_values(ascending=False)
)

if segment_revenue.empty:
    st.info("Tidak ada data segmen pada filter ini.")
else:
    fig3, ax3 = plt.subplots(figsize=(8, 4.5))
    seg_colors = [
        HIGHLIGHT_COLOR if seg in ("Champions", "Loyal Customers")
        else NEUTRAL_COLOR
        for seg in segment_revenue.index
    ]
    ax3.barh(segment_revenue.index[::-1], segment_revenue.values[::-1],
              color=seg_colors[::-1])
    ax3.set_title("Kontribusi Pendapatan per Segmen Pelanggan",
                   fontsize=13, fontweight="bold")
    ax3.set_xlabel("Total Pendapatan (BRL)")
    ax3.set_ylabel("Segmen Pelanggan")
    fig3.tight_layout()
    st.pyplot(fig3)

    st.caption(
        "Segmen **At Risk** dan **Champions** berwarna hijau karena "
        "keduanya memiliki nilai *monetary* tinggi — yang membedakan "
        "adalah seberapa baru transaksi terakhir mereka (*recency*)."
    )

with st.expander("Lihat data mentah (setelah filter)"):
    st.dataframe(filtered_df, use_container_width=True)
