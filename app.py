import streamlit as st
import google.generativeai as genai
from PIL import Image

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

if st.button("LANCER L'ANALYSE NEURO-MARKETING") and uploaded_file and api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- LOGIQUE D'AUTO-DÉTECTION ---
        # On essaie les noms les plus courants un par un
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-8b', 'gemini-1.5-pro', 'gemini-pro-vision']
        model = None
        
        for model_name in models_to_try:
            try:
                test_model = genai.GenerativeModel(model_name)
                # Si on arrive ici sans erreur, c'est que le nom est bon !
                model = test_model
                break
            except:
                continue
        
        if model is None:
            st.error("Aucun modèle trouvé. Essaie de créer une NOUVELLE clé API sur Google AI Studio.")
        else:
            img = Image.open(uploaded_file)
            prompt = f"Analyse ce produit : {product_name}. Rédige un score /10, 5 paragraphes de vente neuro-marketing, 3 titres chocs, et un script voix-off (Problème-Solution-CTA)."
            
            with st.spinner(f'Analyse en cours avec le moteur {model_name}...'):
                response = model.generate_content([prompt, img])
                st.markdown("---")
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Erreur : {e}")
