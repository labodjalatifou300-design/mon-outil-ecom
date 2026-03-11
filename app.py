import streamlit as st
import requests
import json
import os
import base64
import re
import io
import urllib.parse
from PIL import Image

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Master Labo Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CSS GLOBAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;600&display=swap');

:root {
  --bg:     #0d0d14;
  --card:   #13131e;
  --panel:  #1a1a28;
  --red:    #e63946;
  --orange: #f4a261;
  --accent: #ff6b35;
  --white:  #f0f0f0;
  --gray:   #888;
}
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif !important;
  background: var(--bg) !important;
  color: var(--white) !important;
}
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }

/* HERO */
.hero {
  text-align: center; padding: 2rem 1rem 1.5rem;
  background: linear-gradient(160deg, #0d0d14 0%, #1a0a12 50%, #0d0d14 100%);
  border-bottom: 2px solid var(--red);
  position: relative; overflow: hidden; margin-bottom: 1.5rem;
}
.hero::before {
  content:''; position:absolute; inset:0;
  background: radial-gradient(ellipse at 50% -20%, rgba(230,57,70,.25) 0%, transparent 65%);
  animation: pulse 4s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:.5} 50%{opacity:1} }
.hero-title {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(1.6rem, 5vw, 3.5rem); font-weight: 900;
  background: linear-gradient(90deg, var(--red), var(--orange), #fff, var(--orange), var(--red));
  background-size: 300% 100%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  animation: shimmer 4s linear infinite; letter-spacing: 2px;
  position: relative; z-index: 1;
}
@keyframes shimmer { 0%{background-position:300% 0} 100%{background-position:0 0} }
.hero-sub {
  font-family: 'Rajdhani', sans-serif;
  font-size: clamp(.9rem, 2vw, 1.2rem); color: var(--orange);
  letter-spacing: 4px; text-transform: uppercase; margin-top: .4rem;
  position: relative; z-index: 1;
}
.pt { position:absolute; width:3px; height:3px; border-radius:50%; animation: floatup linear infinite; }
@keyframes floatup {
  0%{transform:translateY(120%) translateX(0);opacity:0}
  10%{opacity:1} 90%{opacity:1}
  100%{transform:translateY(-150%) translateX(20px);opacity:0}
}

/* FORM */
.form-wrap {
  background: var(--card); border: 1px solid rgba(230,57,70,.3);
  border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; position: relative;
}
.form-wrap::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(90deg, transparent, var(--red), var(--orange), transparent);
}

/* CARDS */
.card {
  background: var(--card); border: 1px solid rgba(230,57,70,.2);
  border-radius: 14px; padding: 1.4rem; margin-bottom: 1rem;
  position: relative; overflow: hidden; transition: border-color .3s, box-shadow .3s;
}
.card:hover { border-color: var(--red); box-shadow: 0 0 20px rgba(230,57,70,.3); }
.card::before {
  content:''; position:absolute; top:0; left:-100%; right:0; height:1px;
  background: linear-gradient(90deg, transparent, var(--orange), transparent);
  animation: scan 4s linear infinite;
}
@keyframes scan { to { left:100%; } }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
  gap: 3px !important; background: var(--panel) !important;
  border-radius: 12px !important; padding: 4px !important; flex-wrap: wrap !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: var(--gray) !important;
  border-radius: 8px !important; padding: .45rem .9rem !important;
  font-family: 'Rajdhani', sans-serif !important; font-weight: 700 !important;
  font-size: .85rem !important; white-space: nowrap !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--red), var(--accent)) !important;
  color: white !important; box-shadow: 0 0 15px rgba(230,57,70,.5) !important;
}

/* BUTTONS */
.stButton > button {
  background: linear-gradient(135deg, var(--red), var(--accent)) !important;
  color: white !important; border: none !important; border-radius: 10px !important;
  font-family: 'Rajdhani', sans-serif !important; font-weight: 700 !important;
  font-size: 1rem !important; letter-spacing: 1px !important; transition: all .3s !important;
  box-shadow: 0 0 15px rgba(230,57,70,.4) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 0 30px rgba(230,57,70,.7) !important; }

/* INPUTS */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
  background: var(--panel) !important; border: 1px solid rgba(230,57,70,.3) !important;
  border-radius: 8px !important; color: var(--white) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--orange) !important; box-shadow: 0 0 10px rgba(244,162,97,.3) !important;
}

