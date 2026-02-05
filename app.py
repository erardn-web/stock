import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Stock Ergo", layout="wide")

@st.cache_data(ttl=30)
def load_public_data():
    # Ton URL de publication convertie en format CSV
    url = "https://docs.google.com"
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        # On lit le texte reçu
        df = pd.read_csv(io.StringIO(r.text))
        return df
    except Exception as e:
        st.error(f"Erreur de flux : {e}")
        return pd.DataFrame()

st.title("📦 Gestion de Stock Ergothérapie")

df_stock = load_public_data()

if not df_stock.empty:
    st.success("✅ Données synchronisées")
    
    # Recherche simple
    search = st.text_input("🔍 Rechercher un matériel...")
    if search:
        mask = df_stock.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        df_display = df_stock[mask]
    else:
        df_display = df_stock
        
    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ En attente des données...")
    st.info("Vérifiez que le Google Sheet contient des données et qu'il est bien publié.")

st.divider()
# Lien pour aller modifier le contenu
st.link_button("➕ Modifier sur Google Sheets", "https://docs.google.com")
