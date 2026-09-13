"""
JKT48 Sentiment Analysis Dashboard
Analisis Sentimen Fans JKT48 terhadap Kenaikan Harga M&G dan 2-Shot
"""
import streamlit as st
import pandas as pd
import os
from helpers import (
    load_data, calculate_metrics, fmt_pct, fmt_rp,
    create_sentiment_chart, create_product_chart_count,
    create_product_chart_pct, create_model_chart, COLORS,
)

# ── Page Config ──
st.set_page_config(
    page_title="Analisis Sentimen JKT48",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
:root {{
    --bg: {COLORS['bg']};
    --card: {COLORS['card']};
    --border: {COLORS['card_border']};
    --text: {COLORS['text']};
    --muted: {COLORS['text_muted']};
    --negative: {COLORS['negative']};
    --neutral: {COLORS['neutral']};
    --positive: {COLORS['positive']};
    --accent: {COLORS['accent']};
}}
html, body, .stApp {{
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}}
.stApp > header {{ background-color: transparent !important; }}
section[data-testid="stSidebar"] {{
    background-color: #1e2129 !important;
    border-right: 1px solid var(--border) !important;
}}
section[data-testid="stSidebar"] * {{ color: var(--text) !important; }}
h1, h2, h3, h4, h5, h6 {{ color: var(--text) !important; font-family: 'Inter', sans-serif !important; }}
.block-container {{ padding-top: 2rem !important; max-width: 1200px; }}

/* Card base */
.card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}}
.card-sm {{ padding: 1rem 1.2rem; }}

/* Hero */
.hero {{
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    margin-bottom: 0.5rem;
}}
.hero h1 {{
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
    letter-spacing: -0.02em;
}}
.hero p {{
    color: var(--muted);
    font-size: 0.95rem;
    max-width: 700px;
    margin: 0 auto 1rem;
    line-height: 1.6;
}}
.badge {{
    display: inline-block;
    background: rgba(91,141,239,0.12);
    color: var(--accent);
    font-size: 0.75rem;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 0 3px;
    border: 1px solid rgba(91,141,239,0.2);
}}

/* KPI Cards */
.kpi {{
    text-align: center;
    padding: 1.2rem 0.8rem;
}}
.kpi .label {{ color: var(--muted); font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }}
.kpi .value {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 2px; }}
.kpi .sub {{ font-size: 0.85rem; font-weight: 400; }}

/* Price cards */
.price-card {{
    text-align: center;
}}
.price-card .title {{ font-weight: 600; font-size: 1rem; margin-bottom: 12px; color: var(--accent); }}
.price-old {{ color: var(--muted); text-decoration: line-through; font-size: 0.95rem; }}
.price-new {{ font-size: 1.4rem; font-weight: 700; color: var(--text); margin: 4px 0; }}
.price-delta {{ font-size: 0.85rem; font-weight: 500; }}

/* Section header */
.section-header {{
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    margin: 2rem 0 1rem !important;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}}

/* Insight */
.insight {{
    background: var(--card);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.7rem;
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--text);
}}

/* Conclusion */
.conclusion {{
    background: linear-gradient(135deg, rgba(91,141,239,0.08), rgba(76,175,125,0.06));
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
}}
.conclusion h3 {{ margin-top: 0 !important; }}

