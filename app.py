import streamlit as st
import io, re, json, base64
from PIL import Image
from datetime import datetime

# Configuration de base
st.set_page_config(
    page_title="EcoMaster Labo Pro",
    page_icon="🚀",
    layout="wide",
)

# ── DESIGN CSS & JAVASCRIPT POUR LE COPIER ──────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; background-color: #0e1117 !important; color: #F0F0F0 !important; }
    .main { background-color: #0e1117 !important; }
    .block-container { padding-top: 1.5rem !important; max-width: 1100px !important; }
    section[data-testid="stSidebar"] { background-color: #0a0d12 !important; border-right: 1px solid #1e2530 !important; }

    .hero-banner {
        background: linear-gradient(135deg, #0e0000 0%, #1a0000 40%, #0e0000 100%);
        border: 1px solid #D90429; border-radius: 20px;
        padding: 2rem; margin-bottom: 1.5rem; text-align: center;
        box-shadow: 0 0 50px rgba(217,4,41,0.15);
    }
    .hero-banner h1 { font-size: clamp(1.6rem,5vw,2.6rem); font-weight: 900; color: #FFF; margin: 0; }
    .hero-banner h1 span { color: #D90429; }
    .hero-banner .slogan { color: #888; margin: 0.4rem 0 0; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; }

    /* CARD DESIGN */
    .result-card {
        background: #161b22; border: 1px solid #2a3140; border-radius: 14px;
        padding: 1.4rem; margin-bottom: 1rem; position: relative;
    }
    .card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.8rem; border-bottom: 1px solid #2a3140; padding-bottom: 0.5rem; }
    .card-title { color: #D90429; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }

    /* BOUTON COPIER DISCRET */
    .copy-btn {
        background: #1a1a2a; color: #888; border: 1px solid #2a3140;
        border-radius: 6px; padding: 4px 10px; font-size: 0.7rem;
        cursor: pointer; transition: all 0.2s; font-weight: 600;
    }
    .copy-btn:hover { border-color: #D90429; color: #FFF; background: #2a0010; }

    .price-box {
        background: linear-gradient(135deg,#0e0000,#1a0505); border:1px solid #D90429;
        border-radius:14px; padding:1.1rem; text-align:center;
    }
    .gains-table { width:100%; border-collapse:collapse; margin-top:0.5rem; font-size: 0.8rem; }
    .gains-table th { background:#D90429; color:white; padding:8px; }
    .gains-table td { background:#0e1117; color:#CCC; padding:9px; border-bottom:1px solid #1e2530; text-align:center; }

    /* SHOPIFY PARA */
    .para-card { background:#0e1117; border-left:4px solid #D90429; padding:1rem; margin-bottom:0.8rem; border-radius: 0 10px 10px 0; }
    .para-titre { color:#D90429; font-weight:800; font-size:0.95rem; margin-bottom:0.4rem; }
    .para-texte { color:#CCC; font-size:0.9rem; line-height:1.7; }
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
    btn.innerText = '✅ OK';
    setTimeout(() => { btn.innerText = '📋'; }, 2000);
}
</script>
""", unsafe_allow_html=True)

# ── FONCTIONS LOGIQUES ────────────────────────────────────────────────────────

def get_copy_button(text, uid):
    # On échappe les caractères spéciaux pour le JS
    clean_text = text.replace("'", "\\'").replace("\n", "\\n").replace("\r", "")
    return f'<button class="copy-btn" id="btn_{uid}" onclick="copyToClipboard(\'{clean_text}\', \'btn_{uid}\')">📋</button>'

def get_pub_recommendation(v):
    if v <= 10: return "5$ à 7$"
    elif v <= 20: return "7$ à 10$"
    else: return "15$ à 20$"

def save_to_history(name, score, data, price):
    if "history" not in st.session_state: st.session_state.history = []
    entry = {"name": name, "score": score, "data": data, "price": price, "ts": datetime.now().strftime("%H:%M")}
    # Éviter les doublons
    st.session_state.history = [entry] + [h for h in st.session_state.history if h["name"] != name][:6]

# ── SIDEBAR & HISTORIQUE ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#D90429;'>EcoMaster</h2>", unsafe_allow_html=True)
    st.write("🕒 **Historique de session**")
    if "history" in st.session_state and st.session_state.history:
        for i, h in enumerate(st.session_state.history):
            if st.button(f"📦 {h['name']} ({h['score']}/10)", key=f"hist_{i}"):
                st.session_state.result = h["data"]
                st.session_state.analyzed = True
                st.session_state.active_product = h["name"]
                st.session_state.active_price = h["price"]
                st.rerun()
    else:
        st.write("Aucune analyse.")
    
    st.markdown("---")
    st.info("💡 **Règle d'or LABO**\n- Livraison : 2000F\n- Pub : 2000F\n- Closing : 1000F\n- Marge : 3000-5000F")

# ── HERO & INPUTS ─────────────────────────────────────────────────────────────
st.markdown("""<div class="hero-banner"><h1>🚀 <span>EcoMaster</span> Labo Pro</h1>
<p class="slogan">Tout-en-un pour un e-commerce réussi créé par LABO</p></div>""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="large")
with col1:
    prod_name = st.text_input("📦 Nom du Produit", value=st.session_state.get("active_product", ""))
    base_price = st.number_input("💰 Prix d'Achat (FCFA)", min_value=0, value=st.session_state.get("active_price", 5000))
    target_sales = st.number_input("🎯 Objectif de ventes / jour", min_value=1, value=10)

with col2:
    files = st.file_uploader("📸 Photos du produit", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if files:
        cols = st.columns(len(files[:3]))
        for i, f in enumerate(files[:3]):
            cols[i].image(f, use_column_width=True)

# ── CALCULS PRIX ──────────────────────────────────────────────────────────────
p_min = base_price + 8000
p_max = base_price + 12000
st.markdown(f"### 💰 Stratégie : Vendre entre {p_min:,} et {p_max:,} FCFA")

# ── ANALYSE IA (GROQ) ────────────────────────────────────────────────────────
def build_elite_prompt(name, pa, pmin, pmax):
    return f"""Tu es un expert en neuro-marketing pour l'Afrique francophone.
PRODUIT : {name} | ACHAT : {pa} FCFA | VENTE : {pmin}-{pmax} FCFA.

CONTRAINTES STRICTES :
1. SHOPIFY : 3 Titres magnétiques + 6 Paragraphes de vente. 
   Chaque paragraphe = 1 Titre en gras + MAXIMUM 4 phrases de détails profonds (pas de listes, pas de lignes courtes). 
   Structure du texte comme l'exemple : 'Titre: Détail qui explique le bénéfice psychologique'.
2. FACEBOOK ADS : 3 Variantes obligatoires. 
   Chaque variante contient : un Titre Accrocheur (ex: PROMO FLASH, STOCK LIMITÉ) ET un texte publicitaire de MAXIMUM 5 lignes (émotionnel et fun).
3. VOIX-OFF : 3 Scripts de EXACTEMENT 170 mots chacun. Pas d'étiquettes (pas de 'Hook:', 'CTA:'). Texte fluide uniquement.
   - Si produit WOW : Hook Choc -> Problème rapide -> Solution Visuelle -> Preuve ('M. Kofi a testé') -> CTA.
   - Si Problème-Solution : Hook Douleur -> Frustration -> La Solution -> Témoignage ('Mme Aminata') -> CTA.

Réponds UNIQUEMENT en JSON :
{{
  "score": 9,
  "type": "wow",
  "justification": "...",
  "peurs": ["..."], "desirs": ["..."],
  "offres": [{{"titre":"...", "desc":"..."}}],
  "shopify": {{
      "titres": ["...", "...", "..."],
      "paras": [ {{"titre": "...", "texte": "..."}} ]
  }},
  "ads": [ {{"hook": "...", "body": "..."}} ],
  "scripts": [ {{"angle": "...", "texte": "..."}} ]
}}"""

if st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True):
    if not files:
        st.error("Ajoute au moins une photo !")
    else:
        from groq import Groq
        # Utilisation des secrets backstage
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        img_bytes = [f.read() for f in files[:3]]
        
        with st.spinner("Analyse Elite en cours..."):
            try:
                b64_imgs = [base64.b64encode(b).decode() for b in img_bytes]
                content = [{"type": "text", "text": build_elite_prompt(prod_name, base_price, p_min, p_max)}]
                for b in b64_imgs:
                    content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b}"}})
                
                res = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct", # Modèle 2026 stable
                    messages=[{"role": "user", "content": content}],
                    response_format={"type": "json_object"}
                )
                data = json.loads(res.choices[0].message.content)
                st.session_state.result = data
                st.session_state.analyzed = True
                save_to_history(prod_name, data["score"], data, base_price)
                st.rerun()
            except Exception as e:
                st.error(f"Erreur IA : {e}")

# ── AFFICHAGE DES RÉSULTATS ───────────────────────────────────────────────────
if st.session_state.get("analyzed"):
    data = st.session_state.result
    tabs = st.tabs(["📊 Stratégie", "🛍️ Shopify", "📣 Facebook Ads", "🎙️ Voix-Off", "🎁 Offres"])

    with tabs[0]: # STRATÉGIE & CALCULATEUR
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"<div class='price-box'>Score : {data['score']}/10<br><small>{'⚡ WOW' if data['type']=='wow' else '🎯 P-S'}</small></div>", unsafe_allow_html=True)
        with col_s2:
            st.write(data['justification'])
        
        # TABLEAU DE RENTABILITÉ DYNAMIQUE
        st.subheader("📊 Tableau de Rentabilité")
        ca = target_sales * ((p_min + p_max)/2)
        cout_achat = target_sales * base_price
        frais_fixes = target_sales * 5000 # 2k livraison + 2k pub + 1k closing
        benef = ca - cout_achat - frais_fixes
        
        st.markdown(f"""
        <table class="gains-table">
            <tr><th>Ventes</th><th>Budget Pub Recommandé</th><th>CA Estimé</th><th>Coûts Global</th><th>Bénéfice Net</th></tr>
            <tr>
                <td>{target_sales} / jour</td>
                <td><b style="color:#ff9944;">{get_pub_recommendation(target_sales)}</b></td>
                <td>{ca:,.0f} F</td>
                <td>{cout_achat + frais_fixes:,.0f} F</td>
                <td style="color:#44dd88; font-weight:bold;">+{benef:,.0f} F</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

    with tabs[1]: # SHOPIFY
        st.markdown("<h3 style='color:#D90429;'>🏷️ Titres Page Produit</h3>", unsafe_allow_html=True)
        for t in data['shopify']['titres']:
            col_t1, col_t2 = st.columns([0.9, 0.1])
            col_t1.write(f"**{t}**")
            col_t2.markdown(get_copy_button(t, t[:5]), unsafe_allow_html=True)
        
        st.markdown("<h3 style='color:#D90429;'>📝 Fiche de vente (6 Sections)</h3>", unsafe_allow_html=True)
        for i, p in enumerate(data['shopify']['paras']):
            st.markdown(f"""<div class="para-card">
                <div style="display:flex; justify-content:space-between;">
                    <div class="para-titre">{p['titre']}</div>
                    {get_copy_button(p['texte'], f'para_{i}')}
                </div>
                <div class="para-texte">{p['texte']}</div>
            </div>""", unsafe_allow_html=True)

    with tabs[2]: # FACEBOOK ADS
        st.subheader("📣 Ad Copies (Max 5 lignes)")
        for i, ad in enumerate(data['ads']):
            st.markdown(f"""<div class="result-card">
                <div class="card-header"><span class="card-title">Variante {i+1}</span>{get_copy_button(f"{ad['hook']}\\n{ad['body']}", f'ad_{i}')}</div>
                <div style="color:#ff9944; font-weight:bold; margin-bottom:5px;">{ad['hook']}</div>
                <div style="color:#ccc;">{ad['body']}</div>
            </div>""", unsafe_allow_html=True)

    with tabs[3]: # VOIX-OFF
        st.subheader("🎙️ Scripts (170 mots)")
        for i, s in enumerate(data['scripts']):
            st.markdown(f"""<div class="result-card">
                <div class="card-header"><span class="card-title">{s['angle']}</span>{get_copy_button(s['texte'], f'script_{i}')}</div>
                <div style="line-height:2; color:#eee;">{s['texte']}</div>
            </div>""", unsafe_allow_html=True)

    with tabs[4]: # OFFRES
        for i, o in enumerate(data['offres']):
            st.info(f"**{o['titre']}** : {o['desc']}")
