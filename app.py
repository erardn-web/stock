import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="GéoStock Ergo", layout="wide")

# Fichiers de données (Simples CSV pour commencer)
DATA_FILE = "stock_materiel.csv"
HISTORY_FILE = "historique_materiel.csv"

# Initialisation des fichiers si inexistants
for file, columns in {DATA_FILE: ["id", "nom", "provenance", "options", "statut"], 
                       HISTORY_FILE: ["id_materiel", "date", "action", "notes"]}.items():
    if not os.path.exists(file):
        pd.DataFrame(columns=columns).to_csv(file, index=False)

# Fonctions de chargement
def load_data(file):
    return pd.read_csv(file)

def save_data(df, file):
    df.to_csv(file, index=False)

# --- INTERFACE ---
st.title("📦 Gestion de Matériel Ergothérapie")

tab1, tab2, tab3 = st.tabs(["📋 Inventaire", "➕ Ajouter Matériel", "📜 Historique"])

# --- TAB 2 : AJOUTER DU MATÉRIEL ---
with tab2:
    st.header("Nouvel objet")
    with st.form("ajout_objet"):
        nom = st.text_input("Nom de l'objet (ex: Déambulateur Rollator)")
        
        col1, col2 = st.columns(2)
        with col1:
            prov = st.selectbox("Mode d'obtention", ["Achat", "Prêt fournisseur", "Don"])
        with col2:
            options = st.multiselect("Options possibles", ["Prêtable", "Louable", "Achetable"])
        
        submit = st.form_submit_button("Créer l'objet")
        
        if submit and nom:
            df = load_data(DATA_FILE)
            new_id = len(df) + 1
            new_item = {
                "id": new_id,
                "nom": nom,
                "provenance": prov,
                "options": ", ".join(options),
                "statut": "Disponible"
            }
            df = pd.concat([df, pd.DataFrame([new_item])], ignore_index=True)
            save_data(df, DATA_FILE)
            
            # Entrée initiale dans l'historique
            hist_df = load_data(HISTORY_FILE)
            new_hist = {"id_materiel": new_id, "date": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                        "action": "Création", "notes": f"Entrée en stock via {prov}"}
            hist_df = pd.concat([hist_df, pd.DataFrame([new_hist])], ignore_index=True)
            save_data(hist_df, HISTORY_FILE)
            
            st.success(f"'{nom}' ajouté avec succès !")

# --- TAB 1 : INVENTAIRE ---
with tab1:
    st.header("Matériel en stock")
    df_stock = load_data(DATA_FILE)
    if not df_stock.empty:
        st.dataframe(df_stock, use_container_width=True)
    else:
        st.info("L'inventaire est vide.")

# --- TAB 3 : HISTORIQUE ---
with tab3:
    st.header("Parcours d'un élément")
    df_stock = load_data(DATA_FILE)
    if not df_stock.empty:
        choix = st.selectbox("Sélectionner un objet", df_stock["nom"].unique())
        id_choisi = df_stock[df_stock["nom"] == choix]["id"].values[0]
        
        df_hist = load_data(HISTORY_FILE)
        parcours = df_hist[df_hist["id_materiel"] == id_choisi]
        st.table(parcours[["date", "action", "notes"]])
    else:
        st.write("Aucune donnée à afficher.")
