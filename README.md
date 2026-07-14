# 📚 Book Publishing Strategy Analysis

Analisis data 52.000+ buku dari Goodreads untuk membantu penerbit/toko buku menentukan strategi genre, promosi, dan ekspansi katalog berdasarkan data historis rating dan popularitas.

🔗 **Live Dashboard**: [https://books-analysis-dashboard-rifka.streamlit.app/](#) <!-- ganti dengan link Streamlit kamu -->

---

## Business Problem

Penerbit dan platform buku sering kesulitan menentukan genre atau format buku apa yang worth diinvestasikan untuk promosi maupun akuisisi katalog baru. Analisis ini menjawab 5 pertanyaan bisnis kunci:

1. Genre apa yang punya demand tinggi **dan** kualitas terjaga (rating tinggi)?
2. Apakah panjang buku (jumlah halaman) mempengaruhi rating?
3. Bahasa mana yang "underserved" — rating tinggi tapi jumlah bukunya masih sedikit (peluang ekspansi)?
4. Apakah buku pemenang award punya pola berbeda dari buku biasa?
5. Bagaimana tren rating buku dari waktu ke waktu — apakah buku lama lebih "timeless"?

## Data Source

[Goodreads Best Books Ever](https://www.kaggle.com/datasets/thedevastator/comprehensive-overview-of-52478-goodreads-best-b) — 52.478 buku dengan informasi rating, genre, jumlah halaman, penulis, tahun terbit, dan status award.

## Tech Stack

- **Python**: Pandas (cleaning & analysis), Plotly (visualisasi)
- **Dashboard**: Streamlit, di-deploy ke Streamlit Community Cloud
- **Version control**: Git + GitHub


*Project ini dibuat sebagai bagian dari portfolio data analyst, dengan fokus pada analisis berbasis pertanyaan bisnis dan dashboard interaktif yang dapat diakses publik.*
