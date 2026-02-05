import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Stock Ergo", layout="wide")

@st.cache_data(ttl=5)
def load_public_data():
    # URL de publication CSV (Attention au format à la fin)
    url = "https://docs.google.com"
    
    try:
        r = requests.get(url, timeout=10)
        # On ne garde que les données si le serveur répond OK
        if r.status_code == 200:
            # On lit le texte reçu
            df = pd.read_csv(io.StringIO(r.text), on_bad_lines='skip')
            
            # NETTOYAGE CRUCIAL :
            # On ne garde que les lignes où la première colonne est un chiffre (ID) 
            # ou dont le nom n'est pas du code bizarre (pas de { ou <)
            if not df.empty:
                # On filtre pour ne garder que les lignes "propres"
                df = df[df.iloc[:, 0].astype(str).str.len() < 50] # Supprime les lignes trop longues (code)
                df = df[~df.iloc[:, 0].astype(str).str.contains("<|{|#", na=False)] # Supprime le HTML/CSS
            
            return df
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

st.title("📦 Gestion de Stock Ergothérapie")

df_stock = load_public_data()

# Affichage des statistiques réelles
if not df_stock.empty and len(df_stock.columns) > 1:
    st.success(f"✅ {len(df_stock)} article(s) trouvé(s)")
    st.dataframe(df_stock, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ En attente de données valides...")
    st.info("Allez dans Google Sheets > Fichier > Partager > Publier sur le Web. Vérifiez que vous avez publié 'Toute la feuille' au format 'Valeurs séparées par des virgules (.csv)'.")

st.divider()
st.link_button("➕ Modifier sur Google Sheets", "https://docs.google.com")
