import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuration de l'interface
st.set_page_config(page_title="e-com Family Tool by Labo", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #d90429; color: white; width: 100%; border-radius: 10px; font-weight: bold; height: 3em; }
    h1 { color: #d90429; text-align: center; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #1a1c23; color: white; border: 1px solid #d90429; }
    .stInfo { background-color: #1a1c23; border: 1px solid #0077b6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ e-com Family Tool by Labo")

# Clé API dans la barre latérale
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Entre ta clé API ici :", type="password")

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("Nom du produit", placeholder="Ex: Pince Multifonction")
    purchase_price = st.number_input("Prix d'achat (FCFA)", min_value=0, value=2500)
    uploaded_file = st.file_uploader("Photo du produit", type=["jpg", "png", "jpeg"])

with col2:
    if purchase_price > 0:
        # Ta logique de prix (Intervalle 8k - 12k)
        p_min = purchase_price + 8000
        p_max = purchase_price + 12000
        st.info(f"💰 **Vendre entre : {p_min:,} et {p_max:,} FCFA**")
        st.write("📊 **Budget Pub :** 4$ à 7$ / jour (Focus sur 1 seule créative).")

if st.button("LANCER L'ANALYSE NEURO-MARKETING") and uploaded_file and api_key:
    try:
        genai.configure(api_key=api_key)
        # UTILISATION DE GEMINI 3 FLASH (Modèle 2026)
        model = genai.GenerativeModel('gemini-3-flash')
        img = Image.open(uploaded_file)
        
        prompt = f"""
        En tant qu'expert en neuro-marketing pour le marché africain, analyse ce produit : {product_name}.
        1. Donne un score de potentiel /10 (sois très réaliste).
        2. Identifie les frustrations réelles et les peurs des clients (pourquoi ils hésitent à acheter).
        3. Rédige 5 paragraphes de vente Shopify ultra-persuasifs basés sur l'émotion et l'effet WOW.
        4. Propose 3 titres "Stop-Scroll" magnétiques.
        5. Rédige 3 textes publicitaires Facebook courts avec emojis.
        6. Rédige un script Voix-Off (Accroche choc > Problème > Solution > Témoignage > CTA).
        Ton ton doit être humain, puissant et direct.
        """
        
        with st.spinner('Labo AI analyse les frustrations du marché...'):
            response = model.generate_content([prompt, img])
            st.markdown("---")
            st.success("✅ Analyse terminée avec succès !")
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Erreur de connexion : Vérifie que ta clé API est correcte ou réessaie dans 1 minute.")
        st.info("Astuce : Si l'erreur persiste, c'est que Google met à jour ses serveurs pour Gemini 3.")
