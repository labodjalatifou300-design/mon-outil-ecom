import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import re

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EcoMaster Labo Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS (Dark Mode + Red Accents) ───────────────────────────────────────
st.markdown("""
<style>
  /* ── Global reset ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0D0D0D;
    color: #F0F0F0;
  }

  /* ── Main container ── */
  .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
  }

  /* ── Header banner ── */
  .hero-banner {
    background: linear-gradient(135deg, #1a0000 0%, #2d0000 50%, #1a0000 100%);
    border: 1px solid #D90429;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
  }
  .hero-banner h1 {
    font-size: 2.2rem;
    font-weight: 900;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -0.5px;
  }
  .hero-banner h1 span { color: #D90429; }
  .hero-banner p {
    color: #999;
    margin: 0.5rem 0 0;
    font-size: 0.95rem;
  }

  /* ── Input cards ── */
  .input-card {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
  }

  /* ── Streamlit inputs ── */
  .stTextInput input, .stNumberInput input {
    background-color: #1E1E1E !important;
    color: #FFFFFF !important;
    border: 1px solid #3A3A3A !important;
    border-radius: 8px !important;
  }
  .stTextInput input:focus, .stNumberInput input:focus {
    border-color: #D90429 !important;
    box-shadow: 0 0 0 2px rgba(217,4,41,0.25) !important;
  }

  /* ── File uploader ── */
  [data-testid="stFileUploader"] {
    background: #1A1A1A !important;
    border: 2px dashed #3A3A3A !important;
    border-radius: 12px !important;
  }

  /* ── Primary button ── */
  .stButton > button {
    background: linear-gradient(135deg, #D90429, #a80220) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.2s ease !important;
    width: 100%;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(217,4,41,0.4) !important;
  }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #1A1A1A;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #2A2A2A;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #888 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
  }
  .stTabs [aria-selected="true"] {
    background: #D90429 !important;
    color: white !important;
  }

  /* ── Result cards ── */
  .result-card {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
  }
  .result-card h3 {
    color: #D90429;
    font-size: 1rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #2A2A2A;
  }

  /* ── Score badge ── */
  .score-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: 4px solid #D90429;
    font-size: 2rem;
    font-weight: 900;
    color: #FFFFFF;
    background: radial-gradient(circle, #2d0000, #0D0D0D);
    margin: 0 auto 1rem;
  }

  /* ── Price display ── */
  .price-box {
    background: linear-gradient(135deg, #1a0000, #2a0a0a);
    border: 1px solid #D90429;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
  }
  .price-box .label { color: #999; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
  .price-box .value { color: #FFFFFF; font-size: 1.6rem; font-weight: 900; }
  .price-box .currency { color: #D90429; font-size: 0.85rem; }

  /* ── Ad text block ── */
  .ad-block {
    background: #111;
    border-left: 3px solid #D90429;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    white-space: pre-wrap;
    font-size: 0.9rem;
    line-height: 1.7;
  }

  /* ── Script block ── */
  .script-block {
    background: #111;
    border: 1px solid #2A2A2A;
    border-radius: 10px;
    padding: 1.25rem;
    margin-bottom: 0.75rem;
  }
  .script-block .tag {
    display: inline-block;
    background: #D90429;
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  /* ── Metric strip ── */
  .metric-strip {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
  }
  .metric-item {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    flex: 1;
    min-width: 130px;
    text-align: center;
  }
  .metric-item .m-label { color: #666; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.8px; }
  .metric-item .m-value { color: #FFFFFF; font-size: 1.2rem; font-weight: 700; margin-top: 2px; }
  .metric-item .m-value.red { color: #D90429; }

  /* ── Spinner ── */
  .stSpinner > div { border-top-color: #D90429 !important; }

  /* ── Hide Streamlit branding ── */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #111; }
  ::-webkit-scrollbar-thumb { background: #D90429; border-radius: 3px; }

  /* ── Labels ── */
  label, .stTextInput label, .stNumberInput label, .stFileUploader label {
    color: #CCCCCC !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── HERO BANNER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <h1>🚀 <span>EcoMaster</span> Labo Pro</h1>
  <p>Transformez une photo en stratégie de vente complète — Propulsé par l'IA</p>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR — API KEY ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input("Clé API Google Gemini", type="password", placeholder="AIza...")
    st.markdown("---")
    st.markdown("**Comment obtenir une clé ?**")
    st.markdown("👉 [Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.markdown("---")
    st.caption("EcoMaster Labo Pro v1.0\ne-com Family Tool by Labo")

# ─── MAIN INPUTS ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    product_name = st.text_input("📦 Nom du Produit", placeholder="Ex: Sérum Vitamine C Anti-Tache")
    purchase_price = st.number_input("💰 Prix d'Achat (FCFA)", min_value=0, step=500, value=5000)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "📸 Photos du Produit (1 à 3)",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        cols = st.columns(len(uploaded_files))
        for i, f in enumerate(uploaded_files[:3]):
            with cols[i]:
                st.image(f, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── PRICE CALCULATOR ───────────────────────────────────────────────────────────
price_min = purchase_price + 8000
price_max = purchase_price + 12000
margin_min = 8000
margin_max = 12000

pcol1, pcol2, pcol3 = st.columns(3, gap="medium")
with pcol1:
    st.markdown(f"""
    <div class="price-box">
      <div class="label">Prix Vente Min</div>
      <div class="value">{price_min:,} <span class="currency">FCFA</span></div>
    </div>""", unsafe_allow_html=True)
with pcol2:
    st.markdown(f"""
    <div class="price-box">
      <div class="label">Prix Vente Max</div>
      <div class="value">{price_max:,} <span class="currency">FCFA</span></div>
    </div>""", unsafe_allow_html=True)
with pcol3:
    st.markdown(f"""
    <div class="price-box">
      <div class="label">Marge Bénéficiaire</div>
      <div class="value">{margin_min:,}–{margin_max:,} <span class="currency">FCFA</span></div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── ANALYZE BUTTON ─────────────────────────────────────────────────────────────
analyze_clicked = st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True)

