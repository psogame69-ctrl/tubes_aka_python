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
    
    st.title("Analisis Efisiensi: Iteratif vs Rekursif")
    st.markdown("""
    Aplikasi ini membandingkan kecepatan eksekusi antara algoritma Iteratif dan Rekursif dalam mencari kata terpanjang pada suatu teks.
    """)

    st.subheader("Input Data")
    default_text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
    user_text = st.text_area("Masukkan teks yang ingin dianalisis:", default_text, height=150)

    num_runs = 1

    if st.button("Mulai Analisis"):
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
            time_recur = 0
            error_msg = "Teks terlalu panjang untuk metode Rekursif (Batas rekursi tercapai)."

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.info(f"Kata Terpanjang: {res_iter}")
        with col_res2:
            st.info(f"Jumlah Kata: {len(listKata)}")

        st.divider()
        st.subheader("Perbandingan Performa (Waktu Eksekusi)")
        
        if error_msg:
            st.error(error_msg)
        else:
            data = {
                "Metode": ["Iteratif", "Rekursif"],
                "Waktu (ms)": [time_iter, time_recur]
            }
            df = pd.DataFrame(data)

            c1, c2 = st.columns([1, 2])
            with c1:
                st.write(df)
                ratio = time_recur / time_iter if time_iter > 0 else 0
                st.metric("Rasio Kelambatan", f"{ratio:.2f}x", delta="Rekursif lebih lambat", delta_color="inverse")

            with c2:
                fig, ax = plt.subplots(figsize=(8, 4))
                colors = ['#4CAF50', '#F44336']
                ax.bar(df["Metode"], df["Waktu (ms)"], color=colors)
                ax.set_ylabel("Waktu (ms)")
                ax.set_title("Iteratif vs Rekursif (Semakin rendah semakin baik)")
                st.pyplot(fig)

if __name__ == "__main__":
    main()