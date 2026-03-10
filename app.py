import streamlit as st
import io, re, json, base64
from PIL import Image
from datetime import datetime
import plotly.graph_objects as go

# ── CONFIGURATION & DESIGN ORIGINAL ──────────────────────────────────────────
st.set_page_config(page_title="EcoMaster Labo Pro", page_icon="🚀", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; background-color: #0e1117 !important; color: #F0F0F0 !important; }
  .main { background-color: #0e1117 !important; }
  section[data-testid="stSidebar"] { background-color: #0a0d12 !important; border-right: 1px solid #1e2530 !important; }

  .hero-banner {
    background: linear-gradient(135deg, #0e0000 0%, #1a0000 40%, #0e0000 100%);
    border: 1px solid #D90429; border-radius: 20px;
    padding: 2rem; margin-bottom: 1.5rem; text-align: center;
    box-shadow: 0 0 50px rgba(217,4,41,0.15);
    animation: fadeInDown 0.7s ease both;
  }
  .hero-banner h1 { font-size: clamp(1.6rem, 5vw, 2.6rem); font-weight: 900; color: #FFF; margin: 0; }
  .hero-banner h1 span { color: #D90429; }
  
  .stButton > button {
    background: linear-gradient(135deg, #D90429 0%, #a80220 50%, #D90429 100%) !important;
    background-size: 200% auto !important; color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 800 !important; font-size: 1rem !important;
    padding: 0.8rem 2rem !important; width: 100% !important; letter-spacing: 1px !important;
    transition: all 0.3s ease !important; animation: pulse 2.5s infinite;
  }
  @keyframes pulse { 0%,100% { box-shadow:0 0 0 0 rgba(217,4,41,0.4); } 50% { box-shadow:0 0 0 14px rgba(217,4,41,0); } }
  
  .result-card { background: #161b22; border: 1px solid #2a3140; border-radius: 14px; padding: 1.4rem; margin-bottom: 1rem; }
  .score-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 100px; height: 100px; border-radius: 50%;
    border: 4px solid #D90429; font-size: 2.2rem; font-weight: 900;
    color: #FFF; background: radial-gradient(circle,#2d0000,#0e1117);
    margin: 0 auto 0.75rem; animation: glow 2.5s infinite;
  }
  @keyframes glow { 0%,100% { box-shadow:0 0 20px rgba(217,4,41,0.25); } 50% { box-shadow:0 0 45px rgba(217,4,41,0.65); } }

  /* STYLE POUR LES BOUTONS COPIER DISCRETS */
  .stCodeBlock { border: 1px solid #2a3140 !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── LOGIQUE CALCULATEUR & BUDGETS ─────────────────────────────────────────────
def get_pub_advice(v):
    if v <= 10: return "5$ – 7$"
    elif v <= 20: return "7$ – 10$"
    return "15$ – 20$+"

# ── INTERFACE ────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero-banner"><h1>🚀 <span>EcoMaster</span> Labo Pro</h1>
<p style="color:#888;">Tout-en-un pour un e-commerce réussi créé par LABO</p></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.write("🕒 **Historique Interactif**")
    if "history" not in st.session_state: st.session_state.history = []
    for h in st.session_state.history:
        if st.button(f"📦 {h['name']}"):
            st.session_state.result = h["data"]
            st.rerun()

col1, col2 = st.columns([3, 2])
with col1:
    prod_name = st.text_input("📦 Nom du Produit")
    price_buy = st.number_input("💰 Prix d'Achat (FCFA)", value=5000)
    sales_target = st.number_input("🎯 Objectif de ventes / jour", value=10)
with col2:
    uploaded = st.file_uploader("📸 Photo du produit", accept_multiple_files=True)

# ── ANALYSE IA (AVEC TES RÈGLES DE RÉDACTION) ──────────────────────────────
if st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True):
    from groq import Groq
    try:
        # Utilisation de la clé API en BACKSTAGE (Secrets)
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        prompt = f"""Expert Neuro-marketing Afrique. Produit: {prod_name}.
        1. SHOPIFY: 3 titres + 6 paragraphes. Chaque paragraphe = 1 Titre gras + MAX 4 phrases de détails profonds (Style exemple Lampes: Titre puis explication).
        2. ADS: 3 variantes. Titre accrocheur (Promo, Stock...) + Texte émotionnel fun MAX 5 lignes.
        3. VOIX-OFF: 3 scripts de MAX 130 mots. Titres: Argument Marketing 1, 2, 3. Style naturel ('M. Kofi a validé...').
        4. OFFRES: 3 offres psychologiques locales.
        Réponds uniquement en JSON."""
        
        # [Ici le code pour envoyer l'image et recevoir le JSON...]
        # st.session_state.result = data_ia
        # st.session_state.analyzed = True
    except Exception as e:
        st.error(f"Erreur : {e}")

# ── AFFICHAGE ÉLITE (STRATÉGIE & COPIER) ─────────────────────────────────────
if st.session_state.get("analyzed"):
    data = st.session_state.result
    tabs = st.tabs(["📊 Stratégie", "🎁 Offres", "🛍️ Shopify", "📣 Facebook Ads", "🎙️ Voix-Off"])

    with tabs[0]: # STRATÉGIE AVEC DONUT CHART RESTAURÉ
        s_col1, s_col2 = st.columns([1, 2])
        with s_col1:
            score = data['score']
            st.markdown(f"<div class='score-badge'>{score}/10</div>", unsafe_allow_html=True)
            fig = go.Figure(data=[go.Pie(values=[score, 10-score], hole=.7, marker_colors=['#D90429', '#1a1a2e'])])
            fig.update_layout(showlegend=False, height=200, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with s_col2:
            st.subheader("💰 Rentabilité Prévue")
            # Ta formule : 2k liv + 2k pub + 1k closing = 5k frais fixes
            frais_fixes = 5000 
            ca = sales_target * (price_buy + 10000)
            depenses = sales_target * (price_buy + frais_fixes)
            benefice = ca - depenses
            
            st.markdown(f"""
            <table class='gains-table'>
                <tr><th>Ventes</th><th>Budget Pub</th><th>Chiffre d'Affaires</th><th>Bénéfice Net</th></tr>
                <tr><td>{sales_target}/j</td><td>{get_pub_advice(sales_target)}</td><td>{ca:,} F</td><td style='color:#44dd88;'>+{benefice:,} F</td></tr>
            </table>
            """, unsafe_allow_html=True)

    with tabs[2]: # SHOPIFY AVEC BOUTON COPIER NATIF
        st.subheader("🛍️ Page Shopify")
        for i, p in enumerate(data['shopify']['paragraphes']):
            st.markdown(f"**{p['titre']}**")
            # Utilisation de st.code pour avoir un bouton copier DISCRET et FIABLE
            st.code(p['texte'], language=None)

    with tabs[3]: # FACEBOOK ADS
        st.subheader("📣 Ad Copies (Max 5 lignes)")
        for i, ad in enumerate(data['ads']):
            st.write(f"**Variante {i+1}**")
            st.code(f"{ad['titre']}\n\n{ad['texte']}", language=None)

    with tabs[4]: # VOIX-OFF (130 MOTS)
        st.subheader("🎙️ Scripts Arguments Marketing")
        for i, s in enumerate(data['scripts']):
            st.write(f"**Argument Marketing {i+1}**")
            st.code(s['texte'], language=None)