# ─── AI ANALYSIS ────────────────────────────────────────────────────────────────
def build_prompt(name: str, price_achat: int, price_min: int, price_max: int) -> str:
    return f"""
Tu es un expert en neuro-marketing et e-commerce pour le marché africain (Afrique de l'Ouest, francophone).
Analyse le produit présenté sur les images.

PRODUIT : {name}
PRIX D'ACHAT : {price_achat} FCFA
FOURCHETTE DE VENTE RECOMMANDÉE : {price_min} – {price_max} FCFA

Génère une analyse COMPLÈTE et STRUCTURÉE en suivant EXACTEMENT ce format JSON (réponds uniquement avec le JSON, sans balises markdown) :

{{
  "score": <nombre de 1 à 10>,
  "score_justification": "<2-3 phrases expliquant le score>",
  "public_cible": "<description précise du client idéal>",
  "peurs": ["<peur 1>", "<peur 2>", "<peur 3>"],
  "desirs": ["<désir 1>", "<désir 2>", "<désir 3>"],
  "budget_pub_usd": "<fourchette ex: 4$–7$ / jour>",
  "shopify": {{
    "titre": "<Titre magnétique accrocheur>",
    "paragraphes": [
      "<§1 : Accroche émotionnelle — parle de la douleur du client>",
      "<§2 : Présentation du produit comme LA solution>",
      "<§3 : Bénéfices concrets et chiffrés si possible>",
      "<§4 : Preuve sociale / témoignage fictif crédible>",
      "<§5 : Urgence + appel à l'action fort>"
    ]
  }},
  "facebook_ads": [
    {{
      "titre": "<Titre choc 1>",
      "texte": "<Texte pub Facebook 1 avec emojis, 3-5 lignes>"
    }},
    {{
      "titre": "<Titre choc 2>",
      "texte": "<Texte pub Facebook 2 avec emojis, 3-5 lignes>"
    }},
    {{
      "titre": "<Titre choc 3>",
      "texte": "<Texte pub Facebook 3 avec emojis, 3-5 lignes>"
    }}
  ],
  "voix_off": {{
    "accroche": "<1-2 phrases d'accroche percutantes>",
    "probleme": "<Description du problème que le client vit>",
    "solution": "<Comment ce produit résout le problème>",
    "preuve": "<Preuve sociale ou statistique crédible>",
    "cta": "<Appel à l'action fort et urgent>"
  }}
}}
"""

def call_gemini(api_key: str, prompt: str, images: list) -> dict:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    parts = []
    for img_data in images:
        img = Image.open(io.BytesIO(img_data))
        parts.append(img)
    parts.append(prompt)
    
    response = model.generate_content(parts)
    raw = response.text.strip()
    
    # Clean potential markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    
    import json
    return json.loads(raw)

# ─── RESULTS DISPLAY ────────────────────────────────────────────────────────────
if analyze_clicked:
    if not api_key:
        st.error("⚠️ Veuillez entrer votre clé API Google Gemini dans le panneau latéral (⚙️).")
    elif not product_name.strip():
        st.error("⚠️ Veuillez entrer le nom du produit.")
    elif not uploaded_files:
        st.error("⚠️ Veuillez uploader au moins une photo du produit.")
    else:
        images_bytes = [f.read() for f in uploaded_files[:3]]
        prompt = build_prompt(product_name, purchase_price, price_min, price_max)

        with st.spinner("🧠 Analyse IA en cours... (10-20 secondes)"):
            try:
                data = call_gemini(api_key, prompt, images_bytes)
                st.session_state["result"] = data
                st.session_state["analyzed"] = True
            except Exception as e:
                st.error(f"❌ Erreur API : {e}")
                st.session_state["analyzed"] = False

