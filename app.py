import streamlit as st
import io
import re
import json
from PIL import Image
import base64

st.set_page_config(
    page_title="EcoMaster Labo Pro",
    page_icon="🚀",
    layout="wide",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0D0D0D;
    color: #F0F0F0;
  }
  .block-container { padding-top: 2rem; max-width: 1100px; }
  .hero-banner {
    background: linear-gradient(135deg, #1a0000 0%, #2d0000 50%, #1a0000 100%);
    border: 1px solid #D90429; border-radius: 16px;
    padding: 2rem 2.5rem; margin-bottom: 2rem; text-align: center;
  }
  .hero-banner h1 { font-size: 2.2rem; font-weight: 900; color: #FFFFFF; margin: 0; }
  .hero-banner h1 span { color: #D90429; }
  .hero-banner p { color: #999; margin: 0.5rem 0 0; font-size: 0.95rem; }
  .stTextInput input, .stNumberInput input {
    background-color: #1E1E1E !important; color: #FFFFFF !important;
    border: 1px solid #3A3A3A !important; border-radius: 8px !important;
  }
  .stButton > button {
    background: linear-gradient(135deg, #D90429, #a80220) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: 1.05rem !important; padding: 0.65rem 2rem !important;
    width: 100%;
  }
  .stTabs [data-baseweb="tab-list"] {
    background: #1A1A1A; border-radius: 10px; padding: 4px; gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #888 !important;
    border-radius: 8px !important; font-weight: 600 !important;
  }
  .stTabs [aria-selected="true"] { background: #D90429 !important; color: white !important; }
  .result-card {
    background: #1A1A1A; border: 1px solid #2A2A2A;
    border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
  }
  .result-card h3 {
    color: #D90429; font-size: 1rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
    margin-bottom: 0.75rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid #2A2A2A;
  }
  .score-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 90px; height: 90px; border-radius: 50%;
    border: 4px solid #D90429; font-size: 2rem; font-weight: 900;
    color: #FFFFFF; background: radial-gradient(circle, #2d0000, #0D0D0D);
    margin: 0 auto 1rem;
  }
  .price-box {
    background: linear-gradient(135deg, #1a0000, #2a0a0a);
    border: 1px solid #D90429; border-radius: 12px;
    padding: 1.25rem; text-align: center; margin-bottom: 1rem;
  }
  .price-box .label { color: #999; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
  .price-box .value { color: #FFFFFF; font-size: 1.6rem; font-weight: 900; }
  .price-box .currency { color: #D90429; font-size: 0.85rem; }
  .ad-block {
    background: #111; border-left: 3px solid #D90429;
    border-radius: 0 8px 8px 0; padding: 1rem 1.25rem;
    margin-bottom: 0.75rem; white-space: pre-wrap;
    font-size: 0.9rem; line-height: 1.7;
  }
  .script-block {
    background: #111; border: 1px solid #2A2A2A;
    border-radius: 10px; padding: 1.25rem; margin-bottom: 0.75rem;
  }
  .script-tag {
    display: inline-block; background: #D90429; color: white;
    font-size: 0.7rem; font-weight: 700; padding: 2px 8px;
    border-radius: 4px; margin-bottom: 0.4rem;
    text-transform: uppercase; letter-spacing: 1px;
  }
  #MainMenu, footer, header { visibility: hidden; }
  label { color: #CCCCCC !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-banner">
  <h1>🚀 <span>EcoMaster</span> Labo Pro</h1>
  <p>Transformez une photo en stratégie de vente complète — Propulsé par l'IA</p>
</div>
""", unsafe_allow_html=True)

# CHOIX IA
st.markdown("""
<div style="background:#1A1A1A; border:2px solid #D90429; border-radius:12px; padding:1.25rem; margin-bottom:1.5rem;">
  <p style="color:#D90429; font-weight:700; margin:0 0 0.75rem;">🤖 Choisis ton moteur IA</p>
""", unsafe_allow_html=True)

ai_choice = st.radio(
    "Moteur",
    ["🟢 Groq — LLaMA 3 (100% Gratuit)", "🔵 OpenAI — GPT-4o (Payant)"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# CLÉ API selon choix
if "Groq" in ai_choice:
    st.markdown("""
    <div style="background:#001a00; border:2px solid #00aa44; border-radius:12px; padding:1rem 1.5rem; margin-bottom:1.5rem;">
      <p style="color:#00dd55; font-weight:700; margin:0 0 0.3rem;">🔑 Clé API Groq — GRATUITE</p>
      <p style="color:#999; font-size:0.8rem; margin:0;">
        1. Va sur <a href="https://console.groq.com" target="_blank" style="color:#00dd55;">console.groq.com</a><br>
        2. Crée un compte gratuit<br>
        3. Clique "API Keys" puis "Create API Key"<br>
        4. Copie et colle ta clé ici 👇
      </p>
    </div>
    """, unsafe_allow_html=True)
    api_key = st.text_input("🔑 Clé API Groq", type="password", placeholder="gsk_...")
else:
    st.markdown("""
    <div style="background:#001a2d; border:2px solid #0066cc; border-radius:12px; padding:1rem 1.5rem; margin-bottom:1.5rem;">
      <p style="color:#4da6ff; font-weight:700; margin:0 0 0.3rem;">🔑 Clé API OpenAI</p>
      <p style="color:#999; font-size:0.8rem; margin:0;">
        1. Va sur <a href="https://platform.openai.com/api-keys" target="_blank" style="color:#4da6ff;">platform.openai.com</a><br>
        2. Clique "Create new secret key"<br>
        3. Copie et colle ta clé ici 👇
      </p>
    </div>
    """, unsafe_allow_html=True)
    api_key = st.text_input("🔑 Clé API OpenAI", type="password", placeholder="sk-...")

# INPUTS
col1, col2 = st.columns([3, 2], gap="large")
with col1:
    product_name = st.text_input("📦 Nom du Produit", placeholder="Ex: Pince Multifonction")
    purchase_price = st.number_input("💰 Prix d'Achat (FCFA)", min_value=0, step=500, value=5000)
with col2:
    uploaded_files = st.file_uploader(
        "📸 Photos du Produit (1 à 3)",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        cols = st.columns(len(uploaded_files[:3]))
        for i, f in enumerate(uploaded_files[:3]):
            with cols[i]:
                st.image(f, use_column_width=True)

# PRIX
price_min = purchase_price + 8000
price_max = purchase_price + 12000
st.markdown("<br>", unsafe_allow_html=True)
pcol1, pcol2, pcol3 = st.columns(3, gap="medium")
with pcol1:
    st.markdown(f"""<div class="price-box">
      <div class="label">Prix Vente Min</div>
      <div class="value">{price_min:,} <span class="currency">FCFA</span></div>
    </div>""", unsafe_allow_html=True)
with pcol2:
    st.markdown(f"""<div class="price-box">
      <div class="label">Prix Vente Max</div>
      <div class="value">{price_max:,} <span class="currency">FCFA</span></div>
    </div>""", unsafe_allow_html=True)
with pcol3:
    st.markdown(f"""<div class="price-box">
      <div class="label">Marge Bénéficiaire</div>
      <div class="value">8 000–12 000 <span class="currency">FCFA</span></div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True)

# PROMPT
def build_prompt(name, prix_achat, prix_min, prix_max):
    return f"""Tu es un expert en neuro-marketing et e-commerce pour le marché africain francophone.
Analyse ce produit.

PRODUIT : {name}
PRIX D'ACHAT : {prix_achat} FCFA
FOURCHETTE DE VENTE : {prix_min} – {prix_max} FCFA

Réponds UNIQUEMENT avec un JSON valide, sans texte avant ni après, sans balises markdown :

{{
  "score": 8,
  "score_justification": "texte ici",
  "public_cible": "texte ici",
  "peurs": ["peur 1", "peur 2", "peur 3"],
  "desirs": ["desir 1", "desir 2", "desir 3"],
  "budget_pub_usd": "4$-7$ par jour",
  "shopify": {{
    "titre": "titre ici",
    "paragraphes": ["para 1", "para 2", "para 3", "para 4", "para 5"]
  }},
  "facebook_ads": [
    {{"titre": "titre 1", "texte": "texte pub 1"}},
    {{"titre": "titre 2", "texte": "texte pub 2"}},
    {{"titre": "titre 3", "texte": "texte pub 3"}}
  ],
  "voix_off": {{
    "accroche": "texte",
    "probleme": "texte",
    "solution": "texte",
    "preuve": "texte",
    "cta": "texte"
  }}
}}"""

# GROQ (texte seulement — pas de vision)
def call_groq(key, prompt, images):
    from groq import Groq
    client = Groq(api_key=key)

    # Encode images en base64 pour le prompt visuel
    image_descriptions = []
    for i, img_data in enumerate(images):
        b64 = base64.b64encode(img_data).decode("utf-8")
        image_descriptions.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
        })

    content = image_descriptions + [{"type": "text", "text": prompt}]

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": content}],
        max_tokens=2000,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

# OPENAI
def call_openai(key, prompt, images):
    from openai import OpenAI
    client = OpenAI(api_key=key)
    content = []
    for img_data in images:
        b64 = base64.b64encode(img_data).decode("utf-8")
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
        })
    content.append({"type": "text", "text": prompt})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        max_tokens=2000,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

# ANALYSE
if analyze_clicked:
    if not api_key:
        st.error("⚠️ Entre ta clé API en haut de la page !")
    elif not product_name.strip():
        st.error("⚠️ Entre le nom du produit.")
    elif not uploaded_files:
        st.error("⚠️ Upload au moins une photo.")
    else:
        images_bytes = [f.read() for f in uploaded_files[:3]]
        prompt = build_prompt(product_name, purchase_price, price_min, price_max)
        with st.spinner("🧠 Analyse IA en cours... patiente 15-20 secondes ⏳"):
            try:
                if "Groq" in ai_choice:
                    data = call_groq(api_key, prompt, images_bytes)
                else:
                    data = call_openai(api_key, prompt, images_bytes)
                st.session_state["result"] = data
                st.session_state["analyzed"] = True
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                st.session_state["analyzed"] = False

# RÉSULTATS
if st.session_state.get("analyzed") and "result" in st.session_state:
    data = st.session_state["result"]
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Stratégie & Chiffres",
        "🛍️ Boutique Shopify",
        "📣 Facebook Ads",
        "🎙️ Script Voix-Off"
    ])

    with tab1:
        score = data.get("score", "?")
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f"""<div style="text-align:center; padding:1rem;">
              <div class="score-badge">{score}/10</div>
              <p style="color:#999; font-size:0.85rem;">Score de Potentiel</p>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="result-card">
              <h3>💡 Verdict IA</h3>
              <p style="line-height:1.7;">{data.get("score_justification","")}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex; gap:0.75rem; flex-wrap:wrap; margin-bottom:1rem;">
          <div style="background:#1A1A1A; border:1px solid #2A2A2A; border-radius:10px; padding:0.75rem 1rem; flex:1; min-width:130px; text-align:center;">
            <div style="color:#666; font-size:0.72rem; text-transform:uppercase;">Budget Pub / Jour</div>
            <div style="color:#D90429; font-size:1.2rem; font-weight:700;">{data.get("budget_pub_usd","4$-7$")}</div>
          </div>
          <div style="background:#1A1A1A; border:1px solid #2A2A2A; border-radius:10px; padding:0.75rem 1rem; flex:1; min-width:130px; text-align:center;">
            <div style="color:#666; font-size:0.72rem; text-transform:uppercase;">Marge Min</div>
            <div style="color:#FFF; font-size:1.2rem; font-weight:700;">8 000 FCFA</div>
          </div>
          <div style="background:#1A1A1A; border:1px solid #2A2A2A; border-radius:10px; padding:0.75rem 1rem; flex:1; min-width:130px; text-align:center;">
            <div style="color:#666; font-size:0.72rem; text-transform:uppercase;">Marge Max</div>
            <div style="color:#FFF; font-size:1.2rem; font-weight:700;">12 000 FCFA</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_p, col_d = st.columns(2, gap="medium")
        with col_p:
            st.markdown('<div class="result-card"><h3>😰 Peurs du Client</h3>', unsafe_allow_html=True)
            for p in data.get("peurs", []):
                st.markdown(f"<p>🔴 {p}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_d:
            st.markdown('<div class="result-card"><h3>✨ Désirs du Client</h3>', unsafe_allow_html=True)
            for d in data.get("desirs", []):
                st.markdown(f"<p>💚 {d}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""<div class="result-card">
          <h3>🎯 Public Cible</h3>
          <p style="line-height:1.7;">{data.get("public_cible","")}</p>
        </div>""", unsafe_allow_html=True)

    with tab2:
        shopify = data.get("shopify", {})
        st.markdown(f"""<div class="result-card">
          <h3>🏷️ Titre Magnétique</h3>
          <p style="font-size:1.25rem; font-weight:700; color:#FFFFFF;">{shopify.get("titre","")}</p>
        </div>""", unsafe_allow_html=True)
        tags = ["🔥 Accroche", "💊 Solution", "✅ Bénéfices", "⭐ Preuve Sociale", "⏰ Urgence & CTA"]
        for i, para in enumerate(shopify.get("paragraphes", [])):
            tag = tags[i] if i < len(tags) else f"§{i+1}"
            st.markdown(f"""<div class="result-card">
              <h3>{tag}</h3>
              <p style="line-height:1.8;">{para}</p>
            </div>""", unsafe_allow_html=True)

    with tab3:
        for i, ad in enumerate(data.get("facebook_ads", [])):
            st.markdown(f"""<div class="result-card">
              <h3>📣 Publicité {i+1}</h3>
              <p style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:0.5rem;">{ad.get("titre","")}</p>
              <div class="ad-block">{ad.get("texte","")}</div>
            </div>""", unsafe_allow_html=True)

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
            st.markdown(f"""<div class="script-block">
              <div class="script-tag">{label}</div>
              <p style="line-height:1.8; color:#DDDDDD; margin:0;">{content}</p>
            </div>""", unsafe_allow_html=True)

        full_script = "\n\n".join([f"[{l}]\n{c}" for l, c in sections])
        st.download_button(
            label="📥 Télécharger le Script Complet",
            data=full_script,
            file_name=f"script_{product_name.replace(' ','_')}.txt",
            mime="text/plain",
        )
```

---

Et le nouveau `requirements.txt` :
```
streamlit>=1.35.0
groq>=0.9.0
openai>=1.30.0
Pillow>=10.0.0
