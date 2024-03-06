# Import library yang diperlukan
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Membaca data
day = pd.read_csv('day.csv')
hour = pd.read_csv("hour.csv")
bike_sharing = pd.read_csv("bike_sharing.csv")

# Menampilkan judul dan informasi kontak
st.title('Proyek Analisis Data: Bike Sharing Dataset')
st.header('Nama: Ainur Rokhimah')
st.subheader('Email: M008D4KX2937@bangkit.academy')
st.write('\n')
st.write('\n')

# Menampilkan data
st.subheader('Data yang Digunakan')
tab1, tab2, tab3 = st.tabs(["day.csv", "hour.csv", "Data Gabungan"])
 
with tab1:
    st.write(day)
 
with tab2:
    st.write(hour)
 
with tab3:
    st.write(bike_sharing)

# Menghapus kolom 'dteday' yang tidak diperlukan
bike_sharing.drop('dteday', axis=1, inplace=True)

# Menampilkan grafik korelasi
st.subheader('Heatmap Korelasi')
correlation_matrix = bike_sharing.corr()
fig, ax = plt.subplots(figsize=(16, 12))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, annot_kws={"size": 10}, ax=ax)
st.pyplot(fig)

# Pertanyaan 1: Bagaimana pengaruh musim terhadap jumlah peminjaman sepeda harian
st.subheader('Pertanyaan 1: Pengaruh Musim Terhadap Jumlah Peminjaman Sepeda Harian')
# Menghitung rata-rata jumlah sewa harian untuk setiap musim
seasonal_data = bike_sharing.groupby('season_daily')['cnt_daily'].mean()
# Mengurutkan musim berdasarkan rata-rata jumlah sewa harian secara menurun
seasonal_data_sorted = seasonal_data.sort_values(ascending=False)
# Membuat grafik batang setelah data diurutkan
st.bar_chart(seasonal_data_sorted)
with st.expander("See explanation"):
    st.write(
        """Grafik di atas memberikan wawasan mendalam tentang pengaruh musim terhadap jumlah peminjaman sepeda harian. Visualisasi tersebut menggunakan bar plot yang menggambarkan rata-rata jumlah peminjaman sepeda harian untuk setiap musim, dengan musim gugur (Fall) memuncaki daftar diikuti oleh musim panas (Summer) dan musim dingin (Winter). Data yang dibulatkan pada setiap batang bar memberikan informasi lebih lanjut tentang tingkat peminjaman yang sebenarnya. Ini menunjukkan bahwa musim memiliki pengaruh signifikan pada tingkat peminjaman sepeda, dengan musim gugur menjadi puncak aktivitas peminjaman.
        """
    )
# Menambahkan nilai rata-rata yang dibulatkan pada tiap batang
for i, value in enumerate(seasonal_data_sorted):
    rounded_value = round(value)
    st.text(f'Musim: {seasonal_data_sorted.index[i]}, Rata-rata Jumlah Sewa Harian: {rounded_value}')

# Pertanyaan 2: Bagaimana pengaruh cuaca terhadap peminjaman sepeda?
st.subheader('Pertanyaan 2: Bagaimana pengaruh cuaca terhadap peminjaman sepeda?')
weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain'}
bike_sharing['weathersit_hourly'] = bike_sharing['weathersit_hourly'].replace(weather_mapping)
# Menampilkan pilihan kondisi cuaca yang dapat dipilih
selected_weather = st.selectbox("Pilih Kondisi Cuaca", bike_sharing['weathersit_hourly'].unique())
fig = px.box(bike_sharing[bike_sharing['weathersit_hourly'] == selected_weather], 
             x='weathersit_hourly', y='cnt_daily', 
             labels={'cnt_daily': 'Total Peminjaman'},
             category_orders={'weathersit_hourly': ['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain']})
fig.update_layout(title=f'Pengaruh Cuaca terhadap Peminjaman Sepeda ({selected_weather})',
                  xaxis_title='Kondisi Cuaca',
                  yaxis_title='Total Peminjaman')