# Render results if available
if st.session_state.get("analyzed") and "result" in st.session_state:
    data = st.session_state["result"]
    
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Stratégie & Chiffres",
        "🛍️ Boutique Shopify",
        "📣 Facebook Ads",
        "🎙️ Script Voix-Off"
    ])

    # ── TAB 1 : Stratégie & Chiffres ──────────────────────────────────────────
    with tab1:
        score = data.get("score", "?")
        justif = data.get("score_justification", "")
        public = data.get("public_cible", "")
        peurs = data.get("peurs", [])
        desirs = data.get("desirs", [])
        budget = data.get("budget_pub_usd", "4$–7$ / jour")

        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f"""
            <div style="text-align:center; padding:1rem;">
              <div class="score-badge">{score}/10</div>
              <p style="color:#999; font-size:0.85rem;">Score de Potentiel</p>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="result-card">
              <h3>💡 Verdict IA</h3>
              <p style="line-height:1.7; color:#DDDDDD;">{justif}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="metric-strip">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:flex; gap:0.75rem; flex-wrap:wrap; margin-bottom:1rem;">
          <div class="metric-item">
            <div class="m-label">Budget Pub / Jour</div>
            <div class="m-value red">{budget}</div>
          </div>
          <div class="metric-item">
            <div class="m-label">Marge Min</div>
            <div class="m-value">{margin_min:,} FCFA</div>
          </div>
          <div class="metric-item">
            <div class="m-label">Marge Max</div>
            <div class="m-value">{margin_max:,} FCFA</div>
          </div>
          <div class="metric-item">
            <div class="m-label">Fourchette Prix</div>
            <div class="m-value">{price_min:,}–{price_max:,}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_p, col_d = st.columns(2, gap="medium")
        with col_p:
            st.markdown('<div class="result-card"><h3>😰 Peurs du Client</h3>', unsafe_allow_html=True)
            for p in peurs:
                st.markdown(f"<p>🔴 {p}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_d:
            st.markdown('<div class="result-card"><h3>✨ Désirs du Client</h3>', unsafe_allow_html=True)
            for d in desirs:
                st.markdown(f"<p>💚 {d}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-card">
          <h3>🎯 Public Cible</h3>
          <p style="line-height:1.7; color:#DDDDDD;">{public}</p>
        </div>""", unsafe_allow_html=True)

    # ── TAB 2 : Shopify ───────────────────────────────────────────────────────
    with tab2:
        shopify = data.get("shopify", {})
        titre = shopify.get("titre", "")
        paragraphes = shopify.get("paragraphes", [])

        st.markdown(f"""
        <div class="result-card">
          <h3>🏷️ Titre Magnétique</h3>
          <p style="font-size:1.25rem; font-weight:700; color:#FFFFFF; line-height:1.5;">{titre}</p>
        </div>""", unsafe_allow_html=True)

        tags = ["🔥 Accroche", "💊 Solution", "✅ Bénéfices", "⭐ Preuve Sociale", "⏰ Urgence & CTA"]
        for i, para in enumerate(paragraphes):
            tag = tags[i] if i < len(tags) else f"§{i+1}"
            st.markdown(f"""
            <div class="result-card">
              <h3>{tag}</h3>
              <p style="line-height:1.8; color:#DDDDDD;">{para}</p>
            </div>""", unsafe_allow_html=True)

    # ── TAB 3 : Facebook Ads ──────────────────────────────────────────────────
    with tab3:
        ads = data.get("facebook_ads", [])
        for i, ad in enumerate(ads):
            titre_ad = ad.get("titre", f"Publicité {i+1}")
            texte_ad = ad.get("texte", "")
            st.markdown(f"""
            <div class="result-card">
              <h3>📣 Publicité {i+1}</h3>
              <p style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:0.5rem;">{titre_ad}</p>
              <div class="ad-block">{texte_ad}</div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 4 : Voix-Off ──────────────────────────────────────────────────────
    with tab4:
        vo = data.get("voix_off", {})
        sections = [
            ("🎯 ACCROCHE", vo.get("accroche", "")),
            ("😤 PROBLÈME", vo.get("probleme", "")),
            ("💡 SOLUTION", vo.get("solution", "")),
            ("🏆 PREUVE", vo.get("preuve", "")),
            ("📲 CALL TO ACTION", vo.get("cta", "")),
        ]
        for label, content in sections:
            st.markdown(f"""
            <div class="script-block">
              <div class="tag">{label}</div>
              <p style="line-height:1.8; color:#DDDDDD; margin:0;">{content}</p>
            </div>""", unsafe_allow_html=True)

        # Full script for copy
        full_script = "\n\n".join([f"[{l}]\n{c}" for l, c in sections])
        st.download_button(
            label="📥 Télécharger le Script Complet",
            data=full_script,
            file_name=f"script_voixoff_{product_name.replace(' ','_')}.txt",
            mime="text/plain",
        )
