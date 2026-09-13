"""Helper functions for JKT48 Sentiment Dashboard."""
import re
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --- Color Constants ---
COLORS = {
    "bg": "#1a1d23",
    "card": "#23272f",
    "card_border": "#2d3240",
    "text": "#e0e0e0",
    "text_muted": "#8b919a",
    "negative": "#e05555",
    "neutral": "#e0a830",
    "positive": "#4caf7d",
    "accent": "#5b8def",
}

SENTIMENT_COLORS = {
    "negative": COLORS["negative"],
    "neutral": COLORS["neutral"],
    "positive": COLORS["positive"],
}

PROFANITY_LIST = [
    r"\banjing\b", r"\banjir\b", r"\banjay\b", r"\bbangsat\b", r"\bbajingan\b",
    r"\bgoblok\b", r"\btolol\b", r"\bbego\b", r"\bbegok?\b", r"\basu\b",
    r"\btai\b", r"\btaik\b", r"\bkontol\b", r"\bkntl\b", r"\bmemek\b",
    r"\bmmk\b", r"\bngentot\b", r"\bngntot\b", r"\bjancok\b", r"\bjancuk\b",
    r"\b[cC][oO][kK]\b", r"\b[cC][uU][kK]\b", r"\bkampret\b", r"\bbrengsek\b",
    r"\bsetan\b", r"\bfuck\b", r"\bfucking\b", r"\bshit\b", r"\bbitch\b",
    r"\basshole\b", r"\basw\b", r"\banjer\b", r"\banjrit\b", r"\banjrot\b",
    r"\bbgst\b", r"\bbangke\b", r"\bbabi\b", r"\bmonyet\b", r"\bsialan\b",
    r"\bpuki\b", r"\btempik\b", r"\bdongo\b", r"\bnjengg?\b", r"\bmpruy\b",
    r"\bpakyu\b",
]

PROFANITY_PATTERN = re.compile("|".join(PROFANITY_LIST), re.IGNORECASE)


def censor_text(text: str) -> str:
    """Replace profanity with asterisks."""
    if not isinstance(text, str):
        return text
    return PROFANITY_PATTERN.sub(lambda m: "*" * len(m.group()), text)


def anonymize_usernames(text: str) -> str:
    """Replace @username mentions with @user."""
    if not isinstance(text, str):
        return text
    return re.sub(r"@\w+", "@user", text)


def clean_urls(text: str) -> str:
    """Replace URLs with [link]."""
    if not isinstance(text, str):
        return text
    return re.sub(r"https?://\S+", "[link]", text)


