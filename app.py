import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Stock Ergo", layout="wide")

@st.cache_data(ttl=10)
def load_public_data():
    # URL de publication CSV
    url = "https://docs.google.com"
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        
        # On lit le CSV en ignorant les lignes qui ont trop de colonnes (on_bad_lines)
        df = pd.read_csv(io.StringIO(r.text), on_bad_lines='skip', sep=',')
        
        # On ne garde que les lignes où la colonne 'nom' n'est pas vide
        if 'nom' in df.columns:
            df = df.dropna(subset=['nom'])
            
        return df
    except Exception as e:
        st.error(f"Erreur d'analyse des données : {e}")
        return pd.DataFrame()

st.title("📦 Gestion de Stock Ergothérapie")

df_stock = load_public_data()

if not df_stock.empty:
    st.success(f"✅ {len(df_stock)} articles trouvés")
    
    # Recherche
    search = st.text_input("🔍 Rechercher un matériel...")
    if search:
        mask = df_stock.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        df_display = df_stock[mask]
    else:
        df_display = df_stock
        
    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ Les données sont mal formatées ou le tableau est vide.")
    st.info("Conseil : Assurez-vous que la première ligne du Google Sheet contient vos titres (id, nom, provenance, etc.) sans lignes vides au-dessus.")

st.divider()
st.link_button("➕ Modifier sur Google Sheets", "https://docs.google.com")