/* METRIC BOX */
.mbox {
  background: var(--panel); border: 1px solid rgba(230,57,70,.25);
  border-radius: 12px; padding: .9rem; text-align: center; transition: all .3s;
}
.mbox:hover { border-color:var(--orange); transform:translateY(-2px); box-shadow:0 0 15px rgba(244,162,97,.3); }
.mval {
  font-family: 'Orbitron', sans-serif; font-size: 1.3rem; font-weight: 700;
  background: linear-gradient(135deg, var(--red), var(--orange));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.mlbl { font-size:.7rem; color:var(--gray); letter-spacing:2px; text-transform:uppercase; margin-top:.2rem; }

/* TABLE */
.gtable { width:100%; border-collapse:collapse; font-size:.85rem; }
.gtable th {
  background: linear-gradient(135deg, rgba(230,57,70,.35), rgba(244,162,97,.25));
  padding:.7rem .5rem; text-align:center;
  font-family:'Rajdhani',sans-serif; font-weight:700; letter-spacing:1px;
  border:1px solid rgba(230,57,70,.25);
}
.gtable td { padding:.6rem .5rem; text-align:center; border:1px solid rgba(255,255,255,.06); }
.gtable tr:hover td { background:rgba(230,57,70,.07); }
.gtable tr:nth-child(even) td { background:rgba(255,255,255,.02); }
.tg{color:#4ade80;font-weight:700} .tr{color:var(--red);font-weight:700} .to{color:var(--orange);font-weight:600}

/* TEXT BLOCK + COPY */
.tblock {
  background:var(--panel); border:1px solid rgba(255,255,255,.08);
  border-radius:10px; padding:1rem; line-height:1.75; font-size:.92rem; margin:.4rem 0;
}
.cpbtn {
  display:inline-block;
  background:linear-gradient(135deg,rgba(230,57,70,.25),rgba(255,107,53,.2));
  border:1px solid var(--red); color:white; padding:.3rem .8rem; border-radius:8px;
  cursor:pointer; font-size:.75rem; transition:all .2s; margin-top:.3rem; margin-bottom:.8rem;
}
.cpbtn:hover { background:var(--red); box-shadow:0 0 15px rgba(230,57,70,.5); }

/* SCORE BARS */
.sbar-wrap{margin:.35rem 0}
.sbar-row{display:flex;justify-content:space-between;margin-bottom:.15rem;font-size:.88rem}
.sbar-bg{background:#1a1a2e;border-radius:20px;height:9px;overflow:hidden}
.sbar-fill{height:100%;border-radius:20px;transition:width 1.2s ease}

/* OFFER CARD */
.ocard {
  background:linear-gradient(135deg,rgba(230,57,70,.08),rgba(244,162,97,.05));
  border:1px solid rgba(244,162,97,.3); border-radius:12px; padding:1.1rem; margin:.5rem 0; transition:all .3s;
}
.ocard:hover{border-color:var(--orange);box-shadow:0 0 15px rgba(244,162,97,.25);transform:translateX(4px)}

/* AVATAR */
.av-sec{border-left:3px solid var(--red);padding-left:.8rem;margin:.6rem 0}
.av-lbl{font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--orange);font-size:.78rem;letter-spacing:2px;text-transform:uppercase}

/* PLATFORM LINK */
.plink {
  display:block;text-decoration:none;background:var(--panel);
  border:1px solid rgba(230,57,70,.25); border-radius:10px; padding:.8rem 1rem;
  text-align:center; transition:all .25s; margin:.3rem 0;
}
.plink:hover{border-color:var(--orange);box-shadow:0 0 12px rgba(244,162,97,.3);transform:translateY(-2px)}

/* DIVIDER */
.ndiv {
  height:1px; margin:1.5rem 0;
  background:linear-gradient(90deg,transparent,var(--red),var(--orange),var(--red),transparent);
  animation:shimmer 3s linear infinite; background-size:200% 100%;
}

/* NEON LABEL */
.nlbl {
  font-family:'Orbitron',sans-serif; font-size:.8rem; font-weight:700;
  color:var(--red); letter-spacing:2px; text-transform:uppercase; margin-bottom:.5rem;
}
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--red);border-radius:3px}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
defaults = {
    "generated": False, "product_name": "",
    "product_images": [], "cost_price": 0,
    "daily_target": 5, "results": {}, "form_open": True,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  GROQ API KEY — depuis Streamlit Secrets
# ─────────────────────────────────────────────
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def call_groq(prompt: str, system: str = "", max_tokens: int = 3000) -> str:
    if not GROQ_API_KEY:
        return "❌ Clé API Groq manquante. Ajoutez GROQ_API_KEY dans Streamlit Secrets."
    headers = {"Content-Type":"application/json","Authorization":f"Bearer {GROQ_API_KEY}"}
    messages = []
    if system:
        messages.append({"role":"system","content":system})
    messages.append({"role":"user","content":prompt})
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={"model":"llama-3.3-70b-versatile","messages":messages,"max_tokens":max_tokens,"temperature":0.85},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Erreur Groq : {e}"

def parse_json(raw: str) -> dict:
    try:
        return json.loads(re.sub(r"```json|```","",raw).strip())
    except:
        return {}

def copy_block(text: str, uid: str):
    safe = text.replace("\\","\\\\").replace("`","\\`").replace("'","\\'")
    display = text.replace("\n","<br>")
    st.markdown(f"""
    <div class="tblock" id="tb_{uid}">{display}</div>
    <button class="cpbtn"
      onclick="navigator.clipboard.writeText(`{safe}`);
               this.innerText='✅ Copié !';setTimeout(()=>this.innerText='📋 Copier',2000);">
      📋 Copier
    </button>""", unsafe_allow_html=True)

def calc(cost, pub=5000, closing=1000, livraison=2000):
    rec = cost + 10000
    return {"sell_min":cost+8000,"sell_max":cost+12000,"sell_rec":rec,
            "profit":rec-cost-pub-closing-livraison,"pub":pub,"closing":closing,"livraison":livraison}

PAYS = ["Togo","Mali","Bénin","Guinée","Côte d'Ivoire","Congo"]
PAYS_CODES = {"Togo":"TG","Mali":"ML","Bénin":"BJ","Guinée":"GN","Côte d'Ivoire":"CI","Congo":"CG"}

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="pt" style="left:8%;animation-duration:7s;background:#e63946;"></div>
  <div class="pt" style="left:22%;animation-duration:9s;animation-delay:1s;background:#f4a261;"></div>
  <div class="pt" style="left:50%;animation-duration:6s;animation-delay:2s;background:#e63946;"></div>
  <div class="pt" style="left:78%;animation-duration:8s;animation-delay:.5s;background:#f4a261;"></div>
  <div class="pt" style="left:92%;animation-duration:10s;animation-delay:1.5s;background:#ff6b35;"></div>
  <div class="hero-title">⚡ E-Commerce Master Labo Pro</div>
  <div class="hero-sub">🌍 Tout en un pour un e-commerce africain réussi</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FORMULAIRE REPLIABLE
# ─────────────────────────────────────────────
btn_lbl = "🔼 Masquer le formulaire" if st.session_state.form_open else "🔽 Ouvrir le formulaire produit"
if st.button(btn_lbl, key="toggle_form"):
    st.session_state.form_open = not st.session_state.form_open
    st.rerun()

if st.session_state.form_open:
    st.markdown('<div class="form-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="nlbl">📦 Informations produit</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        product_name = st.text_input("🏷️ Nom du produit", placeholder="Ex: Sérum anti-acné naturel",
                                      value=st.session_state.product_name)
    with c2:
        cost_price = st.number_input("💵 Prix d'achat (FCFA)", min_value=0, step=500,
                                      value=int(st.session_state.cost_price))
    with c3:
        daily_target = st.number_input("🎯 Ventes/jour objectif", min_value=1, max_value=50,
                                        value=int(st.session_state.daily_target))

    c4, c5, c6 = st.columns(3)
    with c4:
        pub_budget = st.number_input("📣 Pub/vente (FCFA)", value=5000, step=500)
    with c5:
        closing_cost = st.number_input("📞 Closing/vente (FCFA)", value=1000, step=100)
    with c6:
        livraison_cost = st.number_input("🚚 Livraison/vente (FCFA)", value=2000, step=500)

    st.markdown("**🖼️ Images du produit** (1 à 10 images)")
    uploaded = st.file_uploader("", type=["jpg","jpeg","png","webp"],
                                  accept_multiple_files=True, label_visibility="collapsed")
    if uploaded:
        if len(uploaded) > 10:
            st.warning("⚠️ Maximum 10 images !")
            uploaded = uploaded[:10]
        st.session_state.product_images = uploaded
        img_cols = st.columns(min(len(uploaded),5))
        for i, img in enumerate(uploaded):
            with img_cols[i % 5]:
                st.image(img, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    launch = st.button("🚀 LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── LANCEMENT ANALYSE ──
    if launch:
        if not product_name:
            st.error("❌ Entrez le nom du produit !")
        elif cost_price == 0:
            st.error("❌ Entrez le prix d'achat !")
        elif not GROQ_API_KEY:
            st.error("❌ Clé API Groq manquante ! Ajoutez GROQ_API_KEY dans Streamlit → Settings → Secrets")
        else:
            st.session_state.product_name  = product_name
            st.session_state.cost_price    = cost_price
            st.session_state.daily_target  = daily_target
            pricing = calc(cost_price, pub_budget, closing_cost, livraison_cost)
            st.session_state.results["pricing"] = pricing

            SYS = f"""Tu es un expert en e-commerce africain et neuromarketing.
Produit : {product_name} | Prix achat : {cost_price} FCFA | Prix vente : {pricing['sell_rec']} FCFA
Objectif : {daily_target} ventes/jour | Marge nette : {pricing['profit']} FCFA
Réponds toujours en français, adapté au marché africain francophone."""

            bar = st.progress(0, "⚙️ Analyse en cours...")

            # SCORE
            bar.progress(10, "🎯 Score produit...")
            raw = call_groq(f"""Score STRICT /10 pour ce produit sur le marché africain.
Produit: {product_name} | Achat: {cost_price} FCFA | Vente: {pricing['sell_rec']} FCFA
12 critères: rentabilité, demande Afrique, concurrence, approvisionnement, créatives dispo,
viral Facebook/TikTok, problème réel résolu, simplicité, prix psychologique (SMIC 35k-200k FCFA),
fidélisation, risque retours, saisonnalité.
JSON UNIQUEMENT:
{{"score":7.5,"verdict":"Bon","emoji":"👍","note_rentabilite":8,"note_demande":7,"note_concurrence":6,
"note_creatives":7,"note_viral":7,"note_afrique":8,"note_prix":7,"note_fidelisation":6,
"points_forts":["point1","point2","point3"],"points_faibles":["point1","point2"],
"recommandation":"conseil 2-3 phrases","marches":["Côte d'Ivoire","Sénégal"],"periode":"Toute l'année"}}""", SYS, 1000)
            st.session_state.results["score"] = parse_json(raw) or {
                "score":7,"verdict":"Bon","emoji":"👍","note_rentabilite":7,"note_demande":7,
                "note_concurrence":6,"note_creatives":7,"note_viral":7,"note_afrique":8,
                "note_prix":7,"note_fidelisation":6,"points_forts":["Bonne marge"],
                "points_faibles":["Concurrence présente"],"recommandation":"Tester avec 5$/jour.",
                "marches":["Côte d'Ivoire"],"periode":"Toute l'année"}

            # OFFRES
            bar.progress(22, "🎁 Offres marketing...")
            raw = call_groq(f"""5 offres marketing irrésistibles pour "{product_name}" à {pricing['sell_rec']} FCFA en Afrique.
JSON: {{"offres":[{{"titre":"...","desc":"...","emoji":"...","impact":"Élevé","conseil":"..."}}]}}""", SYS, 700)
            st.session_state.results["offres"] = parse_json(raw) or {"offres":[{"titre":"Livraison gratuite","desc":"Levez les freins à l'achat","emoji":"🚚","impact":"Élevé","conseil":"Incluez le coût dans le prix de vente"}]}

            # SHOPIFY
            bar.progress(38, "🛍️ Description Shopify...")
            raw = call_groq(f"""Pour "{product_name}" sur Shopify en Afrique:
A) 3 titres SEO axés bénéfices (pas caractéristiques)
B) 6 paragraphes max 4 phrases chacun, titres PERCUTANTS et spécifiques (ex: "Résultats en 7 jours")
JSON: {{"titres":["t1","t2","t3"],"paragraphes":[{{"titre":"...","contenu":"..."}}]}}""", SYS, 1800)
            st.session_state.results["shopify"] = parse_json(raw) or {"titres":["Titre 1","Titre 2","Titre 3"],"paragraphes":[{"titre":"Titre","contenu":"Contenu"}]}

            # FACEBOOK ADS
            bar.progress(52, "📢 Facebook Ads...")
            raw = call_groq(f"""3 textes pub Facebook pour "{product_name}" marché africain francophone.
Max 70 mots. Structure: titre CHOC puis 3 tirets bénéfices.
JSON: {{"ads":[{{"accroche":"titre choc","b1":"bénéfice1","b2":"bénéfice2","b3":"bénéfice3","mots":45}}]}}""", SYS, 700)
            st.session_state.results["facebook"] = parse_json(raw) or {"ads":[{"accroche":"Titre choc","b1":"Bénéfice 1","b2":"Bénéfice 2","b3":"Bénéfice 3","mots":30}]}

            # VOIX OFF
            bar.progress(65, "🎙️ Scripts voix off...")
            raw = call_groq(f"""3 scripts voix off pour "{product_name}" (marché africain francophone).
RÈGLE ABSOLUE: chaque script = EXACTEMENT 120 à 140 mots. Compte précisément.
Structure: 1-PROBLÈME (2-3 phrases percutantes) 2-SOLUTION (2-3 phrases) 3-FONCTIONNEMENT (2-3 phrases) 4-TÉMOIGNAGE (prénom africain: Aminata, Kofi, Fatou, Ibrahim, Moussa...)
Neuromarketing: déclenche émotions, crée urgence.
JSON: {{"scripts":[{{"script":"texte 120-140 mots...","mots":125}},{{"script":"texte 120-140 mots...","mots":132}},{{"script":"texte 120-140 mots...","mots":128}}]}}""", SYS, 2500)
            st.session_state.results["voix"] = parse_json(raw) or {"scripts":[{"script":"Script voix off...","mots":125}]}

            # AVATAR
            bar.progress(80, "👤 Avatar client...")
            raw = call_groq(f"""Avatar client idéal pour "{product_name}" en Afrique francophone. Sois TRÈS précis.
JSON: {{"avatar":{{"sexe":"Femme","age":"28-42 ans","situation":"Mariée, 2 enfants","revenus":"80 000 - 150 000 FCFA/mois","profession":"Commerçante / Fonctionnaire","ville":"Grandes villes (Abidjan, Dakar, Douala)","reseaux":["Facebook","WhatsApp","TikTok"],"heure":"19h-22h","peurs":["p1","p2","p3"],"frustrations":["f1","f2","f3"],"desirs":["d1","d2","d3"],"motivations":["m1","m2"],"phrase":"phrase déclenchante parfaite","objections":["o1","o2"],"reponses":["r1","r2"],"pour_qui":"Elle-même ou ses proches","budget":"10 000 - 15 000 FCFA","livraison":"Domicile"}}}}""", SYS, 1400)
            st.session_state.results["avatar"] = parse_json(raw) or {"avatar":{"sexe":"Femme","age":"25-40 ans","revenus":"75 000 - 150 000 FCFA/mois","peurs":["peur1"],"frustrations":["frustration1"],"desirs":["désir1"],"phrase":"Phrase clé...","objections":["Objection 1"],"reponses":["Réponse 1"],"budget":"15 000 FCFA"}}

            bar.progress(100, "✅ Analyse terminée !")
            st.session_state.generated = True
            st.session_state.form_open = False
            st.balloons()
            st.rerun()

# ─────────────────────────────────────────────
#  ONGLETS RÉSULTATS
# ─────────────────────────────────────────────
if st.session_state.generated:
    R  = st.session_state.results
    PN = st.session_state.product_name
    PR = R.get("pricing", {})

    tabs = st.tabs(["💰 Prix & Gains","🎯 Score","🎁 Offres","🛍️ Shopify",
                    "📢 Facebook Ads","🎙️ Voix Off","👤 Avatar","🖼️ Images","🎬 Vidéos","⚔️ Concurrence"])

    # ─── TAB 1 : PRIX & GAINS ────────────────
    with tabs[0]:
        sell = PR.get("sell_rec",0); profit = PR.get("profit",0)
        pub  = PR.get("pub",5000);   closing = PR.get("closing",1000)
        liv  = PR.get("livraison",2000); cost = st.session_state.cost_price
        target = st.session_state.daily_target

        st.markdown(f'<div class="nlbl">💰 Stratégie de prix — {PN}</div>', unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        for col,lbl,val,sub in zip([c1,c2,c3,c4],
            ["Prix Min","Prix Recommandé","Prix Max","Bénéfice Net/vente"],
            [PR.get("sell_min",0),sell,PR.get("sell_max",0),profit],
            ["Marge minimale","✅ Optimal","Marge maximale","Après toutes charges"]):
            with col:
                st.markdown(f'<div class="mbox"><div class="mval">{val:,} FCFA</div><div class="mlbl">{lbl}</div><div style="font-size:.7rem;color:#555;margin-top:.2rem;">{sub}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="ndiv"></div>', unsafe_allow_html=True)
        st.markdown("#### 📊 Charges par vente")
        d1,d2,d3,d4 = st.columns(4)
        for col,lbl,val,clr in zip([d1,d2,d3,d4],
            ["📣 Publicité","📞 Closing","🚚 Livraison","💚 Bénéfice NET"],
            [pub,closing,liv,profit],["#e63946","#f4a261","#4ade80","#a78bfa"]):
            with col:
                st.markdown(f'<div class="mbox"><div style="font-family:Orbitron,sans-serif;font-size:1.2rem;font-weight:700;color:{clr};">{val:,} FCFA</div><div class="mlbl">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="ndiv"></div>', unsafe_allow_html=True)
        st.markdown("#### 📈 Tableau de gains — 1 à 10 ventes/jour")
        rows = ""
        for v in range(1,11):
            ca=v*sell; cp=v*cost; dp=v*pub; dc=v*closing; dl=v*liv
            bn=ca-cp-dp-dc-dl; bm=bn*30
            cl="tg" if bn>0 else "tr"
            rows += f"<tr><td><b>{v}</b></td><td class='to'>{ca:,}</td><td class='tr'>{cp:,}</td><td class='tr'>{dp:,}</td><td class='tr'>{dc:,}</td><td class='tr'>{dl:,}</td><td class='{cl}'>{bn:,}</td><td class='{cl}'>{bm:,}</td></tr>"
        st.markdown(f"""<div class="card"><table class="gtable">
          <thead><tr><th>Ventes/j</th><th>CA (FCFA)</th><th>Coût prod.</th><th>💸 Pub</th><th>📞 Closing</th><th>🚚 Livraison</th><th>💰 Bénéf./j</th><th>📅 Bénéf./mois</th></tr></thead>
          <tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)

        st.markdown('<div class="ndiv"></div>', unsafe_allow_html=True)
        st.markdown("#### 📣 Budget Facebook Ads recommandé")
        if target<=7:    fb=("5 $","1 créative","0-7 ventes/j","#4ade80")
        elif target<=12: fb=("7-8 $","1-2 créatives","7-12 ventes/j","#f4a261")
        elif target<=20: fb=("10-15 $","2-3 créatives","12-20 ventes/j","#e63946")
        else:            fb=("15 $+","3+ créatives","20+ ventes/j","#a78bfa")
        st.markdown(f"""<div class="card" style="border-color:{fb[3]}44;">
          <div style="display:flex;gap:2rem;flex-wrap:wrap;align-items:center;">
            <div><div style="font-family:Orbitron,sans-serif;font-size:2rem;color:{fb[3]};font-weight:900;">{fb[0]} / jour</div>
              <div style="color:#888;font-size:.85rem;">Pour votre objectif de {target} ventes/jour</div></div>
            <div style="text-align:center;"><div style="color:{fb[3]};font-weight:700;">{fb[1]}</div><div style="color:#888;font-size:.78rem;">Créatives conseillées</div></div>
          </div>
          <div style="margin-top:1rem;background:rgba(255,255,255,.04);padding:.7rem 1rem;border-radius:8px;font-size:.88rem;color:#ccc;">
            💡 Démarrez avec 1 créative et {fb[0]}/jour. Si CPA &lt; <b>{profit:,} FCFA</b> après 3 jours → augmentez progressivement.
          </div></div>""", unsafe_allow_html=True)

    # ─── TAB 2 : SCORE ───────────────────────
    with tabs[1]:
        SD = R.get("score",{})
        sv = float(SD.get("score",7)); verdict = SD.get("verdict","Bon"); emoji = SD.get("emoji","👍")
        deg = int((sv/10)*360); sc = "#4ade80" if sv>=7 else "#f4a261" if sv>=5 else "#e63946"

        st.markdown(f"""<div style="text-align:center;padding:1.5rem 0;">
          <div style="display:inline-block;width:180px;height:180px;border-radius:50%;
               background:conic-gradient({sc} {deg}deg,#1a1a2e {deg}deg);box-shadow:0 0 40px {sc}55;position:relative;">
            <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                 width:130px;height:130px;border-radius:50%;background:#0d0d14;
                 display:flex;flex-direction:column;align-items:center;justify-content:center;">
              <div style="font-family:Orbitron,sans-serif;font-size:2.8rem;font-weight:900;color:{sc};">{sv}</div>
              <div style="font-size:.65rem;color:#888;letter-spacing:2px;">/ 10</div>
            </div></div>
          <div style="margin-top:.8rem;font-family:Orbitron,sans-serif;font-size:1.3rem;color:{sc};">{emoji} {verdict.upper()}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("#### 📊 Détail par critère")
        for lbl,key in [("💰 Rentabilité","note_rentabilite"),("📈 Demande marché","note_demande"),
                         ("⚔️ Concurrence","note_concurrence"),("🎨 Créatives dispo","note_creatives"),
                         ("🔥 Potentiel viral","note_viral"),("🌍 Pertinence Afrique","note_afrique"),
                         ("💵 Prix psychologique","note_prix"),("🔄 Fidélisation","note_fidelisation")]:
            val=SD.get(key,7); pct=val*10
            bc="#4ade80" if val>=7 else "#f4a261" if val>=5 else "#e63946"
            st.markdown(f"""<div class="sbar-wrap">
              <div class="sbar-row"><span>{lbl}</span><span style="color:{bc};font-weight:700;">{val}/10</span></div>
              <div class="sbar-bg"><div class="sbar-fill" style="width:{pct}%;background:linear-gradient(90deg,{bc},{bc}66);"></div></div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="ndiv"></div>', unsafe_allow_html=True)
        cA,cB = st.columns(2)
        with cA:
            st.markdown("**✅ Points forts**")
            for p in SD.get("points_forts",[]):
                st.markdown(f'<div style="background:rgba(74,222,128,.1);border-left:3px solid #4ade80;padding:.5rem .8rem;border-radius:0 8px 8px 0;margin:.3rem 0;font-size:.88rem;">✅ {p}</div>', unsafe_allow_html=True)
        with cB:
            st.markdown("**⚠️ Points à surveiller**")
            for p in SD.get("points_faibles",[]):
                st.markdown(f'<div style="background:rgba(230,57,70,.1);border-left:3px solid #e63946;padding:.5rem .8rem;border-radius:0 8px 8px 0;margin:.3rem 0;font-size:.88rem;">⚠️ {p}</div>', unsafe_allow_html=True)

        st.markdown(f"""<div class="card" style="border-color:#f4a261;margin-top:1rem;">
          <div style="color:#f4a261;font-family:Rajdhani,sans-serif;font-weight:700;letter-spacing:2px;margin-bottom:.5rem;font-size:.85rem;">🧭 RECOMMANDATION STRATÉGIQUE</div>
          <div style="line-height:1.8;font-size:.92rem;">{SD.get('recommandation','')}</div>
          <div style="margin-top:.8rem;display:flex;gap:1.5rem;flex-wrap:wrap;font-size:.85rem;">
            <div>🌍 <b>Marchés :</b> {', '.join(SD.get('marches',[]))}</div>
            <div>📅 <b>Période :</b> {SD.get('periode','')}</div>
          </div></div>""", unsafe_allow_html=True)

    # ─── TAB 3 : OFFRES ──────────────────────
    with tabs[2]:
        st.markdown(f'<div class="nlbl">🎁 Offres marketing — {PN}</div>', unsafe_allow_html=True)
        for o in R.get("offres",{}).get("offres",[]):
            ic="#4ade80" if "Élevé" in o.get("impact","") or "Fort" in o.get("impact","") else "#f4a261"
            st.markdown(f"""<div class="ocard">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem;">
                <div><span style="font-size:1.4rem;">{o.get('emoji','🎯')}</span>
                  <span style="font-family:Rajdhani,sans-serif;font-weight:700;font-size:1.05rem;margin-left:.5rem;">{o.get('titre','')}</span></div>
                <span style="color:{ic};border:1px solid {ic}44;padding:.2rem .6rem;border-radius:20px;font-size:.75rem;font-weight:700;">Impact : {o.get('impact','')}</span>
              </div>
              <div style="margin:.5rem 0;color:#ccc;font-size:.88rem;">{o.get('desc','')}</div>
              <div style="background:rgba(244,162,97,.08);border-left:3px solid #f4a261;padding:.4rem .8rem;border-radius:0 8px 8px 0;font-size:.82rem;color:#f4a261;">💡 {o.get('conseil','')}</div>
            </div>""", unsafe_allow_html=True)

    # ─── TAB 4 : SHOPIFY ─────────────────────
    with tabs[3]:
        SH = R.get("shopify",{})
        st.markdown(f'<div class="nlbl">🛍️ Description Shopify — {PN}</div>', unsafe_allow_html=True)
        st.markdown("#### 🏷️ 3 Titres produit optimisés")
        for i,t in enumerate(SH.get("titres",[]),1):
            st.markdown(f'<div style="color:#f4a261;font-family:Rajdhani,sans-serif;font-weight:700;margin-bottom:.2rem;">Titre {i}</div>', unsafe_allow_html=True)
            copy_block(t, f"sh_t{i}")
        st.markdown('<div class="ndiv"></div>', unsafe_allow_html=True)
        st.markdown("#### 📝 6 Paragraphes de description")
        for i,p in enumerate(SH.get("paragraphes",[]),1):
            st.markdown(f'<div style="color:#f4a261;font-family:Rajdhani,sans-serif;font-weight:700;font-size:1rem;margin-top:.8rem;">▶ {p.get("titre","")}</div>', unsafe_allow_html=True)
            copy_block(p.get("contenu",""), f"sh_p{i}")

    # ─── TAB 5 : FACEBOOK ADS ────────────────
    with tabs[4]:
        st.markdown(f'<div class="nlbl">📢 Facebook Ads — {PN}</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#888;font-size:.82rem;margin-bottom:1rem;">3 textes ≤70 mots • Accroche choc + 3 bénéfices</div>', unsafe_allow_html=True)
        for i,ad in enumerate(R.get("facebook",{}).get("ads",[]),1):
            full = f"{ad.get('accroche','')}\n\n- {ad.get('b1','')}\n- {ad.get('b2','')}\n- {ad.get('b3','')}"
            st.markdown(f"""<div style="background:rgba(230,57,70,.07);border-left:3px solid #e63946;padding:.8rem 1rem;border-radius:0 10px 10px 0;margin-bottom:.3rem;">
              <div style="font-weight:700;color:white;font-size:1rem;margin-bottom:.5rem;">🔥 {ad.get('accroche','')}</div>
              <div style="color:#ccc;font-size:.9rem;">✦ {ad.get('b1','')}<br>✦ {ad.get('b2','')}<br>✦ {ad.get('b3','')}</div>
              <div style="font-size:.72rem;color:#555;margin-top:.4rem;">{ad.get('mots','~')} mots</div>
            </div>""", unsafe_allow_html=True)
            copy_block(full, f"fb{i}")

    # ─── TAB 6 : VOIX OFF ────────────────────
    with tabs[5]:
        st.markdown(f'<div class="nlbl">🎙️ Scripts Voix Off — {PN}</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#888;font-size:.82rem;margin-bottom:1rem;">3 scripts • 120-140 mots chacun • Neuromarketing africain</div>', unsafe_allow_html=True)
        for i,s in enumerate(R.get("voix",{}).get("scripts",[]),1):
            txt=s.get("script",""); mots=s.get("mots",len(txt.split()))
            mc="#4ade80" if 120<=mots<=140 else "#f4a261"
            st.markdown(f"""<div style="display:flex;align-items:center;gap:.8rem;margin-bottom:.4rem;">
              <div style="font-family:Orbitron,sans-serif;font-size:.95rem;color:#e63946;font-weight:700;">🎙️ SCRIPT #{i}</div>
              <div style="color:{mc};border:1px solid {mc}44;padding:.15rem .5rem;border-radius:20px;font-size:.72rem;font-weight:700;">{mots} mots</div>
            </div>""", unsafe_allow_html=True)
            copy_block(txt, f"vo{i}")
            st.markdown("<br>", unsafe_allow_html=True)

    # ─── TAB 7 : AVATAR ──────────────────────
    with tabs[6]:
        AV = R.get("avatar",{}).get("avatar",{})
        st.markdown(f'<div class="nlbl">👤 Avatar client — {PN}</div>', unsafe_allow_html=True)
        cL,cR = st.columns(2)
        with cL:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div style="color:#f4a261;font-family:Rajdhani,sans-serif;font-weight:700;letter-spacing:2px;font-size:.82rem;margin-bottom:.8rem;">👤 PROFIL DÉMOGRAPHIQUE</div>', unsafe_allow_html=True)
            for lbl,key in [("🚻 Sexe","sexe"),("🎂 Âge","age"),("👨‍👩‍👧 Situation","situation"),
                              ("💵 Revenus","revenus"),("💼 Profession","profession"),("📍 Villes","ville"),
                              ("🕐 En ligne","heure"),("💰 Budget max","budget"),("🛵 Livraison","livraison"),("🛍️ Achète pour","pour_qui")]:
                val=AV.get(key,"")
                if val:
                    st.markdown(f'<div class="av-sec"><div class="av-lbl">{lbl}</div><div style="font-size:.88rem;">{val}</div></div>', unsafe_allow_html=True)
            rs=AV.get("reseaux",[])
            if rs:
                badges="".join([f'<span style="background:rgba(230,57,70,.2);border:1px solid #e63946;border-radius:20px;padding:.15rem .5rem;margin:.15rem;font-size:.75rem;display:inline-block;">{s}</span>' for s in rs])
                st.markdown(f'<div class="av-sec"><div class="av-lbl">📱 Réseaux</div><div>{badges}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with cR:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div style="color:#f4a261;font-family:Rajdhani,sans-serif;font-weight:700;letter-spacing:2px;font-size:.82rem;margin-bottom:.8rem;">🧠 PROFIL PSYCHOLOGIQUE</div>', unsafe_allow_html=True)
            for lbl,key,clr in [("😱 Peurs","peurs","#e63946"),("😤 Frustrations","frustrations","#f4a261"),
                                  ("💫 Désirs","desirs","#a78bfa"),("⚡ Motivations","motivations","#4ade80"),
                                  ("❓ Objections","objections","#fb923c"),("✅ Réponses","reponses","#4ade80")]:
                items=AV.get(key,[])
                if items:
                    bullets="".join([f'<div style="margin:.2rem 0;padding:.35rem .7rem;background:rgba(0,0,0,.3);border-left:3px solid {clr};border-radius:0 8px 8px 0;font-size:.85rem;">▸ {x}</div>' for x in items])
                    st.markdown(f'<div class="av-sec"><div class="av-lbl" style="color:{clr};">{lbl}</div>{bullets}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        phrase=AV.get("phrase","")
        if phrase:
            st.markdown(f"""<div class="card" style="border-color:#f4a261;text-align:center;margin-top:.8rem;">
              <div style="color:#f4a261;font-family:Rajdhani,sans-serif;font-weight:700;letter-spacing:2px;font-size:.82rem;margin-bottom:.6rem;">💬 PHRASE DÉCLENCHANTE</div>
              <div style="font-size:1.1rem;font-style:italic;color:white;line-height:1.7;">"{phrase}"</div>
            </div>""", unsafe_allow_html=True)
            copy_block(phrase, "phrase")

    # ─── TAB 8 : IMAGES ──────────────────────
    with tabs[7]:
        st.markdown(f'<div class="nlbl">🖼️ Images produit — {PN}</div>', unsafe_allow_html=True)
        if st.session_state.product_images:
            st.markdown("#### 📷 Vos images uploadées")
            nb=len(st.session_state.product_images)
            ic=st.columns(min(nb,5))
            for i,img_file in enumerate(st.session_state.product_images):
                with ic[i%5]:
                    st.image(img_file, use_container_width=True)
                    img_file.seek(0)
                    b64=base64.b64encode(img_file.read()).decode()
                    ext=img_file.name.split(".")[-1]
                    st.markdown(f'<a href="data:image/{ext};base64,{b64}" download="{img_file.name}"><button style="width:100%;background:linear-gradient(135deg,#e63946,#ff6b35);border:none;color:white;padding:.35rem;border-radius:6px;cursor:pointer;font-size:.75rem;margin-top:.2rem;">⬇️ Télécharger</button></a>', unsafe_allow_html=True)
                    img_file.seek(0)
        st.markdown('<div class="ndiv"></div>', unsafe_allow_html=True)
        st.markdown("#### 🔍 Rechercher des images en ligne")
        q=urllib.parse.quote(PN)
        gc=st.columns(3)
        for i,(name,url,clr) in enumerate([
            ("🟠 AliExpress",f"https://fr.aliexpress.com/wholesale?SearchText={q}","#ff6010"),
            ("🔵 Alibaba",f"https://www.alibaba.com/trade/search?SearchText={q}","#e6380a"),
            ("🔴 Pinterest",f"https://www.pinterest.com/search/pins/?q={q}","#e60023"),
            ("🟡 Temu",f"https://www.temu.com/search_result.html?search_key={q}","#f4a261"),
            ("🔍 Google Images",f"https://www.google.com/search?q={q}&tbm=isch","#4285f4"),
            ("🛒 Amazon",f"https://www.amazon.fr/s?k={q}","#ff9900"),
        ]):
            with gc[i%3]:
                st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none;"><div class="plink" style="border-color:{clr}33;"><div style="font-size:1.2rem;">{name.split()[0]}</div><div style="font-weight:700;color:{clr};font-family:Rajdhani,sans-serif;">{name[2:]}</div><div style="font-size:.72rem;color:#666;margin-top:.2rem;">Cliquer → recherche auto 🔍</div></div></a>', unsafe_allow_html=True)

    # ─── TAB 9 : VIDÉOS ──────────────────────
    with tabs[8]:
        st.markdown(f'<div class="nlbl">🎬 Vidéos produit — {PN}</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#888;font-size:.82rem;margin-bottom:1rem;">Cliquez sur un pays → la plateforme s\'ouvre avec votre produit + pays déjà recherchés</div>', unsafe_allow_html=True)
        q=urllib.parse.quote(PN)
        for pname_v,pclr,make_url in [
            ("▶️ YouTube","#ff0000", lambda p: f"https://www.youtube.com/results?search_query={q}+{urllib.parse.quote(p)}"),
            ("🎵 TikTok","#010101",  lambda p: f"https://www.tiktok.com/search?q={q}+{urllib.parse.quote(p)}"),
            ("📌 Pinterest","#e60023",lambda p: f"https://www.pinterest.com/search/pins/?q={q}+{urllib.parse.quote(p)}"),
            ("🔍 Google Vidéos","#4285f4",lambda p: f"https://www.google.com/search?q={q}+{urllib.parse.quote(p)}&tbm=vid"),
            ("🟠 AliExpress","#ff6010",lambda p: f"https://fr.aliexpress.com/wholesale?SearchText={q}"),
        ]:
            st.markdown(f'<div class="card" style="border-color:{pclr}44;"><div style="font-family:Rajdhani,sans-serif;font-weight:700;font-size:1rem;color:{pclr};margin-bottom:.7rem;">{pname_v}</div><div style="display:flex;flex-wrap:wrap;gap:.5rem;">', unsafe_allow_html=True)
            for pays in PAYS:
                url=make_url(pays)
                st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none;"><span style="background:rgba(0,0,0,.4);border:1px solid {pclr}44;color:{pclr};padding:.3rem .7rem;border-radius:20px;font-size:.8rem;display:inline-block;">🌍 {pays} →</span></a>', unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

    # ─── TAB 10 : CONCURRENCE ────────────────
    with tabs[9]:
        st.markdown(f'<div class="nlbl">⚔️ Concurrence — {PN}</div>', unsafe_allow_html=True)
        q=urllib.parse.quote(PN)

        st.markdown("#### 📚 Bibliothèque Publicitaire Facebook par pays")
        st.markdown('<div style="color:#888;font-size:.82rem;margin-bottom:1rem;">Voyez les publicités actives de vos concurrents dans chaque pays</div>', unsafe_allow_html=True)
        cp=st.columns(3)
        for i,pays in enumerate(PAYS):
            code=PAYS_CODES.get(pays,"")
            url=f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={code}&q={q}&search_type=keyword_unordered"
            with cp[i%3]:
                st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none;"><div class="plink" style="border-color:#1877f244;"><div style="font-size:1.1rem;">🌍</div><div style="font-weight:700;color:#1877f2;font-family:Rajdhani,sans-serif;">{pays}</div><div style="font-size:.72rem;color:#666;margin-top:.2rem;">Pub library Facebook →</div></div></a>', unsafe_allow_html=True)

        st.markdown('<div class="ndiv"></div>', unsafe_allow_html=True)
        st.markdown("#### 🏪 Boutiques concurrentes")
        for sname,sclr,make_url in [
            ("🛒 Facebook Pages","#1877f2",lambda p: f"https://www.facebook.com/search/pages/?q={q}+boutique+{urllib.parse.quote(p)}"),
            ("🌐 Google Shopping","#4285f4",lambda p: f"https://www.google.com/search?q={q}+boutique+{urllib.parse.quote(p)}&tbm=shop"),
            ("🟠 AliExpress","#ff6010",lambda p: f"https://fr.aliexpress.com/wholesale?SearchText={q}"),
            ("🔵 Jumia","#f68b1e",lambda p: f"https://www.jumia.com/catalog/?q={q}"),
        ]:
            st.markdown(f'<div class="card" style="border-color:{sclr}44;"><div style="font-family:Rajdhani,sans-serif;font-weight:700;font-size:1rem;color:{sclr};margin-bottom:.7rem;">{sname}</div><div style="display:flex;flex-wrap:wrap;gap:.5rem;">', unsafe_allow_html=True)
            for pays in PAYS:
                url=make_url(pays)
                st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none;"><span style="background:rgba(0,0,0,.4);border:1px solid {sclr}44;color:{sclr};padding:.3rem .7rem;border-radius:20px;font-size:.8rem;display:inline-block;">🌍 {pays} →</span></a>', unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("""<div class="card" style="border-color:#f4a261;">
          <div style="color:#f4a261;font-weight:700;margin-bottom:.5rem;">💡 Comment analyser la concurrence ?</div>
          <div style="font-size:.88rem;color:#ccc;line-height:1.8;">
            1. <b>Bibliothèque pub Facebook</b> → Regardez les pubs actives sur votre produit<br>
            2. +50 pubs actives = marché validé ✅ (concurrence élevée)<br>
            3. 0-10 pubs = marché non validé ⚠️ (risque mais opportunité)<br>
            4. Inspirez-vous des meilleures accroches et offres<br>
            5. Différenciez-vous avec une meilleure offre ou un angle unique
          </div></div>""", unsafe_allow_html=True)

elif not st.session_state.form_open:
    st.markdown("""<div style="text-align:center;padding:3rem 1rem;">
      <div style="font-size:3rem;margin-bottom:1rem;">🚀</div>
      <div style="font-family:Orbitron,sans-serif;font-size:1.2rem;color:#e63946;margin-bottom:.8rem;">PRÊT À ANALYSER VOTRE PRODUIT ?</div>
      <div style="color:#888;font-size:.9rem;">Ouvrez le formulaire en haut, remplissez les informations et lancez l'analyse.</div>
    </div>""", unsafe_allow_html=True)
