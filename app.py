import streamlit as st
import pandas as pd
from gspread_pandas import Spread
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Stock Ergo Pro", layout="wide")

# --- CONFIGURATION DES IDENTIFIANTS ---
# Note : La clé est collée exactement comme dans le JSON original
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCXmLNyCfYDgYPk
QLcRittmVdJOLm4mmlRLmrjva3moMQBdSw36OFdw0w2SLQMhGsxbP7yFaTlAXv4s
AwH6nF/MOJ1JqFE5gIMIbz18lqbEHEXqMHl80mnXz6ZyreFZrjQfz5yaEpC7k6nf
zQaX17iQ3iCuBjUR+qcb6TW0xsItJjU4srw8ITA1/EbRmxLnBSEza6EYpm3ZkJqr
fWGwA4oQAHB5AjeHvy/Wdb3Ji4b6eLDad75ttY6niia9n91GnYrf0mzCHDUvAqNG
IixGPV4Bt7M/s7o6m8JiLFtgMQ5iPXXDFFVb1xV7yw7AzvESurmwcMbDUH/WLyvU
lnPqUDLJAgMBAAECgf8gBrfiSmMZhS3CoD63YLPOgChYhqE+sTFIclIfl9UGc1O1
tzrSDJUXK39HzQ/xg80oeePvS2DiTdnknRNjSSXz6aymTajbPQscUmPrA5NiWuwU
+FNcy2xmQLgpV2gESjPjhI4mU/BqWwfIVXLPIVkclyYlnaoYjPDrie6OrRmDRVE5
QwF7+xTmjyfk+BOkIGDI09AYK6OtPSv6+YCGDBTTGrDPJhP2htMx2OiqQ0vJQja0
aYw6iCZzuz1vITadtYvg3sV+EtPWk/HN5r0D9ikkKkfE4QhzVA6xJfHPwuWvgmDI
DtbrST8OemZpvUWX0eLowKampbkyHFP5eNyTauECgYEAyF5po23n0ykxDZ+xBGvj
VpoNXf53aRM44LwPJI3ZoEJSCLAeBTGRSklpTBYUmqhJ8Rfh2F89bpe+fB+e89jo
6ab+pIc+K8WxgQ+zEyNUotjdC4oam8wA5SdByFRh0IGwdg6VaMNTYnqhbXk4tRFN
ntFYV1EiYffH3k2ttbNigJHECgYEAwa+0fDn5JmNNICtoBhII2Z2GCRflVS15+Mxr
j5UcZkS3Z8zOpDL43Dg28wXhnAPScp7iBCggV1x8QuGtYPe8ie3hqubLKpGavcpL
ZUPixO24tW6hjOWY2sRlZEvrcWhKbfV9KwcnzDSP/6yyJ3+cc+YffpKNNk63SR36
ExHxv9kCgYAZpqyTdZCGIfHbsqPw0vcJsTMg42DaHNHdQ3YU0ewYbiUeY52UQKI/
BmLqkLEWk5DTwqDxGFA/BkImlc29nflDYFOdMIsvA2IUCbR9MLq3FlhGD+oUI+vB
amMriFH1ZYT3uCo8fTUBmH1uDGTMGWj/Oz4ULS8IgJ+XSdt6YckuoQKBgQCjA/Y9
RDHt3FASjlX8Hfuy5MDmMGWFvkPVYn/5FgAUFyviQl99laUc/HdLLZ0ISbM7Y3xJ
EVi/DolLZVQetAPMdxmjVKKUjn4V1QiGD4/yPT5j/dwckTWIkxnfQ4LDLYrPZ3nU
2C3n0imMgFZlpiMQ7RN+3Wva1H+xG3jZyhWVaQKBgCFuQs+EllaHZYS/EVRgKqKs
/MMrHJyAzJSc5ItUjGJVXDamjy38MKh50mQ6L1iXWmf4ilw8xdWYHhqjfVWYEKWn
KaCKiw3wJZqpCHZC3ZP+6qAclgxczDe/AStCeYv/c7EU5P7lTLVEQf2XoETqAX6e
B3pqwbNSZBox8qUCgY5G
-----END PRIVATE KEY-----"""

creds = {
    "type": "service_account",
    "project_id": "stock-ergo",
    "private_key_id": "5e62902c2f1be2356209dc3cb16a5059def2dd93",
    "private_key": PRIVATE_KEY,
    "client_email": "id-6neuf@stock-ergo.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com",
}

# --- CONNEXION ET CHARGEMENT ---
try:
    # On initialise la connexion au Google Sheet
    spread = Spread("11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8", config=creds)
    
    # Chargement des deux onglets
    df_stock = spread.sheet_to_df(sheet='stock', index=0).reset_index()
    df_hist = spread.sheet_to_df(sheet='historique', index=0).reset_index()
    
    # Conversion forcée de l'ID en nombre pour éviter les erreurs de calcul
    df_stock['id'] = pd.to_numeric(df_stock['id'], errors='coerce')
    
except Exception as e:
    st.error(f"Erreur d'initialisation : {e}")
    st.stop()

st.title("📦 Gestion de Stock Ergo")

# Navigation par onglets
tab1, tab2, tab3 = st.tabs(["📋 Inventaire", "🔄 Mouvements", "➕ Ajouter"])

# --- TAB 1 : INVENTAIRE ---
with tab1:
    st.subheader("État actuel du matériel")
    st.dataframe(df_stock, use_container_width=True, hide_index=True)

# --- TAB 2 : MOUVEMENTS (PRÊTS / RETOURS) ---
with tab2:
    st.subheader("Enregistrer un changement de statut")
    if not df_stock.empty:
        with st.form("form_mouvement"):
            article = st.selectbox("Sélectionner l'article", df_stock["nom"].unique())
            action = st.selectbox("Action", ["Prêt", "Retour", "Vente", "Mise au rebut"])
            note = st.text_input("Note (ex: Prêté à M. Dupont)")
            
            if st.form_submit_button("Enregistrer le mouvement"):
                # 1. Mise à jour du stock
                nouveaux_statuts = {"Prêt": "Prêté", "Retour": "Disponible", "Vente": "Vendu", "Mise au rebut": "Jeté"}
                df_stock.loc[df_stock["nom"] == article, "statut"] = nouveaux_statuts[action]
                spread.df_to_sheet(df_stock, sheet='stock', index=False, replace=True)
                
                # 2. Ajout à l'historique
                item_id = df_stock.loc[df_stock["nom"] == article, "id"].values[0]
                new_h = pd.DataFrame([{
                    "id_materiel": item_id,
                    "nom_article": article,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "action": action,
                    "notes": note
                }])
                df_hist = pd.concat([df_hist, new_h], ignore_index=True)
                spread.df_to_sheet(df_hist, sheet='historique', index=False, replace=True)
                
                st.success(f"Action '{action}' enregistrée !")
                st.rerun()
    else:
        st.info("Le stock est vide.")

# --- TAB 3 : AJOUTER UN ARTICLE ---
with tab3:
    st.subheader("Ajouter un nouveau matériel")
    with st.form("form_ajout"):
        nouveau_nom = st.text_input("Nom de l'article")
        prov = st.selectbox("Provenance", ["Achat", "Don", "Prêt fournisseur"])
        
        if st.form_submit_button("Ajouter à l'inventaire"):
            if nouveau_nom:
                next_id = int(df_stock["id"].max() + 1) if not df_stock.empty else 1
                new_item = pd.DataFrame([{
                    "id": next_id,
                    "nom": nouveau_nom,
                    "provenance": prov,
                    "options": "",
                    "statut": "Disponible"
                }])
                df_stock = pd.concat([df_stock, new_item], ignore_index=True)
                spread.df_to_sheet(df_stock, sheet='stock', index=False, replace=True)
                
                st.success(f"'{nouveau_nom}' a été ajouté !")
                st.rerun()

# --- HISTORIQUE EN BAS DE PAGE ---
st.divider()
st.subheader("📜 Historique des allers-retours")
if not df_hist.empty:
    st.dataframe(df_hist.sort_index(ascending=False), use_container_width=True, hide_index=True)
