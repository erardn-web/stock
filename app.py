import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Ergo", layout="wide")

# Methode ultra-directe pour éviter l'erreur de nom de service
@st.cache_data(ttl=60)
def load_data():
    # Ton ID de document sans aucun autre caractère
    sid = "11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8"
    gid = "1192360349"
    full_url = f"https://docs.google.com{sid}/export?format=csv&gid={gid}"
    
    return pd.read_csv(full_url)

st.title("📦 Gestion de Stock Ergothérapie")

try:
    df_stock = load_data()
    
    if not df_stock.empty:
        # Recherche
        search = st.text_input("🔍 Rechercher un matériel...")
        if search:
            mask = df_stock.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
            df_display = df_stock[mask]
        else:
            df_display = df_stock
            
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning("Le fichier est vide.")

except Exception as e:
    st.error("⚠️ Problème de connexion au Google Sheet.")
    st.info("Tentative de diagnostic : vérifiez que le partage est bien 'Tous les utilisateurs disposant du lien'.")
    # Affiche l'erreur technique pour nous aider si ça rate encore
    st.expander("Détails techniques").write(e)

st.divider()
st.link_button("➕ Modifier sur Google Sheets", "https://docs.google.com11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8/edit")
