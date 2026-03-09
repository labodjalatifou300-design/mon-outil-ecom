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
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ e-com Family Tool by Labo")

# Clé API
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Entre ta clé API ici :", type="password")

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("Nom du produit", placeholder="Ex: Pince Multifonction")
    purchase_price = st.number_input("Prix d'achat (FCFA)", min_value=0, value=2500)
    uploaded_file = st.file_uploader("Photo du produit", type=["jpg", "png", "jpeg"])

with col2:
    if purchase_price > 0:
        st.info(f"💰 **Vendre entre : {purchase_price + 8000:,} et {purchase_price + 12000:,} FCFA**")
        st.write("📊 **Budget Pub :** 4$ à 7$ / jour (Focus sur 1 seule créative).")

if st.button("LANCER L'ANALYSE NEURO-MARKETING") and uploaded_file and api_key:
    try:
        genai.configure(api_key=api_key)
        
        # ON UTILISE LE NOM DE MODÈLE LE PLUS STABLE
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        img = Image.open(uploaded_file)
        
        prompt = f"""
        Analyse ce produit e-commerce : {product_name}.
        En tant qu'expert en neuro-marketing :
        1. Score de potentiel /10.
        2. Liste les frustrations et peurs des clients.
        3. Rédige 5 paragraphes de vente Shopify (émotionnel).
        4. 3 titres 'Stop-Scroll'.
        5. Texte pub Facebook + Script Voix-Off (Problème-Solution-CTA).
        Ton ton doit être humain et percutant.
        """
        
        with st.spinner('Connexion sécurisée à Labo AI...'):
            response = model.generate_content([prompt, img])
            st.markdown("---")
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Détail : {e}")
        st.info("Conseil : Vérifie que ta clé API ne contient pas d'espace au début ou à la fin quand tu la colles.")
