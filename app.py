import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Stock Ergo", layout="wide")

@st.cache_data(ttl=5)
def load_data():
    # URL de publication CSV
    url = "https://docs.google.com"
    
    try:
        r = requests.get(url, timeout=10)
        # On lit le flux. Si Google envoie du HTML par erreur, on nettoie.
        df = pd.read_csv(io.StringIO(r.text), on_bad_lines='skip')
        
        # FILTRE DE SÉCURITÉ :
        # On ne garde que les lignes dont la première colonne est courte (un ID ou un petit texte)
        # Cela élimine tout le code Google (CSS/JS) qui est très long.
        df = df[df.iloc[:, 0].astype(str).map(len) < 50]
        # On retire les lignes contenant des balises ou du code
        df = df[~df.iloc[:, 0].astype(str).str.contains("<|{|#|var\(", na=False)]
        
        return df.dropna(how='all')
    except:
        return pd.DataFrame()

st.title("📦 Gestion de Stock Ergothérapie")

df_stock = load_data()

if not df_stock.empty and len(df_stock.columns) > 1:
    st.success(f"✅ {len(df_stock)} matériel(s) trouvé(s)")
    st.dataframe(df_stock, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ Chargement des données...")
    st.info("Si rien ne s'affiche, vérifiez que vous avez bien publié au format 'CSV' dans Google Sheets.")

st.divider()
st.link_button("➕ Modifier sur Google Sheets", "https://docs.google.com")
