import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Stock Ergo", layout="wide")

@st.cache_data(ttl=60)
def load_data():
    sid = "11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8"
    gid = "1192360349"
    # URL simplifiée
    url = f"https://docs.google.com{sid}/export?format=csv&gid={gid}"
    
    # Tentative de téléchargement via requests au lieu de pandas
    response = requests.get(url, timeout=10)
    response.raise_for_status() # Erreur si Google ne répond pas
    
    # Conversion du texte reçu en tableau
    return pd.read_csv(io.StringIO(response.text))

st.title("📦 Gestion de Stock Ergothérapie")

try:
    df_stock = load_data()
    st.success("✅ Connexion établie !")
    st.dataframe(df_stock, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("⚠️ Blocage réseau détecté.")
    st.write("Détail technique pour le support :", e)
    
    # Bouton de secours si le Cloud Streamlit est en panne de DNS
    st.info("💡 Si l'erreur persiste, essayez de supprimer et recréer l'app dans une autre zone (Advanced Settings > Western Europe).")

st.divider()
st.link_button("➕ Modifier sur Google Sheets", "https://docs.google.com11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8/edit")
