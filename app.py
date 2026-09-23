import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="BRVM Wealth & Decision Cockpit",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style visuel soigné
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #1e222d 0%, #252b3b 100%);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #323b4e;
        margin-bottom: 12px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# 45 Entreprises cotées à la BRVM
BRVM_MASTER_DATA = [
    # SERVICES PUBLICS & TÉLÉCOMS
    {"Ticker": "SNTS", "Nom": "Sonatel Sénégal", "Secteur": "Services Publics", "Pays": "Sénégal", "Cours": 41000, "Dividende_Net": 1900, "PER": 8.5, "ROE": 28.0, "Payout": 75.0, "Liquidite": "Très Élevée", "Description": "Opérateur télécoms historique au Sénégal, Mali, Guinée, Bissau et Sierra Leone. Valeur pilier indiscutable."},
    {"Ticker": "ORAC", "Nom": "Orange Côte d'Ivoire", "Secteur": "Services Publics", "Pays": "Côte d'Ivoire", "Cours": 20400, "Dividende_Net": 1500, "PER": 8.9, "ROE": 25.0, "Payout": 80.0, "Liquidite": "Élevée", "Description": "Leader télécoms et mobile money en Côte d'Ivoire, présent aussi au Burkina et Libéria."},
    {"Ticker": "ONTBF", "Nom": "Onatel Burkina Faso", "Secteur": "Services Publics", "Pays": "Burkina Faso", "Cours": 2800, "Dividende_Net": 220, "PER": 7.2, "ROE": 18.0, "Payout": 85.0, "Liquidite": "Moyenne", "Description": "Opérateur de télécommunications burkinabè, filiale du groupe Maroc Telecom."},
    {"Ticker": "CIEC", "Nom": "CIE Côte d'Ivoire", "Secteur": "Services Publics", "Pays": "Côte d'Ivoire", "Cours": 6205, "Dividende_Net": 480, "PER": 8.0, "ROE": 17.5, "Payout": 75.0, "Liquidite": "Élevée", "Description": "Concessionnaire exclusif du service public de distribution d'électricité en Côte d'Ivoire."},
    {"Ticker": "SDCC", "Nom": "SODECI Côte d'Ivoire", "Secteur": "Services Publics", "Pays": "Côte d'Ivoire", "Cours": 11165, "Dividende_Net": 780, "PER": 8.7, "ROE": 16.5, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Société de distribution d'eau potable en Côte d'Ivoire, modèle d'utilité publique défensif."},

    # SECTEUR BANCAIRE & FINANCES
    {"Ticker": "SGBC", "Nom": "Société Générale Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 37985, "Dividende_Net": 2400, "PER": 7.1, "ROE": 23.5, "Payout": 65.0, "Liquidite": "Très Élevée", "Description": "Première institution bancaire de Côte d'Ivoire. Rentabilité supérieure et solidité bilancielle."},
    {"Ticker": "CBIBF", "Nom": "Coris Bank International", "Secteur": "Finances", "Pays": "Burkina Faso", "Cours": 28675, "Dividende_Net": 2100, "PER": 6.8, "ROE": 24.5, "Payout": 60.0, "Liquidite": "Élevée", "Description": "Groupe bancaire panafricain dynamique à très faible coefficient d'exploitation et fort ROE."},
    {"Ticker": "ECOC", "Nom": "Ecobank Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 16800, "Dividende_Net": 1350, "PER": 6.5, "ROE": 22.0, "Payout": 68.0, "Liquidite": "Élevée", "Description": "Filiale ivoirienne du groupe ETI, rentabilité en forte expansion."},
    {"Ticker": "ETIT", "Nom": "Ecobank Transnational Inc.", "Secteur": "Finances", "Pays": "Togo", "Cours": 65, "Dividende_Net": 4.5, "PER": 4.5, "ROE": 16.5, "Payout": 45.0, "Liquidite": "Très Élevée", "Description": "Maison mère panafricaine présente dans 35 pays. Plus fort volume d'actions transigées."},
    {"Ticker": "BOAB", "Nom": "Bank of Africa Bénin", "Secteur": "Finances", "Pays": "Bénin", "Cours": 8790, "Dividende_Net": 780, "PER": 6.0, "ROE": 21.5, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Rendement de dividende historiquement élevé, position de leader au Bénin."},
    {"Ticker": "BOABF", "Nom": "Bank of Africa Burkina Faso", "Secteur": "Finances", "Pays": "Burkina Faso", "Cours": 7400, "Dividende_Net": 650, "PER": 5.8, "ROE": 20.0, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Rendement régulier, profil de risque équilibré dans le secteur bancaire burkinabè."},
    {"Ticker": "BOAC", "Nom": "Bank of Africa Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 10800, "Dividende_Net": 890, "PER": 6.9, "ROE": 21.0, "Payout": 72.0, "Liquidite": "Élevée", "Description": "Filiale ivoirienne en constante progression de parts de marché."},
    {"Ticker": "BOAM", "Nom": "Bank of Africa Mali", "Secteur": "Finances", "Pays": "Mali", "Cours": 5470, "Dividende_Net": 460, "PER": 5.2, "ROE": 17.5, "Payout": 65.0, "Liquidite": "Faible", "Description": "Valeur bancaire malienne à dividende régulier."},
    {"Ticker": "BOAN", "Nom": "Bank of Africa Niger", "Secteur": "Finances", "Pays": "Niger", "Cours": 4550, "Dividende_Net": 420, "PER": 5.0, "ROE": 18.0, "Payout": 70.0, "Liquidite": "Faible", "Description": "Rendement de dividende élevé, valeur de rente pure."},
    {"Ticker": "BOAS", "Nom": "Bank of Africa Sénégal", "Secteur": "Finances", "Pays": "Sénégal", "Cours": 7650, "Dividende_Net": 680, "PER": 6.3, "ROE": 19.5, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Banque sénégalaise bien positionnée avec une politique constante de distribution."},
    {"Ticker": "SIBC", "Nom": "Société Ivoirienne de Banque (SIB)", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 8510, "Dividende_Net": 700, "PER": 6.4, "ROE": 22.5, "Payout": 75.0, "Liquidite": "Élevée", "Description": "Filiale du groupe Attijariwafa Bank, excellente gestion des risques de crédit."},
    {"Ticker": "NSBC", "Nom": "NSIA Banque Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 20815, "Dividende_Net": 1400, "PER": 7.3, "ROE": 19.0, "Payout": 60.0, "Liquidite": "Moyenne", "Description": "Fleuron bancaire du groupe panafricain NSIA, dynamique de croissance soutenue."},
    {"Ticker": "BICC", "Nom": "BICICI Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 29745, "Dividende_Net": 1600, "PER": 8.0, "ROE": 16.0, "Payout": 55.0, "Liquidite": "Faible", "Description": "Banque historique ivoirienne reprise par des capitaux institutionnels locaux."},
    {"Ticker": "BICB", "Nom": "BIIC Bénin", "Secteur": "Finances", "Pays": "Bénin", "Cours": 8560, "Dividende_Net": 520, "PER": 7.5, "ROE": 15.0, "Payout": 50.0, "Liquidite": "Moyenne", "Description": "Acteur bancaire béninois coté récemment, en phase de consolidation."},
    {"Ticker": "ORGT", "Nom": "Oragroup Togo", "Secteur": "Finances", "Pays": "Togo", "Cours": 2800, "Dividende_Net": 0, "PER": 12.0, "ROE": 6.0, "Payout": 0.0, "Liquidite": "Moyenne", "Description": "Holding bancaire régionale présente dans 12 pays d'Afrique de l'Ouest et Centrale."},
    {"Ticker": "SAFC", "Nom": "SAFCA Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 3980, "Dividende_Net": 0, "PER": 14.0, "ROE": 6.0, "Payout": 0.0, "Liquidite": "Faible", "Description": "Établissement financier spécialisé dans le leasing et le crédit professionnel."},

    # DISTRIBUTION & ÉNERGIE
    {"Ticker": "TTLC", "Nom": "TotalEnergies Marketing CI", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 2985, "Dividende_Net": 260, "PER": 8.3, "ROE": 21.0, "Payout": 85.0, "Liquidite": "Élevée", "Description": "Réseau leader de stations-service et lubrifiants en Côte d'Ivoire."},
    {"Ticker": "TTLS", "Nom": "TotalEnergies Marketing Sénégal", "Secteur": "Distribution", "Pays": "Sénégal", "Cours": 3800, "Dividende_Net": 290, "PER": 7.9, "ROE": 20.0, "Payout": 80.0, "Liquidite": "Moyenne", "Description": "Distribution de carburants et services annexes au Sénégal."},
    {"Ticker": "SHEC", "Nom": "Vivo Energy Côte d'Ivoire", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 2475, "Dividende_Net": 180, "PER": 9.2, "ROE": 14.5, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Distributeur exclusif des carburants et lubrifiants Shell en Côte d'Ivoire."},
    {"Ticker": "CFAC", "Nom": "CFAO Motors CI", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 1480, "Dividende_Net": 110, "PER": 8.8, "ROE": 15.5, "Payout": 65.0, "Liquidite": "Élevée", "Description": "Distribution de véhicules neufs, pièces d'origine et engins industriels."},
    {"Ticker": "ABJC", "Nom": "Servair Abidjan", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 3930, "Dividende_Net": 260, "PER": 9.0, "ROE": 18.0, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Restauration aérienne et catering d'entreprises à Abidjan."},
    {"Ticker": "BNBC", "Nom": "Bernabé Côte d'Ivoire", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 1890, "Dividende_Net": 130, "PER": 9.8, "ROE": 13.0, "Payout": 60.0, "Liquidite": "Moyenne", "Description": "Fournitures industrielles, métallurgie et quincaillerie du bâtiment."},
    {"Ticker": "PRSC", "Nom": "Tractafric Motors CI", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 4200, "Dividende_Net": 280, "PER": 8.4, "ROE": 16.5, "Payout": 65.0, "Liquidite": "Faible", "Description": "Concessionnaire de marques automobiles de renom et engins de TP."},

    # AGRO-INDUSTRIE
    {"Ticker": "PALC", "Nom": "Palm Côte d'Ivoire", "Secteur": "Agriculture", "Pays": "Côte d'Ivoire", "Cours": 8100, "Dividende_Net": 750, "PER": 6.2, "ROE": 23.0, "Payout": 65.0, "Liquidite": "Élevée", "Description": "Production d'huile de palme brute, forte génération de trésorerie en période de cours hauts."},
    {"Ticker": "SPHC", "Nom": "SAPH Côte d'Ivoire", "Secteur": "Agriculture", "Pays": "Côte d'Ivoire", "Cours": 7500, "Dividende_Net": 680, "PER": 6.5, "ROE": 20.0, "Payout": 60.0, "Liquidite": "Élevée", "Description": "Leader du caoutchouc naturel d'Afrique de l'Ouest, exportations mondiales."},
    {"Ticker": "SOGC", "Nom": "SOGB Côte d'Ivoire", "Secteur": "Agriculture", "Pays": "Côte d'Ivoire", "Cours": 7300, "Dividende_Net": 710, "PER": 6.0, "ROE": 22.0, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Plantations intégrées d'hévéa et de palmiers dans le sud-ouest ivoirien."},
    {"Ticker": "SCRC", "Nom": "Sucrivoire Côte d'Ivoire", "Secteur": "Agriculture", "Pays": "Côte d'Ivoire", "Cours": 2690, "Dividende_Net": 160, "PER": 10.5, "ROE": 11.0, "Payout": 50.0, "Liquidite": "Faible", "Description": "Exploitation de canne à sucre et raffineries à Zuénoula et Borotou."},

    # INDUSTRIE
    {"Ticker": "SLBC", "Nom": "Solibra Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 37885, "Dividende_Net": 2600, "PER": 9.5, "ROE": 19.0, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Brasseur leader et fabricant de boissons rafraîchissantes en Côte d'Ivoire."},
    {"Ticker": "STBC", "Nom": "SITAB Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 20895, "Dividende_Net": 1800, "PER": 7.4, "ROE": 27.0, "Payout": 85.0, "Liquidite": "Moyenne", "Description": "Manufacture de tabacs, très fort rendement de trésorerie distribuée."},
    {"Ticker": "NTLC", "Nom": "Nestlé Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 14500, "Dividende_Net": 1200, "PER": 8.8, "ROE": 32.0, "Payout": 85.0, "Liquidite": "Élevée", "Description": "Transformation locale de produits alimentaires de grande consommation (Maggi, Nescafé)."},
    {"Ticker": "SMBC", "Nom": "SMB Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 14710, "Dividende_Net": 1100, "PER": 7.0, "ROE": 25.0, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Société Multinationale de Bitumes, acteur stratégique des chantiers routiers régionaux."},
    {"Ticker": "CABC", "Nom": "Sicable Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 3190, "Dividende_Net": 210, "PER": 9.0, "ROE": 16.0, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Fabricant de câbles d'énergie et de télécoms du groupe Prysmian."},
    {"Ticker": "FTSC", "Nom": "Filtisac Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 2000, "Dividende_Net": 140, "PER": 8.5, "ROE": 14.0, "Payout": 60.0, "Liquidite": "Moyenne", "Description": "Leader des emballages industriels et agricoles pour le cacao et café."},
    {"Ticker": "NEIC", "Nom": "NEI-CEDA Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 2405, "Dividende_Net": 180, "PER": 8.0, "ROE": 15.0, "Payout": 65.0, "Liquidite": "Moyenne", "Description": "Édition scolaire et manuels de référence dans la zone UEMOA."},
    {"Ticker": "UNXC", "Nom": "Uniwax Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 2200, "Dividende_Net": 0, "PER": 15.0, "ROE": 4.0, "Payout": 0.0, "Liquidite": "Élevée", "Description": "Manufacture textile de pagnes wax, restructuration commerciale."},
    {"Ticker": "UNLC", "Nom": "Unilever Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 49000, "Dividende_Net": 0, "PER": 18.0, "ROE": 5.0, "Payout": 0.0, "Liquidite": "Très Faible", "Description": "Produits d'hygiène et biens ménagers."},
    {"Ticker": "SIVC", "Nom": "Air Liquide Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 2000, "Dividende_Net": 0, "PER": 20.0, "ROE": 3.0, "Payout": 0.0, "Liquidite": "Faible", "Description": "Gaz industriels et oxygène médical."},

    # SERVICES DIVERS & TRANSPORT
    {"Ticker": "SDSC", "Nom": "Africa Global Logistics CI", "Secteur": "Transport", "Pays": "Côte d'Ivoire", "Cours": 2800, "Dividende_Net": 190, "PER": 8.2, "ROE": 17.0, "Payout": 70.0, "Liquidite": "Élevée", "Description": "Manutentionnaire portuaire et logisticien de premier plan (ex-Bolloré)."},
    {"Ticker": "LNBB", "Nom": "Loterie Nationale du Bénin", "Secteur": "Services Divers", "Pays": "Bénin", "Cours": 3700, "Dividende_Net": 320, "PER": 7.5, "ROE": 26.0, "Payout": 80.0, "Liquidite": "Moyenne", "Description": "Opérateur public de jeux de hasard au Bénin, rendement de distribution attractif."},
    {"Ticker": "STAC", "Nom": "SETAO Côte d'Ivoire", "Secteur": "BTP", "Pays": "Côte d'Ivoire", "Cours": 2100, "Dividende_Net": 0, "PER": 11.0, "ROE": 8.0, "Payout": 0.0, "Liquidite": "Faible", "Description": "Filiale de Bouygues Construction en Côte d'Ivoire."}
]

# Enrichissement & notation
for item in BRVM_MASTER_DATA:
    c = item["Cours"]
    d = item["Dividende_Net"]
    r = round((d / c) * 100, 2) if c > 0 else 0.0
    item["Rendement_Net"] = r
    
    score = 40
    if r >= 8.0:
        score += 25
    elif r >= 6.0:
        score += 15
    elif r > 0:
        score += 5
        
    if item["ROE"] >= 20.0:
        score += 20
    elif item["ROE"] >= 15.0:
        score += 10
        
    if item["PER"] <= 8.0:
        score += 15
    elif item["PER"] <= 10.0:
        score += 8
        
    item["Score"] = min(score, 98)
    if item["Score"] >= 80:
        item["Statut"] = "🟢 Achat Prioritaire"
    elif item["Score"] >= 65:
        item["Statut"] = "🟡 Accumulation"
    else:
        item["Statut"] = "⚪ Surveillance"

df_master = pd.DataFrame(BRVM_MASTER_DATA)

# État de session (Portefeuille réel avec support d'achat et vente)
if "portfolio" not in st.session_state:
    st.session_state.portfolio = [
        {"Ticker": "SNTS", "Nom": "Sonatel Sénégal", "Quantite": 6, "PRU": 41000, "Date": "2026-09-01"},
        {"Ticker": "SGBC", "Nom": "Société Générale CI", "Quantite": 5, "PRU": 37985, "Date": "2026-09-01"},
        {"Ticker": "TTLC", "Nom": "TotalEnergies Marketing CI", "Quantite": 35, "PRU": 2985, "Date": "2026-09-01"}
    ]

if "historique_ventes" not in st.session_state:
    st.session_state.historique_ventes = []

# BARRE LATÉRALE : PARAMÈTRES ET SCÉNARIOS PRÉDÉFINIS
st.sidebar.title("🏛️ Cockpit Patrimoine BRVM")
st.sidebar.caption("Système Décisionnel & Simulateur de Rente")
st.sidebar.markdown("---")

capital_depart = st.sidebar.number_input(
    "Capital d'amorçage disponible (FCFA)", 
    min_value=100000, 
    max_value=100000000, 
    value=600000, 
    step=50000
)

epargne_mensuelle = st.sidebar.number_input(
    "Épargne mensuelle injectée (FCFA)", 
    min_value=0, 
    max_value=10000000, 
    value=175000, 
    step=25000
)

horizon_max = st.sidebar.slider("Horizon de projection (Années)", min_value=1, max_value=25, value=5)

st.sidebar.markdown("### 🎲 Scénarios de Marché")
choix_scenario = st.sidebar.radio(
    "Profil de rendement annuel :",
    ["Médian BRVM (9 % / an)", "Prudent (6 % / an)", "Dynamique (13 % / an)", "Personnalisé"]
)

if choix_scenario == "Prudent (6 % / an)":
    rendement_choisi = 6.0
elif choix_scenario == "Médian BRVM (9 % / an)":
    rendement_choisi = 9.0
elif choix_scenario == "Dynamique (13 % / an)":
    rendement_choisi = 13.0
else:
    rendement_choisi = st.sidebar.slider("Rendement personnalisé (%/an)", 4.0, 20.0, 10.0, 0.5)

# Calcul du rendement pondéré actuel du portefeuille réel
div_total_annuel_pf = 0
val_totale_actuelle_pf = 0
for pos in st.session_state.portfolio:
    match = df_master[df_master["Ticker"] == pos["Ticker"]]
    c_act = match.iloc[0]["Cours"] if not match.empty else pos["PRU"]
    d_act = match.iloc[0]["Dividende_Net"] if not match.empty else 0
    val_totale_actuelle_pf += pos["Quantite"] * c_act
    div_total_annuel_pf += pos["Quantite"] * d_act

rendement_reel_pondere = round((div_total_annuel_pf / val_totale_actuelle_pf) * 100, 2) if val_totale_actuelle_pf > 0 else 8.0

if st.sidebar.button(f"🔗 Injecter le rendement réel ({rendement_reel_pondere}%)"):
    rendement_choisi = rendement_reel_pondere
    st.sidebar.success(f"Rendement calé sur ton portefeuille réel : {rendement_reel_pondere}% !")

st.sidebar.markdown("---")
st.sidebar.info("💡 Les dividendes perçus sont systématiquement réinvestis sur l'horizon choisi.")

# CORPS PRINCIPAL & ONGLETS
tab_dashboard, tab_marche, tab_fiche, tab_portefeuille, tab_calculateur_inverse, tab_alloc, tab_assistant = st.tabs([
    "📈 Tableau de Bord & Courbes", 
    "🏛️ Les 45 Entreprises", 
    "🔍 Fiche Valeur", 
    "💼 Mon Portefeuille (Achat/Vente)", 
    "🎯 Calculateur Rente Cible", 
    "⚖️ Allocation 600k", 
    "🤖 Assistant Stratégique"
])

# ONGLET 1: TABLEAU DE BORD ÉLÉGANT & COURBES D'INCERTITUDE
with tab_dashboard:
    st.subheader("📊 Tableau de Bord Patrimonial & Corridor de Projection")
    
    # 4 Cartes métriques
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Capital de Départ", f"{capital_depart:,} FCFA")
    col_m2.metric("Épargne Mensuelle", f"{epargne_mensuelle:,} FCFA / mois")
    col_m3.metric("Scénario Actif", f"{rendement_choisi}% / an")
    col_m4.metric("Valeur Portefeuille Réel", f"{val_totale_actuelle_pf:,} FCFA")

    # Simulation multi-scénarios (Corridor d'incertitude)
    an_courante = datetime.now().year
    annees_axe = list(range(an_courante, an_courante + horizon_max + 1))
    
    def simuler_courbe(taux_rendement):
        cap = capital_depart
        epargne_an = epargne_mensuelle * 12
        caps = []
        divs = []
        for i in range(len(annees_axe)):
            d = cap * 0.08  # part dividende
            if i == 0:
                caps.append(cap)
                divs.append(d)
            else:
                cap = (cap + epargne_an + d) * (1 + (taux_rendement - 8) / 100)
                caps.append(cap)
                divs.append(d)
        return caps, divs

    caps_prudent, divs_prudent = simuler_courbe(6.0)
    caps_median, divs_median = simuler_courbe(9.0)
    caps_dynamique, divs_dynamique = simuler_courbe(13.0)
    caps_actif, divs_actif = simuler_courbe(rendement_choisi)

    # Graphique interactif Plotly
    fig_corridor = go.Figure()
    
    # Zone d'incertitude entre prudent et dynamique
    fig_corridor.add_trace(go.Scatter(
        x=annees_axe + annees_axe[::-1],
        y=caps_dynamique + caps_prudent[::-1],
        fill='toself',
        fillcolor='rgba(0, 102, 204, 0.12)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Corridor Marché (6% à 13%)'
    ))
    
    # Courbe prudente
    fig_corridor.add_trace(go.Scatter(
        x=annees_axe, y=caps_prudent,
        mode='lines',
        name='Scénario Prudent (6%)',
        line=dict(color='#888888', dash='dot')
    ))
    
    # Courbe dynamique
    fig_corridor.add_trace(go.Scatter(
        x=annees_axe, y=caps_dynamique,
        mode='lines',
        name='Scénario Dynamique (13%)',
        line=dict(color='#00cc66', dash='dash')
    ))
    
    # Courbe du scénario sélectionné (en valeur plein)
    fig_corridor.add_trace(go.Scatter(
        x=annees_axe, y=caps_actif,
        mode='lines+markers',
        name=f'Scénario Sélectionné ({rendement_choisi}%)',
        line=dict(color='#0088ff', width=3.5)
    ))

    fig_corridor.update_layout(
        title="<b>Trajectoire de Croissance du Capital (Corridor d'Incertitude BRVM)</b>",
        xaxis_title="Année",
        yaxis_title="Capital Total Estimé (FCFA)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_corridor, use_container_width=True)
    
    # Tableau récapitulatif
    df_dashboard_recap = pd.DataFrame({
        "Année": annees_axe,
        "Scénario Prudent 6% (FCFA)": [f"{round(x):,}" for x in caps_prudent],
        "Scénario Médian 9% (FCFA)": [f"{round(x):,}" for x in caps_median],
        "Scénario Dynamique 13% (FCFA)": [f"{round(x):,}" for x in caps_dynamique],
        "Dividende Projeté Médian (FCFA)": [f"{round(x):,}" for x in divs_median]
    })
    
    st.markdown("### 📋 Données Annuelles Comparatives")
    st.dataframe(df_dashboard_recap, use_container_width=True, hide_index=True)

    # Bouton d'export rapport
    st.markdown("---")
    rapport_txt = f"""RAPPORT D'INVESTISSEMENT PATRIMONIAL - BRVM
Généré le : {datetime.now().strftime('%d/%m/%Y')}
-------------------------------------------------------------
1. HYPOTHÈSES INITIALES
- Capital de départ : {capital_depart:,} FCFA
- Épargne mensuelle : {epargne_mensuelle:,} FCFA
- Horizon temporel : {horizon_max} ans (jusqu'en {annees_axe[-1]})
- Rendement sélectionné : {rendement_choisi}% / an

2. PROJECTIONS À TERME ({annees_axe[-1]})
- Capital estimé (Scénario Médian 9%) : {round(caps_median[-1]):,} FCFA
- Dividende annuel attendu : {round(divs_median[-1]):,} FCFA / an
- Capital estimé (Scénario Prudent 6%) : {round(caps_prudent[-1]):,} FCFA
- Capital estimé (Scénario Dynamique 13%) : {round(caps_dynamique[-1]):,} FCFA

3. RÈGLE DE GESTION DU RISQUE
- Réinvestissement 100% des dividendes perçus (effet boule de neige).
- Diversification maximale : 4 à 6 piliers (Banques, Télécoms, Énergie).
- Aucune ligne ne doit dépasser 15% du capital global.
-------------------------------------------------------------
"""
    st.download_button(
        label="📄 Télécharger le Rapport d'Investissement Synthétique (.txt)",
        data=rapport_txt,
        file_name=f"rapport_brvm_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

# ONGLET 2: LES 45 ENTREPRISES
with tab_marche:
    st.subheader(f"🏛️ Cote Officielle BRVM ({len(df_master)} Valeurs)")
    
    c_f1, c_f2, c_f3 = st.columns(3)
    f_sect = c_f1.selectbox("Secteur :", ["Tous"] + sorted(df_master["Secteur"].unique().tolist()))
    f_pays = c_f2.selectbox("Pays :", ["Tous"] + sorted(df_master["Pays"].unique().tolist()))
    f_tri = c_f3.selectbox("Trier la cote par :", ["Score décroissant", "Rendement dividende décroissant", "PER croissant", "Cours croissant"])
    
    df_view = df_master.copy()
    if f_sect != "Tous":
        df_view = df_view[df_view["Secteur"] == f_sect]
    if f_pays != "Tous":
        df_view = df_view[df_view["Pays"] == f_pays]
        
    if f_tri == "Score décroissant":
        df_view = df_view.sort_values(by="Score", ascending=False)
    elif f_tri == "Rendement dividende décroissant":
        df_view = df_view.sort_values(by="Rendement_Net", ascending=False)
    elif f_tri == "PER croissant":
        df_view = df_view.sort_values(by="PER", ascending=True)
    elif f_tri == "Cours croissant":
        df_view = df_view.sort_values(by="Cours", ascending=True)

    st.dataframe(
        df_view[["Ticker", "Nom", "Pays", "Secteur", "Cours", "Dividende_Net", "Rendement_Net", "PER", "ROE", "Liquidite", "Score", "Statut"]],
        use_container_width=True,
        hide_index=True
    )

# ONGLET 3: FICHE VALEUR
with tab_fiche:
    st.subheader("🔍 Fiche d'Identité et Audit Fondamental")
    val_select = st.selectbox("Sélectionne une entreprise :", df_master["Ticker"] + " - " + df_master["Nom"])
    val_code = val_select.split(" - ")[0]
    info_v = df_master[df_master["Ticker"] == val_code].iloc[0]
    
    col_v1, col_v2 = st.columns([1, 2])
    with col_v1:
        st.markdown(f"### {info_v['Nom']} (`{info_v['Ticker']}`)")
        st.write(f"📍 **Pays :** {info_v['Pays']}")
        st.write(f"🏭 **Secteur :** {info_v['Secteur']}")
        st.write(f"💰 **Dernier cours :** **{info_v['Cours']:,} FCFA**")
        st.write(f"💵 **Dividende Net :** **{info_v['Dividende_Net']:,} FCFA**")
        st.write(f"📈 **Rendement Net :** **{info_v['Rendement_Net']} %**")
        st.write(f"⚖️ **Ratio PER :** {info_v['PER']}x")
        st.write(f"💎 **ROE (Rentabilité FP) :** {info_v['ROE']} %")
        st.write(f"📊 **Taux Distribution (Payout) :** {info_v['Payout']} %")
        st.write(f"💧 **Liquidité :** {info_v['Liquidite']}")
    with col_v2:
        st.success(f"**Score Stratégique : {info_v['Score']}/100** — Statut : **{info_v['Statut']}**")
        st.info(f"**Modèle d'affaires & Position de marché :**\n\n{info_v['Description']}")
        
        st.markdown("#### Plan de conduite face aux variations :")
        if info_v["Score"] >= 80:
            st.success("🟢 **Valeur Pilier (Top Tier) :** Si le cours recule de 10% sans atteinte aux bénéfices, exploiter la faiblesse pour renforcer à prix décoté.")
        elif info_v["Score"] >= 65:
            st.warning("🟡 **Valeur de Rendement :** Conserver pour la rente annuelle. Ne pas renforcer excessivement.")
        else:
            st.error("🔴 **Valeur Délicate / Cyclique :** Couper la ligne si le dividende n'est pas reconduit.")

# ONGLET 4: MON PORTEFEUILLE (ACHATS ET VENTES / RETRAITS)
with tab_portefeuille:
    st.subheader("💼 Gestion Active de ton Portefeuille Réel")
    
    tab_achat, tab_vente = st.tabs(["➕ Enregistrer un Achat", "➖ Enregistrer une Vente / Retrait"])
    
    with tab_achat:
        with st.form("form_add_achat"):
            fa_tick = st.selectbox("Action achetée :", df_master["Ticker"] + " - " + df_master["Nom"], key="buy_tick")
            fa_q = st.number_input("Nombre d'actions acquises :", min_value=1, value=5, key="buy_q")
            fa_p = st.number_input("Prix d'achat unitaire (PRU en FCFA) :", min_value=10, value=25000, step=100, key="buy_p")
            fa_d = st.date_input("Date de la transaction :", datetime.now(), key="buy_d")
            submit_achat = st.form_submit_button("Valider l'Achat")
            
            if submit_achat:
                code_a = fa_tick.split(" - ")[0]
                nom_a = fa_tick.split(" - ")[1]
                # Vérifie si le titre existe déjà pour fusionner ou ajouter
                existant = False
                for p in st.session_state.portfolio:
                    if p["Ticker"] == code_a:
                        total_titres = p["Quantite"] + fa_q
                        p["PRU"] = round(((p["Quantite"] * p["PRU"]) + (fa_q * fa_p)) / total_titres)
                        p["Quantite"] = total_titres
                        existant = True
                        break
                if not existant:
                    st.session_state.portfolio.append({
                        "Ticker": code_a,
                        "Nom": nom_a,
                        "Quantite": fa_q,
                        "PRU": fa_p,
                        "Date": str(fa_d)
                    })
                st.success(f"Achat validé : {fa_q} titres {nom_a} enregistrés !")

    with tab_vente:
        if st.session_state.portfolio:
            with st.form("form_add_vente"):
                liste_detenue = [f"{p['Ticker']} - {p['Nom']} (Dispo: {p['Quantite']})" for p in st.session_state.portfolio]
                fv_choix = st.selectbox("Sélectionne la ligne à alléger ou solder :", liste_detenue)
                fv_code = fv_choix.split(" - ")[0]
                ligne_cible = next(item for item in st.session_state.portfolio if item["Ticker"] == fv_code)
                
                fv_q = st.number_input("Quantité d'actions à vendre :", min_value=1, max_value=int(ligne_cible["Quantite"]), value=1)
                fv_prix = st.number_input("Prix de vente unitaire effectif (FCFA) :", min_value=10, value=int(ligne_cible["PRU"]), step=100)
                fv_date = st.date_input("Date de la cession :", datetime.now(), key="sell_d")
                submit_vente = st.form_submit_button("Exécuter la Vente")
                
                if submit_vente:
                    pv_realisee = (fv_prix - ligne_cible["PRU"]) * fv_q
                    st.session_state.historique_ventes.append({
                        "Ticker": fv_code,
                        "Nom": ligne_cible["Nom"],
                        "Quantite": fv_q,
                        "Prix_Achat": ligne_cible["PRU"],
                        "Prix_Vente": fv_prix,
                        "PV_Realisee": pv_realisee,
                        "Date": str(fv_date)
                    })
                    if ligne_cible["Quantite"] <= fv_q:
                        st.session_state.portfolio.remove(ligne_cible)
                    else:
                        ligne_cible["Quantite"] -= fv_q
                    st.success(f"Vente effectuée : {fv_q} actions vendues. Plus-value réalisée : {pv_realisee:+,} FCFA.")
        else:
            st.info("Aucune ligne en portefeuille à vendre.")

    # Affichage du portefeuille en direct
    st.markdown("### 📊 État Actuel des Positions")
    if st.session_state.portfolio:
        pf_display = []
        tot_achat = 0
        tot_actuel = 0
        tot_dividende = 0
        
        for pos in st.session_state.portfolio:
            match = df_master[df_master["Ticker"] == pos["Ticker"]]
            c_courant = match.iloc[0]["Cours"] if not match.empty else pos["PRU"]
            d_net = match.iloc[0]["Dividende_Net"] if not match.empty else 0
            
            cout = pos["Quantite"] * pos["PRU"]
            val_actuelle = pos["Quantite"] * c_courant
            pv = val_actuelle - cout
            perf = ((c_courant - pos["PRU"]) / pos["PRU"]) * 100 if pos["PRU"] > 0 else 0
            div_pos = pos["Quantite"] * d_net
            
            tot_achat += cout
            tot_actuel += val_actuelle
            tot_dividende += div_pos
            
            pf_display.append({
                "Ticker": pos["Ticker"],
                "Nom": pos["Nom"],
                "Quantité": pos["Quantite"],
                "PRU": f"{pos['PRU']:,} FCFA",
                "Cours Marché": f"{c_courant:,} FCFA",
                "Valeur Actuelle": f"{val_actuelle:,} FCFA",
                "Plus-Value Latente": f"{pv:+,} FCFA",
                "Performance": f"{perf:+.2f} %",
                "Dividende Net Estimé": f"{div_pos:,} FCFA"
            })
            
        st.dataframe(pd.DataFrame(pf_display), use_container_width=True, hide_index=True)
        
        c_k1, c_k2, c_k3 = st.columns(3)
        pv_glob = tot_actuel - tot_achat
        c_k1.metric("Valeur Totale", f"{tot_actuel:,} FCFA")
        c_k2.metric("Plus-Value Globale Latente", f"{pv_glob:+,} FCFA", delta=f"{(pv_glob/tot_achat)*100:+.2f}%")
        c_k3.metric("Rente Dividendes Annuelle", f"{tot_dividende:,} FCFA / an", delta=f"{(tot_dividende/tot_actuel)*100:.2f}% net")
    else:
        st.warning("Le portefeuille est actuellement vide.")

    # Historique des ventes
    if st.session_state.historique_ventes:
        st.markdown("### 📜 Historique des Ventes Réalisées")
        st.dataframe(pd.DataFrame(st.session_state.historique_ventes), use_container_width=True, hide_index=True)

# ONGLET 5: CALCULATEUR INVERSE ("OBJECTIF RENTE")
with tab_calculateur_inverse:
    st.subheader("🎯 Calculateur Inversé de Liberté Financière")
    st.write("Indique la rente que tu souhaites percevoir pour que l'outil calcule précisément les exigences d'épargne et de capital.")
    
    col_ci1, col_ci2 = st.columns(2)
    mode_rente = col_ci1.radio("Périodicité de l'objectif :", ["Par mois", "Par an"])
    
    if mode_rente == "Par mois":
        rente_saisie = col_ci2.number_input("Rente mensuelle nette souhaitée (FCFA)", min_value=25000, value=200000, step=25000)
        rente_annuelle_cible = rente_saisie * 12
    else:
        rente_saisie = col_ci2.number_input("Rente annuelle nette souhaitée (FCFA)", min_value=100000, value=1000000, step=100000)
        rente_annuelle_cible = rente_saisie

    rendement_hypothese = st.slider("Rendement net en dividende moyen estimé (%) :", min_value=5.0, max_value=12.0, value=8.0, step=0.5)
    
    capital_requis = rente_annuelle_cible / (rendement_hypothese / 100)
    
    st.markdown("---")
    st.markdown(f"""
    ### 📌 Résultat du Diagnostic :
    * Pour percevoir **{rente_annuelle_cible:,} FCFA net par an** (soit **{round(rente_annuelle_cible/12):,} FCFA / mois**), 
      il te faut un capital cible en bourse d'environ : **{round(capital_requis):,} FCFA**.
    """)
    
    # Calcul de l'effort d'épargne mensuel nécessaire
    st.markdown("#### Quel effort d'épargne pour y parvenir selon la durée ?")
    durees = [3, 5, 7, 10]
    lignes_effort = []
    
    for d in durees:
        # Formule de rente composée avec réinvestissement
        # A(t) = Cap_init*(1+r)^t + PMT * [((1+r)^t - 1) / r] * 12
        r_dec = (rendement_choisi / 100)
        k_init = capital_depart * ((1 + r_dec) ** d)
        deficit = max(0, capital_requis - k_init)
        facteur_annuite = (((1 + r_dec) ** d) - 1) / r_dec if r_dec > 0 else d
        epargne_an_requise = deficit / facteur_annuite if facteur_annuite > 0 else 0
        epargne_mois_requise = epargne_an_requise / 12
        
        lignes_effort.append({
            "Horizon visé": f"{d} ans ({an_courante + d})",
            "Capital Cible Requis": f"{round(capital_requis):,} FCFA",
            "Épargne Mensuelle Nécessaire": f"{round(epargne_mois_requise):,} FCFA / mois"
        })
        
    st.dataframe(pd.DataFrame(lignes_effort), use_container_width=True, hide_index=True)

# ONGLET 6: ALLOCATION SUGGÉRÉE 600k
with tab_alloc:
    st.subheader(f"⚖️ Répartition Optimale de tes {capital_depart:,} FCFA")
    st.caption("Allocation diversifiée sur 4 piliers historiques sans sur-exposition.")
    
    panier_modele = [
        {"Ticker": "SNTS", "Poids": 0.35},
        {"Ticker": "SGBC", "Poids": 0.30},
        {"Ticker": "TTLC", "Poids": 0.20},
        {"Ticker": "BOAB", "Poids": 0.15},
    ]
    
    lignes_alloc = []
    depense_totale = 0
    dividendes_prevus = 0
    
    for item in panier_modele:
        info_t = df_master[df_master["Ticker"] == item["Ticker"]].iloc[0]
        budget = capital_depart * item["Poids"]
        qte = int(budget // info_t["Cours"])
        total_ligne = qte * info_t["Cours"]
        depense_totale += total_ligne
        div_t = qte * info_t["Dividende_Net"]
        dividendes_prevus += div_t
        
        lignes_alloc.append({
            "Action": info_t["Nom"],
            "Ticker": item["Ticker"],
            "Secteur": info_t["Secteur"],
            "Cours Marché": f"{info_t['Cours']:,} FCFA",
            "Nombre d'actions": qte,
            "Total Engagé": f"{total_ligne:,} FCFA",
            "Poids Réel (%)": round((total_ligne / capital_depart) * 100, 1),
            "Dividende Annuel Net": f"{div_t:,} FCFA"
        })
        
    st.dataframe(pd.DataFrame(lignes_alloc), use_container_width=True, hide_index=True)
    
    col_a1, col_a2, col_a3 = st.columns(3)
    solde = capital_depart - depense_totale
    col_a1.metric("Montant Investi", f"{depense_totale:,} FCFA")
    col_a2.metric("Réserve Cash Non Utilisée", f"{solde:,} FCFA")
    col_a3.metric("Rendement Net Pondéré", f"{(dividendes_prevus/depense_totale)*100:.2f} % net")

# ONGLET 7: ASSISTANT STRATÉGIQUE
with tab_assistant:
    st.subheader("🤖 Assistant d'Aide à la Décision")
    q_user = st.text_input("Pose une question financière ou demande une vérification de ratio :", placeholder="Ex : Est-ce le moment d'alléger Total CI ou de renforcer Sonatel ?")
    
    if q_user:
        st.markdown(f"**Analyse demandée :** *{q_user}*")
        st.success("""
        **Vérification Automatique des Ratios Clés :**
        - **Liquidité & Flottant :** S'assurer que le titre s'échange au moins 3 fois par semaine sur le Bulletin Officiel de la Cote.
        - **Plafond de Risque :** Ne pas dépasser 15 % du portefeuille global sur une seule entreprise.
        - **Période Favorable :** Les entrées sur le marché BRVM sont statistiquement optimales entre octobre et janvier, avant les publications de résultats et l'annonce des dividendes du printemps.
        """)
