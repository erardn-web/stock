import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="ErgoStock Pro", layout="wide")

# 1. Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Chargement des données (ttl=0 pour rafraîchir à chaque action)
def load_data():
    stock = conn.read(worksheet="stock", ttl=0).dropna(how='all')
    hist = conn.read(worksheet="historique", ttl=0).dropna(how='all')
    return stock, hist

df_stock, df_hist = load_data()

st.title("📦 Gestion de Stock & Historique")

tab1, tab2, tab3 = st.tabs(["📊 Inventaire", "🔄 Mouvements", "➕ Nouvel Article"])

# --- TAB 1 : INVENTAIRE ---
with tab1:
    st.subheader("État actuel du matériel")
    search = st.text_input("🔍 Rechercher un article")
    if search:
        st.dataframe(df_stock[df_stock['nom'].str.contains(search, case=False, na=False)], use_container_width=True, hide_index=True)
    else:
        st.dataframe(df_stock, use_container_width=True, hide_index=True)

# --- TAB 2 : MOUVEMENTS (PRÊTS, RETOURS, VENTES) ---
with tab2:
    st.subheader("Enregistrer un mouvement")
    if not df_stock.empty:
        with st.form("form_mouvement"):
            article_nom = st.selectbox("Sélectionner l'article", df_stock["nom"].unique())
            action = st.selectbox("Action", ["Prêt", "Retour", "Vente", "Location", "Mise au rebut"])
            note = st.text_input("Commentaire (ex: Nom du patient, état du matériel)")
            
            if st.form_submit_button("Valider le mouvement"):
                # 1. Trouver l'ID de l'article
                item_idx = df_stock[df_stock["nom"] == article_nom].index[0]
                item_id = df_stock.at[item_idx, "id"]
                
                # 2. Mettre à jour le statut dans l'onglet STOCK
                nouveaux_statuts = {"Prêt": "Prêté", "Retour": "Disponible", "Vente": "Vendu", "Location": "Loué", "Mise au rebut": "Jeté"}
                df_stock.at[item_idx, "statut"] = nouveaux_statuts.get(action, "Inconnu")
                
                # 3. Ajouter une ligne dans l'onglet HISTORIQUE
                nouvel_hist = pd.DataFrame([{
                    "id_materiel": item_id,
                    "nom_article": article_nom,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "action": action,
                    "notes": note
                }])
                
                df_hist_updated = pd.concat([df_hist, nouvel_hist], ignore_index=True)
                
                # 4. Sauvegarde simultanée
                conn.update(worksheet="stock", data=df_stock)
                conn.update(worksheet="historique", data=df_hist_updated)
                
                st.success(f"✅ Action '{action}' enregistrée pour {article_nom}")
                st.rerun()
    else:
        st.info("Aucun article en stock.")

# --- TAB 3 : AJOUTER UN ARTICLE ---
with tab3:
    st.subheader("Créer une nouvelle fiche matériel")
    with st.form("form_ajout"):
        nom = st.text_input("Nom de l'article")
        provenance = st.selectbox("Provenance", ["Achat", "Dépôt en prêt", "Don"])
        options = st.multiselect("Possibilités", ["Prêtable", "Louable", "Achetable"])
        
        if st.form_submit_button("Créer l'article"):
            if nom:
                new_id = int(df_stock["id"].max() + 1) if not df_stock.empty else 1
                new_item = pd.DataFrame([{
                    "id": new_id,
                    "nom": nom,
                    "provenance": provenance,
                    "options": ", ".join(options),
                    "statut": "Disponible"
                }])
                
                df_stock_updated = pd.concat([df_stock, new_item], ignore_index=True)
                conn.update(worksheet="stock", data=df_stock_updated)
                
                st.success(f"✨ {nom} a été ajouté à l'inventaire.")
                st.rerun()

# --- AFFICHAGE HISTORIQUE (BAS DE PAGE) ---
st.divider()
st.subheader("📜 Historique récent des allers-retours")
if not df_hist.empty:
    st.dataframe(df_hist.sort_index(ascending=False), use_container_width=True, hide_index=True)
