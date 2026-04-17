# Pengantar Pemrograman dan Rekayasa AI (Artificial Intelligence)

## Pendahuluan
Sesi ini akan memberikan pemahaman dasar tentang apa itu Kecerdasan Buatan (AI), Pembelajaran Mesin (Machine Learning/ML), dan Pembelajaran Mendalam (Deep Learning/DL). Kita akan membahas konsep-konsep inti, mengapa AI penting saat ini, serta melihat sekilas bagaimana pemrograman dan rekayasa terlibat dalam pengembangan sistem AI.

**Durasi:** 2 Jam

## Prasyarat
*   Pemahaman dasar tentang pemrograman (preferable Python).
*   Pemahaman dasar tentang matematika (aljabar linear, kalkulus dasar) - *konseptual saja*.
*   Keingintahuan tentang bagaimana teknologi AI bekerja.

## Tujuan Pembelajaran
Setelah sesi ini, Anda diharapkan dapat:
1.  Memahami definisi dan perbedaan antara AI, ML, dan DL.
2.  Menjelaskan mengapa AI memiliki dampak signifikan dalam berbagai industri.
3.  Mengenali tahapan dasar dalam siklus hidup proyek AI (data, model, pelatihan, inferensi).
4.  Memahami peran utama pemrograman Python dan pustaka populer dalam AI.
5.  Mengenali beberapa konsep dasar dalam rekayasa AI (AI Engineering).
6.  Menyadari pentingnya etika dalam pengembangan AI.

---

## Modul 1: Memahami AI, ML, dan DL (± 30 menit)

### 1.1 Apa itu Kecerdasan Buatan (AI)?
*   Definisi umum: Mesin yang meniru "kognisi" manusia (pemecahan masalah, pembelajaran, pengambilan keputusan).
*   AI sebagai payung besar.
*   Contoh: Sistem rekomendasi, asisten suara, mobil otonom.

### 1.2 Pembelajaran Mesin (Machine Learning - ML)
*   Definisi: Subset AI yang memungkinkan sistem "belajar" dari data tanpa diprogram secara eksplisit.
*   Jenis-jenis Pembelajaran Mesin (overview):
    *   **Supervised Learning:** Belajar dari data berlabel (klasifikasi, regresi).
    *   **Unsupervised Learning:** Mencari pola dalam data tidak berlabel (clustering, dimensionality reduction).
    *   **Reinforcement Learning:** Belajar melalui coba-coba dan umpan balik (games, robotika).
*   Contoh: Deteksi spam email, prediksi harga rumah.

### 1.3 Pembelajaran Mendalam (Deep Learning - DL)
*   Definisi: Subset ML yang menggunakan jaringan saraf tiruan (Artificial Neural Networks/ANNs) dengan banyak lapisan (deep).
*   Kekuatan DL: Otomatisasi ekstraksi fitur dari data mentah (gambar, suara, teks).
*   Contoh: Pengenalan wajah, terjemahan bahasa, pengolahan bahasa alami (NLP).

---

## Modul 2: Konsep Dasar Pemrograman AI (± 45 menit)

### 2.1 Python sebagai Bahasa Pilihan AI
*   Mengapa Python? Sintaksis yang mudah dibaca, ekosistem pustaka yang kaya, komunitas besar.

### 2.2 Pustaka Kunci dalam AI Python (Overview Singkat)
*   **NumPy:** Komputasi numerik dengan array multidimensional.
*   **Pandas:** Manipulasi dan analisis data.
*   **Scikit-learn:** Pustaka ML klasik (regresi, klasifikasi, clustering).
*   **TensorFlow / PyTorch:** Pustaka DL untuk membangun dan melatih jaringan saraf tiruan (ANNs).

### 2.3 Siklus Hidup Proyek AI Sederhana
1.  **Pengumpulan Data:** Mendapatkan data yang relevan.
2.  **Pra-pemrosesan Data:** Membersihkan, mengubah, dan menyiapkan data.
3.  **Pemilihan Model:** Memilih algoritma ML yang sesuai.
4.  **Pelatihan Model:** Menggunakan data untuk "mengajarkan" model.
5.  **Evaluasi Model:** Mengukur kinerja model.
6.  **Inferensi/Prediksi:** Menggunakan model terlatih untuk membuat prediksi pada data baru.

### 2.4 Contoh Kode Sederhana (Linear Regression dengan Scikit-learn)
```python
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 1. Data Dummy (Suhu vs. Penjualan Es Krim)
x = np.array([10, 15, 20, 25, 30]).reshape(-1, 1) # Suhu dalam Celsius
y = np.array([20, 30, 40, 50, 60]) # Penjualan Es Krim

# 2. Inisialisasi dan Latih Model Regresi Linear
model = LinearRegression()
model.fit(x, y)

# 3. Prediksi
new_temp = np.array([[22]]) # Suhu baru
prediction = model.predict(new_temp)

print(f"Jika suhu {new_temp[0][0]}°C, prediksi penjualan es krim adalah: {prediction[0]:.2f}")

# 4. Visualisasi (Opsional)
plt.scatter(x, y, color='blue', label='Data Asli')
plt.plot(x, model.predict(x), color='red', label='Garis Regresi')
plt.xlabel("Suhu (°C)")
plt.ylabel("Penjualan Es Krim")
plt.title("Regresi Linear: Suhu vs. Penjualan Es Krim")
plt.legend()
plt.grid(True)
plt.show()
```

---

## Modul 3: Konsep Rekayasa AI (AI Engineering) dan Etika (± 30 menit)

### 3.1 Apa itu Rekayasa AI?
*   Definisi: Disiplin yang berfokus pada pembangunan, pengujian, dan penerapan sistem AI ke dalam produksi.
*   Lebih dari sekadar ML: Mencakup seluruh siklus hidup pengembangan sistem AI, termasuk infrastruktur, operasional, dan pemeliharaan.

### 3.2 Aspek Kunci Rekayasa AI (Tingkat Tinggi)
*   **Data Pipelines:** Otomatisasi aliran data dari sumber ke model.
*   **MLOps (Machine Learning Operations):** Praktik untuk mengotomatisasi dan menyederhanakan siklus hidup ML (mirip DevOps).
*   **Monitoring & Pemeliharaan:** Memastikan model terus berkinerja baik di lingkungan produksi.
*   **Skalabilitas & Efisiensi:** Mendesain sistem AI yang dapat menangani data besar dan permintaan tinggi.

### 3.3 Pertimbangan Etika dalam AI
*   **Bias Data:** Model AI dapat mewarisi bias dari data pelatihan.
*   **Transparansi & Akuntabilitas:** Bagaimana model membuat keputusan?
*   **Privasi Data:** Perlindungan informasi sensitif.
*   **Dampak Sosial:** Pekerjaan, diskriminasi, pengambilan keputusan otomatis.
*   Pentingnya pengembangan AI yang bertanggung jawab dan adil.

---

## Tanya Jawab & Diskusi (± 15 menit)