/* Model table */
.model-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
.model-table th {{ background: rgba(91,141,239,0.1); padding: 10px 14px; text-align: left; border-bottom: 2px solid var(--border); font-weight: 600; }}
.model-table td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); }}
.model-table tr:last-child {{ background: rgba(76,175,125,0.08); }}
.best-badge {{ background: var(--positive); color: #fff; font-size: 0.7rem; padding: 2px 8px; border-radius: 10px; margin-left: 6px; font-weight: 600; }}

/* Footer */
.footer {{
    text-align: center;
    color: var(--muted);
    font-size: 0.78rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
.stTabs [data-baseweb="tab"] {{
    background: var(--card) !important;
    color: var(--muted) !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 8px 20px !important;
    border: 1px solid var(--border) !important;
    border-bottom: none !important;
}}
.stTabs [aria-selected="true"] {{
    background: rgba(91,141,239,0.15) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
}}

/* Dataframe */
.stDataFrame {{ border-radius: 8px; overflow: hidden; }}

/* Expander */
.streamlit-expanderHeader {{ font-weight: 600 !important; font-size: 0.95rem !important; }}

/* Hide default Streamlit elements */
#MainMenu, footer, .stDeployButton {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# ── Load Data ──
if not os.path.exists("jkt48_sentiment_final_labeled.csv"):
    st.error("⚠️ File dataset 'jkt48_sentiment_final_labeled.csv' tidak ditemukan. Pastikan file berada di direktori yang sama dengan app.py.")
    st.stop()

df = load_data()

# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🔍 Filter Analisis")
    st.markdown("---")

    prod_options = {"Semua": None, "2-Shot": "2SHOT", "M&G": "MNG", "Both": "BOTH"}
    selected_products = st.multiselect(
        "Produk",
        options=list(prod_options.keys())[1:],
        default=list(prod_options.keys())[1:],
    )
    selected_sentiments = st.multiselect(
        "Sentimen",
        options=["negative", "neutral", "positive"],
        default=["negative", "neutral", "positive"],
        format_func=lambda x: {"negative": "Negative", "neutral": "Neutral", "positive": "Positive"}[x],
    )

    if st.button("🔄 Reset Filter", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.caption("Gunakan filter untuk mempersempit analisis berdasarkan produk dan sentimen.")

# Apply filters
prod_vals = [prod_options[p] for p in selected_products if prod_options.get(p)]
if not prod_vals:
    prod_vals = df["product"].unique().tolist()
if not selected_sentiments:
    selected_sentiments = ["negative", "neutral", "positive"]

filtered = df[df["product"].isin(prod_vals) & df["final_sentiment"].isin(selected_sentiments)]

# ══════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════
st.markdown("""
<div class="hero">
    <h1>Analisis Sentimen Fans JKT48 terhadap Kenaikan Harga M&G dan 2-Shot</h1>
    <p>Analisis respons fans di platform X terhadap perubahan harga tiket Meet & Greet dan 2-Shot menggunakan pendekatan Natural Language Processing.</p>
    <span class="badge">NLP</span>
    <span class="badge">Sentiment Analysis</span>
    <span class="badge">JKT48</span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# KONTEKS KENAIKAN HARGA
# ══════════════════════════════════════════
st.markdown('<div class="section-header">📋 Konteks Kenaikan Harga</div>', unsafe_allow_html=True)

col_p1, col_p2 = st.columns(2)
with col_p1:
    st.markdown(f"""
    <div class="card price-card">
        <div class="title">Meet & Greet / Photocard</div>
        <div class="price-old">{fmt_rp(50000)}</div>
        <div class="price-new">{fmt_rp(60000)}</div>
        <div class="price-delta" style="color: var(--negative);">+{fmt_rp(10000)} &nbsp;·&nbsp; +20%</div>
    </div>
    """, unsafe_allow_html=True)
with col_p2:
    st.markdown(f"""
    <div class="card price-card">
        <div class="title">2-Shot</div>
        <div class="price-old">{fmt_rp(180000)}</div>
        <div class="price-new">{fmt_rp(200000)}</div>
        <div class="price-delta" style="color: var(--negative);">+{fmt_rp(20000)} &nbsp;·&nbsp; +11,11%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="card card-sm" style="font-size:0.88rem; color: var(--muted); line-height:1.6;">
    Perubahan harga tersebut memicu beragam respons dari fans di media sosial. Analisis ini digunakan untuk melihat kecenderungan sentimen fans setelah kenaikan harga.
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════
st.markdown('<div class="section-header">📊 Ringkasan Sentimen</div>', unsafe_allow_html=True)

m = calculate_metrics(filtered)
kc1, kc2, kc3, kc4 = st.columns(4)

with kc1:
    st.markdown(f"""
    <div class="card kpi">
        <div class="label">Total Post</div>
        <div class="value" style="color: var(--accent);">{m['total']}</div>
    </div>""", unsafe_allow_html=True)
with kc2:
    st.markdown(f"""
    <div class="card kpi">
        <div class="label">Negatif</div>
        <div class="value" style="color: var(--negative);">{m['neg']}</div>
        <div class="sub" style="color: var(--negative);">{fmt_pct(m['neg_pct'])}</div>
    </div>""", unsafe_allow_html=True)
with kc3:
    st.markdown(f"""
    <div class="card kpi">
        <div class="label">Netral</div>
        <div class="value" style="color: var(--neutral);">{m['neu']}</div>
        <div class="sub" style="color: var(--neutral);">{fmt_pct(m['neu_pct'])}</div>
    </div>""", unsafe_allow_html=True)
with kc4:
    st.markdown(f"""
    <div class="card kpi">
        <div class="label">Positif</div>
        <div class="value" style="color: var(--positive);">{m['pos']}</div>
        <div class="sub" style="color: var(--positive);">{fmt_pct(m['pos_pct'])}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# EMPTY STATE CHECK
# ══════════════════════════════════════════
if len(filtered) == 0:
    st.info("ℹ️ Tidak ada data yang sesuai dengan filter. Silakan ubah filter di sidebar.")
    st.stop()

# ══════════════════════════════════════════
# DISTRIBUSI SENTIMEN
# ══════════════════════════════════════════
st.markdown('<div class="section-header">📈 Distribusi Sentimen</div>', unsafe_allow_html=True)
st.plotly_chart(create_sentiment_chart(filtered), use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# SENTIMEN BERDASARKAN PRODUK
# ══════════════════════════════════════════
st.markdown('<div class="section-header">📦 Sentimen Berdasarkan Produk</div>', unsafe_allow_html=True)

tab_count, tab_pct = st.tabs(["Jumlah Post", "Persentase"])
with tab_count:
    st.plotly_chart(create_product_chart_count(filtered), use_container_width=True, config={"displayModeBar": False})
with tab_pct:
    st.plotly_chart(create_product_chart_pct(filtered), use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# INSIGHT UTAMA
# ══════════════════════════════════════════
st.markdown('<div class="section-header">💡 Insight Utama</div>', unsafe_allow_html=True)

# Generate dynamic insights
insights = []
if m["total"] > 0:
    # Insight 1: dominant sentiment
    dominant = max(["neg", "neu", "pos"], key=lambda k: m[k])
    dom_map = {"neg": "negatif", "neu": "netral", "pos": "positif"}
    insights.append(f"{fmt_pct(m[dominant + '_pct'])} post menunjukkan sentimen {dom_map[dominant]}.")

    # Insight 2: product with most negative
    prod_neg = filtered[filtered["final_sentiment"] == "negative"]["product"].value_counts()
    if len(prod_neg) > 0:
        top_prod = prod_neg.index[0]
        prod_name = {"2SHOT": "2-Shot", "MNG": "M&G", "BOTH": "BOTH"}.get(top_prod, top_prod)
        insights.append(f"Kategori {prod_name} memiliki jumlah sentimen negatif terbesar, yaitu {prod_neg.iloc[0]} post.")

    # Insight 3: product with highest positive proportion
    for p in ["2SHOT", "MNG", "BOTH"]:
        sub = filtered[filtered["product"] == p]
        if len(sub) > 0:
            pos_count = (sub["final_sentiment"] == "positive").sum()
            pos_pct_val = pos_count / len(sub) * 100
            if p == filtered.groupby("product").apply(
                lambda x: (x["final_sentiment"] == "positive").sum() / len(x) * 100
            ).idxmax():
                pn = {"2SHOT": "2-Shot", "MNG": "M&G", "BOTH": "BOTH"}.get(p, p)
                insights.append(f"Proporsi sentimen positif tertinggi terdapat pada {pn} sebesar {fmt_pct(pos_pct_val)}.")
                break

    # Insight 4: consistency check
    all_neg_dominant = True
    for p in filtered["product"].unique():
        sub = filtered[filtered["product"] == p]
        if len(sub) > 0:
            neg_r = (sub["final_sentiment"] == "negative").sum() / len(sub) * 100
            if neg_r < 50:
                all_neg_dominant = False
    if all_neg_dominant and len(filtered["product"].unique()) > 1:
        insights.append("Sentimen negatif konsisten mendominasi seluruh kategori produk.")

for ins in insights:
    st.markdown(f'<div class="insight">{ins}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# DESKRIPSI DATASET
# ══════════════════════════════════════════
st.markdown('<div class="section-header">🗂️ Deskripsi Dataset</div>', unsafe_allow_html=True)

ds_col1, ds_col2 = st.columns(2)

with ds_col1:
    st.markdown(f"""
    <div class="card card-sm" style="line-height:1.8; font-size:0.88rem;">
        <div style="font-weight:600; font-size:0.95rem; margin-bottom:10px; color: var(--accent);">📄 Informasi Umum</div>
        <table style="width:100%; border-collapse:collapse;">
            <tr><td style="color:var(--muted); padding:4px 0; width:140px;">Sumber Data</td><td>Post publik platform X (Twitter)</td></tr>
            <tr><td style="color:var(--muted); padding:4px 0;">Total Data</td><td><b>264</b> post</td></tr>
            <tr><td style="color:var(--muted); padding:4px 0;">Format</td><td>CSV (Comma Separated Values)</td></tr>
            <tr><td style="color:var(--muted); padding:4px 0;">Nama File</td><td><code style="background:rgba(91,141,239,0.1); padding:2px 6px; border-radius:4px; font-size:0.82rem;">jkt48_sentiment_final_labeled.csv</code></td></tr>
            <tr><td style="color:var(--muted); padding:4px 0;">Periode</td><td>12–13 September 2026</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with ds_col2:
    st.markdown("""
    <div class="card card-sm" style="line-height:1.8; font-size:0.88rem;">
        <div style="font-weight:600; font-size:0.95rem; margin-bottom:10px; color: var(--accent);">📋 Struktur Kolom</div>
        <table style="width:100%; border-collapse:collapse;">
            <tr><td style="color:var(--muted); padding:4px 0; width:140px;"><code style="font-size:0.82rem;">post_id</code></td><td>ID unik setiap post</td></tr>
            <tr><td style="color:var(--muted); padding:4px 0;"><code style="font-size:0.82rem;">created_at</code></td><td>Waktu post dibuat</td></tr>
            <tr><td style="color:var(--muted); padding:4px 0;"><code style="font-size:0.82rem;">text_raw</code></td><td>Teks asli post</td></tr>
            <tr><td style="color:var(--muted); padding:4px 0;"><code style="font-size:0.82rem;">product</code></td><td>Kategori produk (2SHOT / MNG / BOTH)</td></tr>
            <tr><td style="color:var(--muted); padding:4px 0;"><code style="font-size:0.82rem;">final_sentiment</code></td><td>Label sentimen (negative / neutral / positive)</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# Distribusi kelas ringkas
st.markdown(f"""
<div class="card card-sm" style="font-size:0.88rem;">
    <div style="font-weight:600; font-size:0.95rem; margin-bottom:10px; color: var(--accent);">📊 Distribusi Kelas Sentimen</div>
    <div style="display:flex; gap:2rem; flex-wrap:wrap;">
        <div><span style="color:var(--negative); font-weight:600;">● Negative:</span> 209 post (79,17%)</div>
        <div><span style="color:var(--neutral); font-weight:600;">● Neutral:</span> 46 post (17,42%)</div>
        <div><span style="color:var(--positive); font-weight:600;">● Positive:</span> 9 post (3,41%)</div>
    </div>
    <p style="color:var(--muted); font-size:0.82rem; margin-top:8px; margin-bottom:0;">
        ⚠ Distribusi kelas sangat tidak seimbang — sentimen positif hanya mencakup 3,41% dari total dataset.
    </p>
</div>
""", unsafe_allow_html=True)

# Download button
csv_data = df[["post_id", "created_at", "text_raw", "product", "final_sentiment"]].to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Dataset (CSV)",
    data=csv_data,
    file_name="jkt48_sentiment_final_labeled.csv",
    mime="text/csv",
    use_container_width=True,
)

# ══════════════════════════════════════════
# DATA POST
# ══════════════════════════════════════════
st.markdown('<div class="section-header">📝 Data Post</div>', unsafe_allow_html=True)

search = st.text_input("🔎 Cari post...", placeholder="Ketik kata kunci untuk mencari...")

display_df = filtered[["created_at", "text_display", "product", "final_sentiment"]].copy()
display_df.columns = ["Waktu", "Post", "Produk", "Sentimen"]
display_df["Produk"] = display_df["Produk"].map({"2SHOT": "2-Shot", "MNG": "M&G", "BOTH": "Both"})

if search:
    display_df = display_df[display_df["Post"].str.contains(search, case=False, na=False)]

st.dataframe(
    display_df.reset_index(drop=True),
    use_container_width=True,
    height=450,
)

# ══════════════════════════════════════════
# EVALUASI MODEL NLP
# ══════════════════════════════════════════
st.markdown('<div class="section-header">🤖 Evaluasi Model NLP</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
<table class="model-table">
<thead><tr><th>Model</th><th>Accuracy</th><th>Macro F1</th><th>Weighted F1</th></tr></thead>
<tbody>
<tr><td>Logistic Regression</td><td>73,58%</td><td>0,4111</td><td>0,7300</td></tr>
<tr><td>Linear SVM</td><td>73,58%</td><td>0,3902</td><td>0,7200</td></tr>
<tr><td>IndoBERT <span class="best-badge">Model Terbaik</span></td><td>75,47%</td><td>0,4190</td><td>0,7472</td></tr>
</tbody>
</table>
</div>
""", unsafe_allow_html=True)

st.caption("Macro F1 digunakan sebagai salah satu metrik penting karena distribusi kelas tidak seimbang.")

tab_acc, tab_mf1, tab_wf1 = st.tabs(["Accuracy", "Macro F1", "Weighted F1"])
with tab_acc:
    st.plotly_chart(create_model_chart("Accuracy"), use_container_width=True, config={"displayModeBar": False})
with tab_mf1:
    st.plotly_chart(create_model_chart("Macro F1"), use_container_width=True, config={"displayModeBar": False})
with tab_wf1:
    st.plotly_chart(create_model_chart("Weighted F1"), use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# KESIMPULAN
# ══════════════════════════════════════════
st.markdown('<div class="section-header">📌 Kesimpulan Analisis</div>', unsafe_allow_html=True)

st.markdown("""
<div class="conclusion">
    <h3 style="font-size:1.1rem; font-weight:600;">Kesimpulan</h3>
    <p style="font-size:0.9rem; line-height:1.7; color: var(--text);">
        Berdasarkan 264 post yang dianalisis, respons fans terhadap kenaikan harga Meet & Greet dan 2-Shot
        didominasi oleh sentimen negatif sebesar 79,17%. Sentimen netral sebesar 17,42%, sedangkan sentimen
        positif hanya sebesar 3,41%.
    </p>
    <p style="font-size:0.9rem; line-height:1.7; color: var(--text);">
        Pola sentimen negatif juga konsisten pada kategori 2-Shot, Meet & Greet, maupun post yang membahas
        keduanya secara bersamaan. Hal ini menunjukkan bahwa kenaikan harga cenderung mendapat respons kurang
        baik dari fans.
    </p>
    <h3 style="font-size:1rem; font-weight:600; margin-top:1.5rem;">Interpretasi Model</h3>
    <p style="font-size:0.88rem; line-height:1.7; color: var(--text);">
        IndoBERT memperoleh performa terbaik dengan accuracy 75,47%, Macro F1 0,4190, dan Weighted F1 0,7472.
    </p>
    <h3 style="font-size:1rem; font-weight:600; margin-top:1.5rem; color: var(--neutral);">⚠ Keterbatasan</h3>
    <p style="font-size:0.88rem; line-height:1.7; color: var(--muted);">
        Keterbatasan utama analisis adalah ketidakseimbangan distribusi kelas, khususnya sentimen positif yang
        hanya berjumlah 9 data. Kondisi ini menyebabkan model memiliki kemampuan yang terbatas dalam mengenali
        kelas positif.
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# METODOLOGI & LIMITATIONS
# ══════════════════════════════════════════
with st.expander("📘 Metodologi Singkat"):
    st.markdown("""
**1. Data Acquisition**
Data dikumpulkan dari post publik platform X menggunakan query terkait kenaikan harga M&G dan 2-Shot.

**2. Data Cleaning**
Dilakukan deduplication, filtering bahasa, filtering relevansi, dan penghapusan noise.

**3. Annotation**
Data diklasifikasikan ke dalam sentimen negative, neutral, dan positive dengan manual review dan AI-assisted annotation.

**4. NLP Modeling**
Model yang diuji:
- Logistic Regression + TF-IDF
- Linear SVM + TF-IDF
- IndoBERT

**5. Evaluation**
Model dibandingkan menggunakan Accuracy, Macro F1, dan Weighted F1.

**Final dataset:** 264 post.
    """)

with st.expander("⚠️ Keterbatasan Data"):
    st.markdown("""
- Dataset hanya merepresentasikan post yang berhasil dikumpulkan dari platform X pada periode penelitian.
- Dataset tidak merepresentasikan seluruh fans JKT48.
- Distribusi kelas sangat tidak seimbang.
- Sentimen positif hanya berjumlah 9 post.
- Sarkasme dan bahasa informal dapat mempersulit klasifikasi.
- Beberapa konteks pada media sosial dapat bergantung pada gambar, quote post, atau konteks percakapan lain.
- Hasil analisis menggambarkan sentimen dari data yang tersedia, bukan keseluruhan opini fandom.
    """)

# ══════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════
st.markdown("""
<div class="footer">
    <p>JKT48 Sentiment Analysis • NLP Project</p>
    <p>Data source: public posts from X</p>
</div>
""", unsafe_allow_html=True)