def clean_text_for_display(text: str) -> str:
    """Apply all display cleaning: censor, anonymize, clean URLs."""
    text = censor_text(text)
    text = anonymize_usernames(text)
    text = clean_urls(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


@st.cache_data
def load_data():
    """Load and prepare the dataset."""
    df = pd.read_csv("jkt48_sentiment_final_labeled.csv")
    df["text_display"] = df["text_raw"].apply(clean_text_for_display)
    return df


def fmt_pct(value: float) -> str:
    """Format percentage Indonesian style."""
    return f"{value:.2f}%".replace(".", ",")


def fmt_rp(value: int) -> str:
    """Format Rupiah Indonesian style."""
    return f"Rp{value:,.0f}".replace(",", ".")


def calculate_metrics(df: pd.DataFrame) -> dict:
    """Calculate sentiment metrics from dataframe."""
    total = len(df)
    if total == 0:
        return {"total": 0, "neg": 0, "neu": 0, "pos": 0,
                "neg_pct": 0, "neu_pct": 0, "pos_pct": 0}
    neg = (df["final_sentiment"] == "negative").sum()
    neu = (df["final_sentiment"] == "neutral").sum()
    pos = (df["final_sentiment"] == "positive").sum()
    return {
        "total": total, "neg": neg, "neu": neu, "pos": pos,
        "neg_pct": neg / total * 100,
        "neu_pct": neu / total * 100,
        "pos_pct": pos / total * 100,
    }


def create_sentiment_chart(df: pd.DataFrame) -> go.Figure:
    """Create sentiment distribution bar chart."""
    counts = df["final_sentiment"].value_counts()
    total = len(df)
    order = ["negative", "neutral", "positive"]
    labels_id = {"negative": "Negatif", "neutral": "Netral", "positive": "Positif"}
    vals = [counts.get(s, 0) for s in order]
    pcts = [v / total * 100 if total > 0 else 0 for v in vals]
    colors = [SENTIMENT_COLORS[s] for s in order]

    fig = go.Figure(go.Bar(
        x=[labels_id[s] for s in order], y=vals,
        marker_color=colors,
        text=[f"{v}<br>{fmt_pct(p)}" for v, p in zip(vals, pcts)],
        textposition="outside", textfont=dict(color="#e0e0e0", size=13),
        hovertemplate="<b>%{x}</b><br>Jumlah: %{y}<br><extra></extra>",
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0", family="Inter, sans-serif"),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#2d3240"),
        height=380, margin=dict(t=30, b=40, l=50, r=20),
    )
    return fig


def create_product_chart_count(df: pd.DataFrame) -> go.Figure:
    """Create grouped bar chart by product (count)."""
    order = ["negative", "neutral", "positive"]
    labels_id = {"negative": "Negatif", "neutral": "Netral", "positive": "Positif"}
    prod_map = {"2SHOT": "2-Shot", "MNG": "M&G", "BOTH": "Both"}
    products = [p for p in ["2SHOT", "MNG", "BOTH"] if p in df["product"].unique()]
    fig = go.Figure()
    for s in order:
        vals = []
        for p in products:
            vals.append(len(df[(df["product"] == p) & (df["final_sentiment"] == s)]))
        fig.add_trace(go.Bar(
            name=labels_id[s], x=[prod_map.get(p, p) for p in products], y=vals,
            marker_color=SENTIMENT_COLORS[s],
            text=vals, textposition="outside",
            textfont=dict(color="#e0e0e0", size=11),
        ))
    fig.update_layout(
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0", family="Inter, sans-serif"),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#2d3240"),
        height=380, margin=dict(t=30, b=40, l=50, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    return fig


def create_product_chart_pct(df: pd.DataFrame) -> go.Figure:
    """Create stacked bar chart by product (percentage)."""
    order = ["negative", "neutral", "positive"]
    labels_id = {"negative": "Negatif", "neutral": "Netral", "positive": "Positif"}
    prod_map = {"2SHOT": "2-Shot", "MNG": "M&G", "BOTH": "Both"}
    products = [p for p in ["2SHOT", "MNG", "BOTH"] if p in df["product"].unique()]
    fig = go.Figure()
    for s in order:
        vals = []
        for p in products:
            sub = df[df["product"] == p]
            t = len(sub)
            c = len(sub[sub["final_sentiment"] == s])
            vals.append(c / t * 100 if t > 0 else 0)
        fig.add_trace(go.Bar(
            name=labels_id[s], x=[prod_map.get(p, p) for p in products], y=vals,
            marker_color=SENTIMENT_COLORS[s],
            text=[fmt_pct(v) for v in vals], textposition="inside",
            textfont=dict(color="white", size=11),
        ))
    fig.update_layout(
        barmode="stack",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0", family="Inter, sans-serif"),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False, range=[0, 105]),
        height=380, margin=dict(t=30, b=40, l=50, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    return fig


def create_model_chart(metric: str) -> go.Figure:
    """Create model comparison bar chart for a given metric."""
    models = ["Logistic Regression", "Linear SVM", "IndoBERT"]
    data = {
        "Accuracy": [73.58, 73.58, 75.47],
        "Macro F1": [0.4111, 0.3902, 0.4190],
        "Weighted F1": [0.7300, 0.7200, 0.7472],
    }
    vals = data[metric]
    colors = ["#5b8def", "#5b8def", "#4caf7d"]
    if metric == "Accuracy":
        texts = [fmt_pct(v) for v in vals]
    else:
        texts = [f"{v:.4f}".replace(".", ",") for v in vals]
    fig = go.Figure(go.Bar(
        x=models, y=vals, marker_color=colors,
        text=texts, textposition="outside",
        textfont=dict(color="#e0e0e0", size=13),
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0", family="Inter, sans-serif"),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#2d3240"),
        height=350, margin=dict(t=30, b=40, l=50, r=20),
    )
    return fig
