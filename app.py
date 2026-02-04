import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration
st.set_page_config(page_title="GéoStock Ergo", layout="wide")

# --- CONFIGURATION DE L'URL ---
# ID de votre sheet extrait de votre lien
SHEET_ID = "11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8"
# GID 0 est généralement la première feuille (stock)
URL_STOCK = f"https://docs.google.com{SHEET_ID}/export?format=csv&gid=0"
# Pour l'historique, on essaiera de lire la feuille nommée 'historique'
URL_HIST = f"https://docs.google.com{SHEET_ID}/export?format=csv&sheet=historique"

def load_data():
    try:
        # Lecture directe du CSV public via Pandas
        stock = pd.read_csv(URL_STOCK)
        try:
            hist = pd.read_csv(URL_HIST)
        except:
            hist = pd.DataFrame(columns=["id_materiel", "date", "action", "notes"])
        
        # Nettoyage des données vides
        stock = stock.dropna(subset=['nom']) if 'nom' in stock.columns else stock
        return stock, hist
    except Exception as e:
        st.error(f"Erreur de connexion au Google Sheet : {e}")
        return pd.DataFrame(), pd.DataFrame()

df_stock, df_hist = load_data()

st.title("📦 Gestion de Stock Ergothérapie")

tab1, tab2, tab3 = st.tabs(["📋 Inventaire & Actions", "➕ Ajouter Matériel", "📜 Historique"])

# --- TAB 1 : INVENTAIRE & ACTIONS ---
with tab1:
    st.header("Matériel en stock")
    if not df_stock.empty:
        # Affichage du tableau
        st.dataframe(df_stock, use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("Modifier un statut")
        
        # Sélection pour action
        selected_name = st.selectbox("Choisir un objet :", ["---"] + df_stock["nom"].tolist())
        
        if selected_name != "---":
            idx = df_stock[df_stock["nom"] == selected_name].index[0]
            current_status = df_stock.at[idx, 'statut']
            
            st.write(f"Statut actuel : **{current_status}**")
            
            c1, c2, c3, c4 = st.columns(4)
            new_status = None
            
            with c1: 
                if st.button("🤝 Prêter"): new_status, action = "Prêté", "Prêt"
            with c2: 
                if st.button("🔄 Retour"): new_status, action = "Disponible", "Retour"
            with c3: 
                if st.button("💰 Vendre"): new_status, action = "Vendu", "Vente"
            with c4: 
                if st.button("🗑️ Jeter"): new_status, action = "Jeté", "Rebut"
            
            if new_status:
                st.warning("⚠️ Note : Pour sauvegarder cette modification, ouvrez votre Google Sheet et changez le statut manuellement (La version gratuite 'lecture seule' ne permet pas l'écriture directe sans configuration complexe).")
    else:
        st.info("Aucune donnée trouvée. Vérifiez que la première ligne du Google Sheet contient : id, nom, provenance, options, statut")

# --- TAB 2 : AJOUTER DU MATÉRIEL ---
with tab2:
    st.header("Ajouter un nouvel élément")
    st.write("Pour ajouter un élément, remplissez une nouvelle ligne dans votre [Google Sheet](https://docs.google.com11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8/edit)")
    
    with st.expander("Voir l'aide au remplissage"):
        st.markdown("""
        1. Allez sur le Google Sheet.
        2. Ajoutez une ligne avec :
           - **id** : Le numéro suivant.
           - **nom** : Nom de l'objet.
           - **provenance** : Achat, Don, ou Prêt fournisseur.
           - **options** : Louable, Prêtable, etc.
           - **statut** : Disponible.
        """)

# --- TAB 3 : HISTORIQUE ---
with tab3:
    st.header("Historique")
    if not df_hist.empty:
        st.table(df_hist)
    else:
        st.info("L'historique est géré dans l'onglet 'historique' de votre Google Sheet.")
