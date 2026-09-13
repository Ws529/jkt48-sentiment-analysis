# 📊 Analisis Sentimen Fans JKT48 terhadap Kenaikan Harga M&G dan 2-Shot

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-IndoBERT-blue?style=for-the-badge)

Dashboard analitik interaktif untuk menganalisis respons dan kecenderungan sentimen fans JKT48 di platform X (Twitter) terkait penyesuaian harga tiket event **Meet & Greet (M&G) / Photocard** dan **2-Shot**.

---

## 📌 Konteks Penelitian

Pada pertengahan September 2026, JKT48 mengumumkan penyesuaian harga tiket untuk dua jenis produk event utama:

| Produk Event | Harga Lama | Harga Baru | Kenaikan Nominal | Kenaikan (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Meet & Greet / Photocard** | Rp50.000 | Rp60.000 | +Rp10.000 | **+20,00%** |
| **2-Shot** | Rp180.000 | Rp200.000 | +Rp20.000 | **+11,11%** |

Perubahan harga tersebut memicu berbagai percakapan dan dinamika respons di media sosial. Penelitian ini menggunakan pendekatan **Natural Language Processing (NLP)** untuk memetakan distribusi sentimen fans secara terukur.

---

## 📊 Hasil Utama & Distribusi Sentimen

Dari total **264 post publik** yang dikumpulkan dari platform X dan di-label secara cermat:

* 🔴 **Negatif:** 209 post (**79,17%**) — Mendominasi seluruh kategori produk.
* 🟡 **Netral:** 46 post (**17,42%**) — Diskusi logis seputar harga, perbandingan, & informasi.
* 🟢 **Positif:** 9 post (**3,41%**) — Dukungan atau penerimaan terhadap kebijakan baru.

### Distribusi Berdasarkan Kategori Produk:
- **2-Shot:** 77,78% Negatif \| 13,33% Netral \| 8,89% Positif
- **M&G:** 78,05% Negatif \| 14,63% Netral \| 7,32% Positif
- **Both (Keduanya):** 79,78% Negatif \| 19,10% Netral \| 1,12% Positif

---

## 🤖 Evaluasi Model NLP

Tiga arsitektur model diuji untuk melakukan klasifikasi sentimen:

| Model | Accuracy | Macro F1 | Weighted F1 | Keterangan |
| :--- | :---: | :---: | :---: | :--- |
| **Logistic Regression + TF-IDF** | 73,58% | 0,4111 | 0,7300 | Baseline Model |
| **Linear SVM + TF-IDF** | 73,58% | 0,3902 | 0,7200 | 5-Fold CV Accuracy: 76,88% |
| **IndoBERT (Transformers)** 🏆 | **75,47%** | **0,4190** | **0,7472** | **Model Terbaik** |

> ⚠️ **Catatan Keterbatasan (Limitations):**  
> Dataset memiliki ketidakseimbangan kelas (*class imbalance*) yang signifikan (sentimen positif hanya 9 sampel). Oleh karena itu, metrik **Macro F1** menjadi indikator evaluasi utama.

---

## ✨ Fitur Dashboard

* 🎨 **Modern Dark Mode Aesthetic:** Desain clean, profesional, dan nyaman untuk presentasi akademik.
* 📈 **Visualisasi Interaktif (Plotly):** Bar chart distribusi sentimen & perbandingan antarkategori produk.
* 🔍 **Filtering Dinamis:** Filter berdasarkan kategori produk (`2-Shot`, `M&G`, `Both`) dan kelas sentimen.
* 🛡️ **Privasi & Censorship Engine:** Sensor otomatis kata-kata kasar/profanity, anonimisasi `@username` $\rightarrow$ `@user`, dan penyederhanaan link.
* 💡 **Insight Otomatis:** Generasi poin insight kunci secara matematis sesuai filter aktif.
* 🗂️ **Deskripsi Dataset & Export:** Penjelasan struktur kolom, distribusi kelas, serta tombol *Download Dataset (CSV)* teranonimkan.


## 💻 Menjalankan Secara Lokal

1. **Clone repositori:**
   ```bash
   git clone https://github.com/Ws529/jkt48-sentiment-analysis.git
   cd jkt48-sentiment-analysis
   ```

2. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi Streamlit:**
   ```bash
   python -m streamlit run app.py
   ```

4. Buka browser di `http://localhost:8501`.

---

## 📝 Lisensi & Disclaimer

Data yang digunakan dalam penelitian ini merupakan data publik platform X yang telah dialiasikasi/dianonimkan demi privasi. Hasil analisis hanya merepresentasikan data percakapan sampel yang berhasil dikumpulkan dan bukan gambaran keseluruhan fans JKT48.
