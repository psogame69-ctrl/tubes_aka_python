import streamlit as st
import time
import sys
import matplotlib.pyplot as plt
import pandas as pd

sys.setrecursionlimit(10000)

def maxKataIteratif(teks):
    listKata = teks.split()
    maxKata = ""
    for kata in listKata:
        if len(kata) > len(maxKata):
            maxKata = kata
    return maxKata

def maxKataRekursif(listKata, index=0, maxKata=""):
    if index == len(listKata):
        return maxKata

    kata = listKata[index]
    if len(kata) > len(maxKata):
        maxKata = kata

    return maxKataRekursif(listKata, index + 1, maxKata)

def main():
    st.set_page_config(page_title="Analisis Algoritma: Iteratif vs Rekursif", layout="wide")
    
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    st.title("Analisis Efisiensi: Iteratif vs Rekursif")
    st.markdown("""
    Aplikasi ini membandingkan kecepatan eksekusi antara algoritma Iteratif dan Rekursif dalam mencari kata terpanjang pada suatu teks.
    Data dari setiap eksekusi akan disimpan untuk menampilkan grafik trend di bagian bawah.
    """)

    st.subheader("Input Data")
    default_text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
    user_text = st.text_area("Masukkan teks yang ingin dianalisis:", default_text, height=150)

    num_runs = 1

    col_action1, col_action2 = st.columns([1, 5])
    
    with col_action1:
        start_btn = st.button("Mulai Analisis")
    
    with col_action2:
        if st.button("Hapus Riwayat"):
            st.session_state['history'] = []
            st.rerun()

    if start_btn:
        listKata = user_text.split()

        if not listKata:
            st.warning("Silakan masukkan teks terlebih dahulu.")
            return

        start_time = time.perf_counter()
        for _ in range(num_runs):
            res_iter = maxKataIteratif(user_text)
        end_time = time.perf_counter()
        time_iter = (end_time - start_time) / num_runs * 1000

        try:
            start_time = time.perf_counter()
            for _ in range(num_runs):
                res_recur = maxKataRekursif(listKata)
            end_time = time.perf_counter()
            time_recur = (end_time - start_time) / num_runs * 1000
            error_msg = None
        except RecursionError:
            time_recur = None
            error_msg = "Teks terlalu panjang untuk metode Rekursif (Batas rekursi tercapai)."

        st.session_state['history'].append({
            "Jumlah Kata": len(listKata),
            "Iteratif": time_iter,
            "Rekursif": time_recur
        })

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.info(f"Kata Terpanjang: {res_iter}")
        with col_res2:
            st.info(f"Jumlah Kata: {len(listKata)}")

        st.divider()
        st.subheader("Hasil Eksekusi Saat Ini")

        if error_msg:
            st.error(error_msg)

        display_time_recur = time_recur if time_recur is not None else 0
        
        data = {
            "Metode": ["Iteratif", "Rekursif"],
            "Waktu (ms)": [time_iter, display_time_recur]
        }
        df = pd.DataFrame(data)

        c1, c2 = st.columns([1, 2])
        with c1:
            st.write(df)
            if display_time_recur > 0:
                ratio = display_time_recur / time_iter if time_iter > 0 else 0
                st.metric("Rasio Kelambatan", f"{ratio:.2f}x", delta="Rekursif lebih lambat", delta_color="inverse")
            elif time_recur is None:
                st.metric("Rasio Kelambatan", "N/A", delta="Rekursi Gagal")

        with c2:
            fig, ax = plt.subplots(figsize=(8, 4))
            colors = ['#4CAF50', '#F44336']
            ax.bar(df["Metode"], df["Waktu (ms)"], color=colors)
            ax.set_ylabel("Waktu (ms)")
            ax.set_title("Iteratif vs Rekursif (Run Ini)")
            st.pyplot(fig)

    if len(st.session_state['history']) > 0:
        st.divider()
        st.subheader("Riwayat Performa (Analisis Trend)")

        history_df = pd.DataFrame(st.session_state['history'])

        history_df_sorted = history_df.sort_values(by="Jumlah Kata")

        h_col1, h_col2 = st.columns([3, 1])

        with h_col1:
            fig2, ax2 = plt.subplots(figsize=(10, 5))

            ax2.plot(history_df_sorted["Jumlah Kata"], history_df_sorted["Iteratif"], 
                     marker='o', linestyle='-', color='#87CEEB', label='Iteratif')

            ax2.plot(history_df_sorted["Jumlah Kata"], history_df_sorted["Rekursif"], 
                     marker='o', linestyle='-', color='#F44336', label='Rekursif')

            ax2.set_xlabel("Jumlah Kata (Input Size)")
            ax2.set_ylabel("Waktu Eksekusi (ms)")
            ax2.set_title("Pertumbuhan Waktu Eksekusi vs Ukuran Input")
            ax2.legend()
            ax2.grid(True, linestyle='--', alpha=0.7)

            st.pyplot(fig2)

        with h_col2:
            st.write("Data Riwayat:")
            st.dataframe(history_df_sorted[["Jumlah Kata", "Iteratif", "Rekursif"]], height=300)

if __name__ == "__main__":
    main()