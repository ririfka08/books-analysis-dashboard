import streamlit as st
import pandas as pd
import plotly.express as px


# PAGE CONFIG (harus di baris paling atas setelah import)

st.set_page_config(
    page_title="Book Publishing Insights",
    page_icon="📚",
    layout="wide"
)


# LOAD DATA

@st.cache_data  # biar data nggak di-reload tiap ganti filter (bikin app lebih responsif)
def load_data():
    df = pd.read_csv("books_cleaned.csv")
    # genre_list & award_list ke-save sebagai string representasi list di CSV,
    # perlu di-parse ulang jadi list Python asli
    import ast
    df["genre_list"] = df["genre_list"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    return df

df = load_data()
df_exploded = df.explode("genre_list")


# HEADER

st.title("📚 Book Publishing Insights Dashboard")
st.markdown("Analisis genre, panjang buku, dan tren rating untuk strategi republishing & promosi")


# SIDEBAR FILTERS

st.sidebar.header("Filter")

min_books = st.sidebar.slider(
    "Minimal jumlah buku per genre (biar genre niche tidak bias)",
    min_value=10, max_value=200, value=50, step=10
)

year_range = st.sidebar.slider(
    "Rentang tahun terbit",
    min_value=1900, max_value=2024,
    value=(1990, 2024)
)


# KEY METRICS (Row Atas)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Buku", f"{len(df):,}")
col2.metric("Rating Rata-rata", f"{df['rating'].mean():.2f}")
col3.metric("Jumlah Genre Unik", df_exploded["genre_list"].nunique())
col4.metric("% Buku Menang Award", f"{df['has_award'].mean()*100:.1f}%")

st.divider()


# CHART 1 - Genre Popularity vs Rating

st.subheader("1. Genre Populer vs Rating — mana yang worth dipromosikan?")

genre_stats = df_exploded.groupby("genre_list").agg(
    avg_rating=("rating", "mean"),
    total_books=("title", "count")
).reset_index()
genre_stats = genre_stats[genre_stats["total_books"] >= min_books]
genre_stats = genre_stats.sort_values("avg_rating", ascending=False)

fig1 = px.scatter(
    genre_stats, x="total_books", y="avg_rating",
    text="genre_list", size="total_books",
    labels={"total_books": "Jumlah Buku", "avg_rating": "Rating Rata-rata"},
    color="avg_rating", color_continuous_scale="Blues"
)
fig1.update_traces(textposition="top center")
st.plotly_chart(fig1, width='stretch')

st.info("💡 **Insight**: Genre di kuadran kanan-atas (jumlah buku banyak + rating tinggi) adalah kandidat paling aman untuk promosi karena sudah terbukti demand-nya tinggi dan kualitasnya konsisten.")

st.divider()


# CHART 2 - Pages vs Rating

st.subheader("2. Panjang Buku vs Rating")

df_filtered = df[(df["publish_year"] >= year_range[0]) & (df["publish_year"] <= year_range[1])]
df_filtered["page_category"] = pd.cut(
    df_filtered["pages_clean"],
    bins=[0, 200, 400, 600, 10000],
    labels=["Short (<200)", "Medium (200-400)", "Long (400-600)", "Very Long (600+)"]
)

fig2 = px.box(df_filtered, x="page_category", y="rating",
              color="page_category",
              labels={"page_category": "Kategori Panjang", "rating": "Rating"})
st.plotly_chart(fig2, width='stretch')

st.divider()


# CHART 3 - Trend Over Time

st.subheader("3. Tren Rating per Tahun Terbit")

yearly_trend = df_filtered.groupby("publish_year")["rating"].mean().reset_index()
fig3 = px.line(yearly_trend, x="publish_year", y="rating",
               labels={"publish_year": "Tahun Terbit", "rating": "Rating Rata-rata"})
st.plotly_chart(fig3, width='stretch')

st.divider()


# CHART 4 - Award Comparison
st.subheader("4. Buku Award vs Non-Award")

award_comparison = df.groupby("has_award").agg(
    avg_rating=("rating", "mean"),
    avg_pages=("pages_clean", "mean"),
    total_books=("title", "count")
).reset_index()
award_comparison["has_award"] = award_comparison["has_award"].map({True: "Menang Award", False: "Tidak Menang Award"})

fig4 = px.bar(award_comparison, x="has_award", y="avg_rating",
              color="has_award",
              labels={"has_award": "", "avg_rating": "Rating Rata-rata"})
st.plotly_chart(fig4, width='stretch')

st.divider()


# TABLE - Underserved Language Markets
st.subheader("5. Peluang Pasar Bahasa yang Underserved")

language_stats = df.groupby("language").agg(
    avg_rating=("rating", "mean"),
    total_books=("title", "count")
).reset_index()
language_stats = language_stats[language_stats["total_books"] >= 20]
language_stats = language_stats.sort_values(["avg_rating", "total_books"], ascending=[False, True])

st.dataframe(language_stats.head(15), width='stretch')
st.info("💡 **Insight**: Bahasa dengan rating tinggi tapi jumlah buku sedikit menunjukkan demand yang belum terpenuhi — peluang ekspansi katalog ke bahasa tersebut.")