st.plotly_chart(fig)
with st.expander("See explanation"):
    st.write(
        """Grafik di atas memberikan wawasan tentang pengaruh cuaca terhadap peminjaman sepeda. Visualisasi tersebut menggunakan boxplot yang menggambarkan distribusi data peminjaman sepeda dari setiap cuaca, dengan kondisi cuaca cerah (Clear) memuncaki daftar diikuti oleh cuaca kabut (Mist) dan cuaca salju ringan/hujan (Light Snow/Rain). Hasil ini mengindikasikan bahwa cuaca yang cerah dan bersahabat cenderung meningkatkan minat masyarakat untuk menggunakan layanan peminjaman sepeda, sedangkan kondisi cuaca yang kurang nyaman seperti hujan atau kabut dapat berdampak negatif pada tingkat peminjaman sepeda.
        """
    )

# Pertanyaan 3: Bagaimana pola peminjaman sepeda berdasarkan hari kerja dan hari libur?
st.subheader('Pertanyaan 3: Bagaimana pola peminjaman sepeda berdasarkan hari kerja dan hari libur?')
# Membuat pie chart
fig = px.pie(bike_sharing, names='workingday_daily', title='Pola Peminjaman Sepeda Berdasarkan Hari Kerja dan Hari Libur',
             labels=['Hari Kerja', 'Hari Libur'], color_discrete_map={'0': 'lightcoral', '1': 'skyblue'})
st.plotly_chart(fig)
with st.expander("See explanation"):
    st.write(
        """Visualisasi menggunakan pie chart ini memberikan gambaran tentang pola peminjaman sepeda berdasarkan hari kerja dan hari libur. Dengan melihat pie chart, dapat disimpulkan bahwa sebagian besar peminjaman sepeda terjadi pada hari kerja, dengan persentase sebesar 68,3%. Sementara itu, peminjaman pada hari libur menyumbang sekitar 31,7% dari total peminjaman.
        """
    )

# Pertanyaan 4: Bagaimana hubungan antara suhu dan peminjaman sepeda?
st.subheader('Pertanyaan 4: Bagaimana hubungan antara suhu dan peminjaman sepeda?')
# Membuat scatter plot
fig = px.scatter(bike_sharing, x='temp_daily', y='cnt_daily', title='Hubungan antara Suhu dan Peminjaman Sepeda',
                 labels={'temp_daily': 'Suhu (Normalized)', 'cnt_daily': 'Total Peminjaman'})
st.plotly_chart(fig)
with st.expander("See explanation"):
    st.write(
        """Visualisasi menggunakan scatter plot ini memberikan gambaran yang jelas tentang hubungan antara suhu harian dan jumlah peminjaman sepeda. Dengan melihat scatter plot, terlihat bahwa terdapat korelasi positif yang cukup kuat antara suhu harian (dinyatakan dalam nilai terormalisasi) dan total peminjaman sepeda. Titik-titik pada plot cenderung membentuk pola yang naik, menunjukkan bahwa ketika suhu harian meningkat, jumlah peminjaman sepeda juga cenderung meningkat, dan sebaliknya.
        """
    )

# Kesimpulan
st.subheader("Kesimpulan")
st.markdown("- **Pertanyaan 1:** Musim memiliki pengaruh signifikan pada tingkat peminjaman sepeda, dengan musim gugur (fall) menjadi puncak aktivitas peminjaman.")
st.markdown("- **Pertanyaan 2:** Cuaca yang cerah dan bersahabat cenderung meningkatkan minat masyarakat untuk menggunakan layanan peminjaman sepeda, sedangkan kondisi cuaca yang kurang nyaman seperti hujan atau kabut dapat berdampak negatif pada tingkat peminjaman sepeda.")
st.markdown("- **Pertanyaan 3:** Sebagian besar peminjaman sepeda terjadi pada hari kerja, dengan persentase sebesar 68,3%. Sementara itu, peminjaman pada hari libur menyumbang sekitar 31,7% dari total peminjaman.")
st.markdown("- **Pertanyaan 4:** Terdapat korelasi positif yang cukup kuat antara suhu harian (dinyatakan dalam nilai terormalisasi) dan total peminjaman sepeda. Kesimpulan ini konsisten dengan ekspektasi umum, di mana cuaca yang lebih hangat dan nyaman cenderung mendorong lebih banyak orang untuk menggunakan sepeda.")