import streamlit as st
import io, re, json, base64
from PIL import Image
from datetime import datetime
import plotly.graph_objects as go

# ── CONFIGURATION & DESIGN ÉLITE ──────────────────────────────────────────────
st.set_page_config(page_title="EcoMaster Labo Pro", page_icon="🚀", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; background-color: #0e1117 !important; color: #F0F0F0 !important; }
  .main { background-color: #0e1117 !important; }
  .block-container { padding-top: 1.5rem !important; max-width: 1100px !important; }
  section[data-testid="stSidebar"] { background-color: #0a0d12 !important; border-right: 1px solid #1e2530 !important; }

  /* HERO BANNER */
  .hero-banner {
    background: linear-gradient(135deg, #0e0000 0%, #1a0000 40%, #0e0000 100%);
    border: 1px solid #D90429; border-radius: 20px;
    padding: 2rem; margin-bottom: 1.5rem; text-align: center;
    box-shadow: 0 0 50px rgba(217,4,41,0.15);
    animation: fadeInDown 0.7s ease both;
  }
  .hero-banner h1 { font-size: clamp(1.6rem, 5vw, 2.6rem); font-weight: 900; color: #FFF; margin: 0; }
  .hero-banner h1 span { color: #D90429; }
  .hero-banner .slogan { color: #888; margin: 0.4rem 0 0; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; }

  /* ANIMATIONS */
  @keyframes fadeInDown { from { opacity:0; transform:translateY(-25px); } to { opacity:1; transform:translateY(0); } }
  @keyframes fadeInUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
  @keyframes pulse { 0%,100% { box-shadow:0 0 0 0 rgba(217,4,41,0.4); } 50% { box-shadow:0 0 0 14px rgba(217,4,41,0); } }
  @keyframes glow { 0%,100% { box-shadow:0 0 20px rgba(217,4,41,0.25); } 50% { box-shadow:0 0 45px rgba(217,4,41,0.65); } }

  /* INPUTS */
  .stTextInput input, .stNumberInput input {
    background-color: #161b22 !important; color: #FFF !important;
    border: 1px solid #2a3140 !important; border-radius: 10px !important;
    transition: all 0.3s ease !important;
  }
  .stTextInput input:focus, .stNumberInput input:focus { border-color: #D90429 !important; }

  /* BOUTON ROUGE PULSANT */
  .stButton > button {
    background: linear-gradient(135deg, #D90429 0%, #a80220 50%, #D90429 100%) !important;
    background-size: 200% auto !important; color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 800 !important; font-size: 1rem !important;
    padding: 0.8rem 2rem !important; width: 100% !important; animation: pulse 2.5s infinite;
  }

  /* RESULT CARDS & TABLEAUX */
  .result-card { background: #161b22; border: 1px solid #2a3140; border-radius: 14px; padding: 1.4rem; margin-bottom: 1rem; }
  .gains-table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; text-align: center; }
  .gains-table th { background: #D90429; color: white; padding: 8px; font-size: 0.7rem; }
  .gains-table td { background: #0e1117; color: #CCC; padding: 10px; border-bottom: 1px solid #1e2530; }

  /* BOUTON COPIER DISCRET */
  .copy-btn-wrapper { float: right; }
  .copy-btn {
    background: #1a1a2a; color: #888; border: 1px solid #2a3140;
    border-radius: 6px; padding: 3px 8px; font-size: 0.7rem; cursor: pointer;
  }
  .copy-btn:hover { border-color: #D90429; color: #FFF; }
</style>

<script>
function copyToClipboard(text, btnId) {
  const el = document.createElement('textarea');
  el.value = text;
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);
  const btn = document.getElementById(btnId);
  btn.innerHTML = '✅ OK';
  setTimeout(() => { btn.innerHTML = '📋 Copier'; }, 2000);
}
</script>
""", unsafe_allow_html=True)

# ── LOGIQUE CALCULATEUR ───────────────────────────────────────────────────────

def get_pub_bracket(v):
    if v <= 10: return 6000 # ~10$
    elif v <= 20: return 12000 # ~20$
    return 20000

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#D90429;'>🚀 Labo Pro</h2>", unsafe_allow_html=True)
    st.write("🕒 **Historique de session**")
    if "history" not in st.session_state: st.session_state.history = []
    for i, h in enumerate(st.session_state.history):
        if st.button(f"📦 {h['name']}", key=f"h_{i}"):
            st.session_state.result = h["data"]
            st.session_state.analyzed = True
            st.rerun()

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero-banner"><h1>🚀 <span>EcoMaster</span> Labo Pro</h1>
<p class="slogan">Tout-en-un pour un e-commerce réussi</p><p class="sub">créé par LABO</p></div>""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    prod_name = st.text_input("📦 Nom du Produit", placeholder="Ex: Mini Vélo")
    pa = st.number_input("💰 Prix d'Achat (FCFA)", min_value=0, value=5000)
    target_sales = st.number_input("🎯 Objectif ventes / jour", min_value=1, value=10)
with col2:
    files = st.file_uploader("📸 Photos", accept_multiple_files=True)

# ── ANALYSE IA ────────────────────────────────────────────────────────────────
if st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True):
    from groq import Groq
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        # Prompt strict pour les 6 paragraphes de 4 phrases
        prompt = f"""Produit: {prod_name}. Achat: {pa} F.
        1. SHOPIFY: 3 titres + 6 paragraphes (Titre gras + MAX 4 phrases).
        2. ADS: 3 variantes (Titre choc + Texte fun MAX 5 lignes).
        3. VOIX-OFF: 3 scripts de MAX 130 mots. Titres: Argument 1, 2, 3.
        4. OFFRES: 3 offres neuromarketing.
        Réponds en JSON uniquement."""
        
        # [Ici l'appel IA classique que tu connais]
        # data = client.chat.completions.create(...)
        # st.session_state.result = data
        # st.session_state.analyzed = True
        # save_to_history(...)
    except Exception as e:
        st.error(f"Erreur : {e}")

# ── RÉSULTATS ─────────────────────────────────────────────────────────────────
if st.session_state.get("analyzed"):
    data = st.session_state.result
    tabs = st.tabs(["📊 Stratégie", "🎁 Offres", "🛍️ Shopify", "📣 Facebook Ads", "🎙️ Voix-Off"])

    with tabs[0]: # STRATÉGIE
        c1, c2 = st.columns([1, 2])
        with c1:
            score = data.get('score', 8)
            st.markdown(f"<div class='score-badge'>{score}/10</div>", unsafe_allow_html=True)
            # DIAGRAMME CIRCULAIRE Plotly
            fig = go.Figure(data=[go.Pie(values=[score, 10-score], hole=.7, marker_colors=['#D90429', '#1a1a2e'])])
            fig.update_layout(showlegend=False, height=220, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            st.subheader("💰 Rentabilité LABO")
            ca = target_sales * (pa + 10000)
            frais = target_sales * (pa + 2000 + 2000 + 1000) # Liv+Pub+Clos
            benef = ca - frais
            st.markdown(f"""
            <table class="gains-table">
                <tr><th>Ventes</th><th>CA</th><th>Coûts Global</th><th>Bénéfice Net</th></tr>
                <tr><td>{target_sales}/j</td><td>{ca:,} F</td><td>{frais:,} F</td><td style='color:#44dd88;'>+{benef:,} F</td></tr>
            </table>
            """, unsafe_allow_html=True)

    with tabs[2]: # SHOPIFY
        for i, p in enumerate(data['shopify']['paragraphes']):
            txt_copy = f"{p['titre']}\n{p['texte']}"
            st.markdown(f"""<div class="result-card">
                <button class="copy-btn" id="cp_{i}" onclick="copyToClipboard('{txt_copy}', 'cp_{i}')">📋 Copier</button>
                <p><b>{p['titre']}</b></p>
                <p>{p['texte']}</p>
            </div>""", unsafe_allow_html=True)

    with tabs[3]: # FACEBOOK ADS
        for i, ad in enumerate(data['ads']):
            st.markdown(f"**Variante {i+1}**")
            st.code(f"{ad['titre']}\n{ad['texte']}")

    with tabs[4]: # VOIX-OFF
        for i, s in enumerate(data['scripts']):
            st.markdown(f"**Argument Marketing {i+1}**")
            st.code(s['texte'])
