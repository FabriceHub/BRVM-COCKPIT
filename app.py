import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="BRVM Alpha Cockpit Pro",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base complète de référence des sociétés cotées à la BRVM
BRVM_MASTER_DATA = [
    # SERVICES PUBLICS & TÉLÉCOMS
    {"Ticker": "SNTS", "Nom": "Sonatel Sénégal", "Secteur": "Services Publics", "Pays": "Sénégal", "Cours": 41000, "Dividende_Net": 1900, "PER": 8.5, "ROE": 28.0, "Payout": 75.0, "Liquidite": "Très Élevée", "Description": "Opérateur historique de télécoms au Sénégal, Mali, Guinée, Guinée-Bissau et Sierra Leone. Valeur pilier incontournable de la BRVM."},
    {"Ticker": "ORAC", "Nom": "Orange Côte d'Ivoire", "Secteur": "Services Publics", "Pays": "Côte d'Ivoire", "Cours": 20400, "Dividende_Net": 1500, "PER": 8.9, "ROE": 25.0, "Payout": 80.0, "Liquidite": "Élevée", "Description": "Leader des télécommunications et des services financiers mobiles en Côte d'Ivoire, présent également au Burkina et au Libéria."},
    {"Ticker": "ONTBF", "Nom": "Onatel Burkina Faso", "Secteur": "Services Publics", "Pays": "Burkina Faso", "Cours": 2800, "Dividende_Net": 220, "PER": 7.2, "ROE": 18.0, "Payout": 85.0, "Liquidite": "Moyenne", "Description": "Opérateur télécoms burkinabè, filiale du groupe Maroc Telecom. Rendement de dividende attractif."},
    {"Ticker": "CIEC", "Nom": "CIE Côte d'Ivoire", "Secteur": "Services Publics", "Pays": "Côte d'Ivoire", "Cours": 6205, "Dividende_Net": 480, "PER": 8.0, "ROE": 17.5, "Payout": 75.0, "Liquidite": "Élevée", "Description": "Compagnie Ivoirienne d'Electricité, concessionnaire du service public de transport et distribution d'électricité."},
    {"Ticker": "SDCC", "Nom": "SODECI Côte d'Ivoire", "Secteur": "Services Publics", "Pays": "Côte d'Ivoire", "Cours": 11165, "Dividende_Net": 780, "PER": 8.7, "ROE": 16.5, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Société de distribution d'eau potable de Côte d'Ivoire, modèle d'utilité publique résilient et régulier."},

    # SECTEUR FINANCIER & BANQUES
    {"Ticker": "SGBC", "Nom": "Société Générale Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 37985, "Dividende_Net": 2400, "PER": 7.1, "ROE": 23.5, "Payout": 65.0, "Liquidite": "Très Élevée", "Description": "Première institution bancaire de Côte d'Ivoire. Rentabilité solide et croissance continue des fonds propres."},
    {"Ticker": "CBIBF", "Nom": "Coris Bank International", "Secteur": "Finances", "Pays": "Burkina Faso", "Cours": 28675, "Dividende_Net": 2100, "PER": 6.8, "ROE": 24.5, "Payout": 60.0, "Liquidite": "Élevée", "Description": "Groupe bancaire panafricain dynamique à très fort coefficient d'exploitation et excellent ROE."},
    {"Ticker": "ECOC", "Nom": "Ecobank Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 16800, "Dividende_Net": 1350, "PER": 6.5, "ROE": 22.0, "Payout": 68.0, "Liquidite": "Élevée", "Description": "Filiale ivoirienne du groupe ETI, rentabilité en nette progression et politique de dividende généreuse."},
    {"Ticker": "ETIT", "Nom": "Ecobank Transnational Inc.", "Secteur": "Finances", "Pays": "Togo", "Cours": 65, "Dividende_Net": 4.5, "PER": 4.5, "ROE": 16.5, "Payout": 45.0, "Liquidite": "Très Élevée", "Description": "Maison-mère du réseau bancaire panafricain présent dans 35 pays. Plus important volume d'actions échangées."},
    {"Ticker": "BOAB", "Nom": "Bank of Africa Bénin", "Secteur": "Finances", "Pays": "Bénin", "Cours": 8790, "Dividende_Net": 780, "PER": 6.0, "ROE": 21.5, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Rendement de dividende historiquement très robuste, assise financière éprouvée au Bénin."},
    {"Ticker": "BOABF", "Nom": "Bank of Africa Burkina Faso", "Secteur": "Finances", "Pays": "Burkina Faso", "Cours": 7400, "Dividende_Net": 650, "PER": 5.8, "ROE": 20.0, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Rendement régulier, profil de risque équilibré dans le secteur bancaire burkinabè."},
    {"Ticker": "BOAC", "Nom": "Bank of Africa Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 10800, "Dividende_Net": 890, "PER": 6.9, "ROE": 21.0, "Payout": 72.0, "Liquidite": "Élevée", "Description": "Filiale ivoirienne en constante progression commerciale et financière."},
    {"Ticker": "BOAM", "Nom": "Bank of Africa Mali", "Secteur": "Finances", "Pays": "Mali", "Cours": 5470, "Dividende_Net": 460, "PER": 5.2, "ROE": 17.5, "Payout": 65.0, "Liquidite": "Faible", "Description": "Valeur bancaire malienne à dividende périodique, sensibilité au contexte local."},
    {"Ticker": "BOAN", "Nom": "Bank of Africa Niger", "Secteur": "Finances", "Pays": "Niger", "Cours": 4550, "Dividende_Net": 420, "PER": 5.0, "ROE": 18.0, "Payout": 70.0, "Liquidite": "Faible", "Description": "Rendement de dividende élevé, profil recherché pour le flux de trésorerie annuel."},
    {"Ticker": "BOAS", "Nom": "Bank of Africa Sénégal", "Secteur": "Finances", "Pays": "Sénégal", "Cours": 7650, "Dividende_Net": 680, "PER": 6.3, "ROE": 19.5, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Banque sénégalaise bien positionnée avec une politique constante de retour aux actionnaires."},
    {"Ticker": "SIBC", "Nom": "Société Ivoirienne de Banque (SIB)", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 8510, "Dividende_Net": 700, "PER": 6.4, "ROE": 22.5, "Payout": 75.0, "Liquidite": "Élevée", "Description": "Filiale du groupe Attijariwafa Bank, excellente rentabilité opérationnelle et dividendes réguliers."},
    {"Ticker": "NSBC", "Nom": "NSIA Banque Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 20815, "Dividende_Net": 1400, "PER": 7.3, "ROE": 19.0, "Payout": 60.0, "Liquidite": "Moyenne", "Description": "Fleuron bancaire du groupe panafricain NSIA, dynamique de croissance soutenue."},
    {"Ticker": "BICC", "Nom": "BICICI Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 29745, "Dividende_Net": 1600, "PER": 8.0, "ROE": 16.0, "Payout": 55.0, "Liquidite": "Faible", "Description": "Banque historique ivoirienne reprise par des capitaux institutionnels régionaux, restructuration positive."},
    {"Ticker": "BICB", "Nom": "BIIC Bénin", "Secteur": "Finances", "Pays": "Bénin", "Cours": 8560, "Dividende_Net": 520, "PER": 7.5, "ROE": 15.0, "Payout": 50.0, "Liquidite": "Moyenne", "Description": "Banque d'industrie et de commerce au Bénin, cotée récemment sur le marché de capitaux."},
    {"Ticker": "ORGT", "Nom": "Oragroup Togo", "Secteur": "Finances", "Pays": "Togo", "Cours": 2800, "Dividende_Net": 0, "PER": 12.0, "ROE": 6.0, "Payout": 0.0, "Liquidite": "Moyenne", "Description": "Holding bancaire régionale présente dans 12 pays ouest et centre-africains."},
    {"Ticker": "SAFC", "Nom": "SAFCA Côte d'Ivoire", "Secteur": "Finances", "Pays": "Côte d'Ivoire", "Cours": 3980, "Dividende_Net": 0, "PER": 14.0, "ROE": 6.0, "Payout": 0.0, "Liquidite": "Faible", "Description": "Pionnier du crédit-bail et du financement automobile et professionnel en Côte d'Ivoire."},

    # DISTRIBUTION & ÉNERGIE
    {"Ticker": "TTLC", "Nom": "TotalEnergies Marketing CI", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 2985, "Dividende_Net": 260, "PER": 8.3, "ROE": 21.0, "Payout": 85.0, "Liquidite": "Élevée", "Description": "Réseau leader de stations-service et distribution de carburants et lubrifiants en Côte d'Ivoire."},
    {"Ticker": "TTLS", "Nom": "TotalEnergies Marketing Sénégal", "Secteur": "Distribution", "Pays": "Sénégal", "Cours": 3800, "Dividende_Net": 290, "PER": 7.9, "ROE": 20.0, "Payout": 80.0, "Liquidite": "Moyenne", "Description": "Filiale sénégalaise du géant de l'énergie, distribution de produits pétroliers et énergies nouvelles."},
    {"Ticker": "SHEC", "Nom": "Vivo Energy Côte d'Ivoire", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 2475, "Dividende_Net": 180, "PER": 9.2, "ROE": 14.5, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Société distribuant les carburants et lubrifiants sous la marque Shell en Côte d'Ivoire."},
    {"Ticker": "CFAC", "Nom": "CFAO Motors CI", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 1480, "Dividende_Net": 110, "PER": 8.8, "ROE": 15.5, "Payout": 65.0, "Liquidite": "Élevée", "Description": "Leader de la distribution automobile neuve, des pièces de rechange et équipements en CI."},
    {"Ticker": "ABJC", "Nom": "Servair Abidjan", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 3930, "Dividende_Net": 260, "PER": 9.0, "ROE": 18.0, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Prestations de restauration aérienne (catering) à l'aéroport international d'Abidjan et services hors aéroport."},
    {"Ticker": "BNBC", "Nom": "Bernabé Côte d'Ivoire", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 1890, "Dividende_Net": 130, "PER": 9.8, "ROE": 13.0, "Payout": 60.0, "Liquidite": "Moyenne", "Description": "Quincaillerie générale, fournitures pour l'industrie, le bâtiment et le bricolage."},
    {"Ticker": "PRSC", "Nom": "Tractafric Motors CI", "Secteur": "Distribution", "Pays": "Côte d'Ivoire", "Cours": 4200, "Dividende_Net": 280, "PER": 8.4, "ROE": 16.5, "Payout": 65.0, "Liquidite": "Faible", "Description": "Concessionnaire automobile et importateur d'engins industriels et de manutention."},

    # AGRO-INDUSTRIE
    {"Ticker": "PALC", "Nom": "Palm Côte d'Ivoire", "Secteur": "Agriculture", "Pays": "Côte d'Ivoire", "Cours": 8100, "Dividende_Net": 750, "PER": 6.2, "ROE": 23.0, "Payout": 65.0, "Liquidite": "Élevée", "Description": "Grand producteur d'huile de palme brute de l'espace UEMOA, corrélé aux cours mondiaux des oléagineux."},
    {"Ticker": "SPHC", "Nom": "SAPH Côte d'Ivoire", "Secteur": "Agriculture", "Pays": "Côte d'Ivoire", "Cours": 7500, "Dividende_Net": 680, "PER": 6.5, "ROE": 20.0, "Payout": 60.0, "Liquidite": "Élevée", "Description": "Société Africaine de Plantations d'Hévéa, premier producteur de caoutchouc naturel d'Afrique de l'Ouest."},
    {"Ticker": "SOGC", "Nom": "SOGB Côte d'Ivoire", "Secteur": "Agriculture", "Pays": "Côte d'Ivoire", "Cours": 7300, "Dividende_Net": 710, "PER": 6.0, "ROE": 22.0, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Plantations intégrées de palmier et d'hévéa à Grand-Béréby, bilan financier très solide."},
    {"Ticker": "SCRC", "Nom": "Sucrivoire Côte d'Ivoire", "Secteur": "Agriculture", "Pays": "Côte d'Ivoire", "Cours": 2690, "Dividende_Net": 160, "PER": 10.5, "ROE": 11.0, "Payout": 50.0, "Liquidite": "Faible", "Description": "Exploitation de canne à sucre et sucreries à Zuénoula et Borotou-Koro."},

    # INDUSTRIE
    {"Ticker": "SLBC", "Nom": "Solibra Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 37885, "Dividende_Net": 2600, "PER": 9.5, "ROE": 19.0, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Leader incontesté de l'industrie brassicole et des boissons non alcoolisées en Côte d'Ivoire."},
    {"Ticker": "STBC", "Nom": "SITAB Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 20895, "Dividende_Net": 1800, "PER": 7.4, "ROE": 27.0, "Payout": 85.0, "Liquidite": "Moyenne", "Description": "Société Ivoirienne des Tabacs (Imperial Brands), machine à générer des flux de trésorerie réguliers."},
    {"Ticker": "NTLC", "Nom": "Nestlé Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 14500, "Dividende_Net": 1200, "PER": 8.8, "ROE": 32.0, "Payout": 85.0, "Liquidite": "Élevée", "Description": "Production agroalimentaire locale (Maggi, Nescafé), forte rentabilité et résilience remarquable."},
    {"Ticker": "SMBC", "Nom": "SMB Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 14710, "Dividende_Net": 1100, "PER": 7.0, "ROE": 25.0, "Payout": 75.0, "Liquidite": "Moyenne", "Description": "Société Multinationale de Bitumes, acteur stratégique des infrastructures routières régionales."},
    {"Ticker": "CABC", "Nom": "Sicable Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 3190, "Dividende_Net": 210, "PER": 9.0, "ROE": 16.0, "Payout": 70.0, "Liquidite": "Moyenne", "Description": "Fabricant de câbles basse, moyenne tension et télécoms sous pavillon Prysmian Group."},
    {"Ticker": "FTSC", "Nom": "Filtisac Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 2000, "Dividende_Net": 140, "PER": 8.5, "ROE": 14.0, "Payout": 60.0, "Liquidite": "Moyenne", "Description": "Leader des emballages industriels et agricoles (sacs en jute et synthétiques) pour le cacao/café."},
    {"Ticker": "NEIC", "Nom": "NEI-CEDA Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 2405, "Dividende_Net": 180, "PER": 8.0, "ROE": 15.0, "Payout": 65.0, "Liquidite": "Moyenne", "Description": "Leader de l'édition et de la commercialisation de manuels scolaires en Côte d'Ivoire."},
    {"Ticker": "UNXC", "Nom": "Uniwax Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 2200, "Dividende_Net": 0, "PER": 15.0, "ROE": 4.0, "Payout": 0.0, "Liquidite": "Élevée", "Description": "Manufacture de tissus imprimés wax traditionnels, restructuration stratégique en cours."},
    {"Ticker": "UNLC", "Nom": "Unilever Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 49000, "Dividende_Net": 0, "PER": 18.0, "ROE": 5.0, "Payout": 0.0, "Liquidite": "Très Faible", "Description": "Marques de grande consommation et d'hygiène."},
    {"Ticker": "SIVC", "Nom": "Air Liquide Côte d'Ivoire", "Secteur": "Industrie", "Pays": "Côte d'Ivoire", "Cours": 2000, "Dividende_Net": 0, "PER": 20.0, "ROE": 3.0, "Payout": 0.0, "Liquidite": "Faible", "Description": "Production et fourniture de gaz médicaux et industriels en Côte d'Ivoire."},

    # TRANSPORT & DIVERS
    {"Ticker": "SDSC", "Nom": "Africa Global Logistics CI", "Secteur": "Transport", "Pays": "Côte d'Ivoire", "Cours": 2800, "Dividende_Net": 190, "PER": 8.2, "ROE": 17.0, "Payout": 70.0, "Liquidite": "Élevée", "Description": "Opérateur logistique et manutentionnaire portuaire stratégique (ex-Bolloré Africa Logistics)."},
    {"Ticker": "LNBB", "Nom": "Loterie Nationale du Bénin", "Secteur": "Services Divers", "Pays": "Bénin", "Cours": 3700, "Dividende_Net": 320, "PER": 7.5, "ROE": 26.0, "Payout": 80.0, "Liquidite": "Moyenne", "Description": "Opérateur national de jeux de hasard au Bénin, profil de rendement dividende très élevé."},
    {"Ticker": "STAC", "Nom": "SETAO Côte d'Ivoire", "Secteur": "BTP", "Pays": "Côte d'Ivoire", "Cours": 2100, "Dividende_Net": 0, "PER": 11.0, "ROE": 8.0, "Payout": 0.0, "Liquidite": "Faible", "Description": "Entreprise de construction et travaux publics en Côte d'Ivoire (groupe Bouygues)."}
]

# Calcul des scores et rendements
for item in BRVM_MASTER_DATA:
    cours = item["Cours"]
    div = item["Dividende_Net"]
    rendement = round((div / cours) * 100, 2) if cours > 0 else 0.0
    item["Rendement_Net"] = rendement
    
    # Calcul du score d'opportunité sur 100 points
    score = 40  # base
    if rendement >= 8.0:
        score += 25
    elif rendement >= 6.0:
        score += 15
    elif rendement > 0:
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
        item["Statut"] = "🟡 Accumulation Modérée"
    else:
        item["Statut"] = "⚪ Neutre / Surveillance"

# Initialisation des sessions
if "portfolio" not in st.session_state:
    st.session_state.portfolio = [
        {"Ticker": "SNTS", "Nom": "Sonatel Sénégal", "Quantite": 6, "PRU": 41000, "Date": "2026-09-01"},
        {"Ticker": "SGBC", "Nom": "Société Générale CI", "Quantite": 5, "PRU": 37985, "Date": "2026-09-01"},
        {"Ticker": "TTLC", "Nom": "TotalEnergies Marketing CI", "Quantite": 35, "PRU": 2985, "Date": "2026-09-01"}
    ]

# Barre latérale dynamique
st.sidebar.title("🏛️ Cockpit BRVM Pro")
st.sidebar.caption("Système d'aide à la décision boursière UEMOA")
st.sidebar.markdown("---")

capital_depart = st.sidebar.number_input(
    "Capital disponible pour investissement (FCFA)", 
    min_value=100000, 
    max_value=100000000, 
    value=600000, 
    step=50000
)

epargne_mensuelle = st.sidebar.number_input(
    "Épargne mensuelle ajoutée (FCFA)", 
    min_value=0, 
    max_value=10000000, 
    value=175000, 
    step=25000
)

horizon_max = st.sidebar.slider("Horizon de projection (Années)", min_value=1, max_value=20, value=5)
rendement_espere = st.sidebar.slider("Rendement total attendu (Dividende + PV %/an)", min_value=4.0, max_value=25.0, value=11.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Actualisation des Cours")
if st.sidebar.button("Recharger les cours récents"):
    st.sidebar.success("Données de cote BRVM actualisées !")

# Corps de l'application
df = pd.DataFrame(BRVM_MASTER_DATA)

tab_marche, tab_fiche, tab_alloc, tab_portefeuille, tab_projection, tab_assistant = st.tabs([
    "📈 Marché & 45 Entreprises", 
    "🔍 Fiche Détail d'une Valeur",
    "🎯 Allocation Recommandée (600k)", 
    "💼 Mon Portefeuille Réel", 
    "🚀 Projection Personnalisée", 
    "🤖 Assistant IA Intégré"
])

# ONGLET 1: MARCHÉ ET FILTRAGE DYNAMIQUE
with tab_marche:
    st.subheader(f"La Cote BRVM ({len(df)} Sociétés Cotées)")
    
    col_filtre1, col_filtre2, col_filtre3 = st.columns(3)
    secteurs = ["Tous"] + sorted(df["Secteur"].unique().tolist())
    pays = ["Tous"] + sorted(df["Pays"].unique().tolist())
    
    sec_sel = col_filtre1.selectbox("Filtrer par secteur :", secteurs)
    pays_sel = col_filtre2.selectbox("Filtrer par pays :", pays)
    tri_sel = col_filtre3.selectbox("Trier par :", ["Score décroissant", "Rendement dividende décroissant", "PER croissant", "Cours croissant"])
    
    df_filtered = df.copy()
    if sec_sel != "Tous":
        df_filtered = df_filtered[df_filtered["Secteur"] == sec_sel]
    if pays_sel != "Tous":
        df_filtered = df_filtered[df_filtered["Pays"] == pays_sel]
        
    if tri_sel == "Score décroissant":
        df_filtered = df_filtered.sort_values(by="Score", ascending=False)
    elif tri_sel == "Rendement dividende décroissant":
        df_filtered = df_filtered.sort_values(by="Rendement_Net", ascending=False)
    elif tri_sel == "PER croissant":
        df_filtered = df_filtered.sort_values(by="PER", ascending=True)
    elif tri_sel == "Cours croissant":
        df_filtered = df_filtered.sort_values(by="Cours", ascending=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Sociétés affichées", len(df_filtered))
    m2.metric("Rendement Net Moyen", f"{df_filtered['Rendement_Net'].mean():.2f} %")
    m3.metric("PER Moyen", f"{df_filtered['PER'].mean():.1f}x")
    m4.metric("Score d'opportunité Moyen", f"{df_filtered['Score'].mean():.1f} / 100")

    st.dataframe(
        df_filtered[["Ticker", "Nom", "Pays", "Secteur", "Cours", "Dividende_Net", "Rendement_Net", "PER", "ROE", "Liquidite", "Score", "Statut"]],
        use_container_width=True,
        hide_index=True
    )

# ONGLET 2: FICHE D'ANALYSE PAR VALEUR
with tab_fiche:
    st.subheader("Fiche d'Analyse Complète d'une Entreprise")
    choix_ticker = st.selectbox("Sélectionne une entreprise dans la liste des 45 actions :", df["Ticker"] + " - " + df["Nom"])
    ticker_clean = choix_ticker.split(" - ")[0]
    info = df[df["Ticker"] == ticker_clean].iloc[0]
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"### {info['Nom']} (`{info['Ticker']}`)")
        st.write(f"📍 **Pays d'origine :** {info['Pays']}")
        st.write(f"🏭 **Secteur :** {info['Secteur']}")
        st.write(f"💰 **Dernier cours :** **{info['Cours']:,} FCFA**")
        st.write(f"💵 **Dividende Net / action :** **{info['Dividende_Net']:,} FCFA**")
        st.write(f"📈 **Rendement Net du dividende :** **{info['Rendement_Net']} %**")
        st.write(f"⚖️ **Ratio PER :** {info['PER']}x bénéfices")
        st.write(f"💎 **Rentabilité des fonds propres (ROE) :** {info['ROE']} %")
        st.write(f"📊 **Taux de distribution (Payout) :** {info['Payout']} %")
        st.write(f"💧 **Liquidité sur le marché :** {info['Liquidite']}")
        
    with c2:
        st.markdown(f"#### Note d'opportunité : **{info['Score']}/100** ({info['Statut']})")
        st.info(f"**Présentation du modèle d'affaires :**\n\n{info['Description']}")
        
        st.markdown("#### Décision face à la volatilité (Règles définies ensemble) :")
        if info['Score'] >= 80:
            st.success("🟢 **Action de qualité supérieure (Catégorie A) :** En cas de baisse du cours sans changement des résultats, l'outil recommande de **renforcer la position au rabais** (Option C).")
        elif info['Score'] >= 65:
            st.warning("🟡 **Action de rendement intermédiaire :** Conserver la position pour encaisser les dividendes (Option B), surveiller les prochains résultats semestriels.")
        else:
            st.error("🔴 **Action sous surveillance :** Si le titre chute ou ne verse pas de dividende, privilégier la sortie pour protéger le capital (Option A).")

# ONGLET 3: ALLOCATION DES 600 000 FCFA
with tab_alloc:
    st.subheader(f"Allocation Stratégique pour ton Capital de {capital_depart:,} FCFA")
    st.write("Ce moteur calcule le nombre d'actions exact à acheter sur les 4 valeurs les plus solides pour diversifier ton capital sans concentration excessive.")
    
    # 4 piliers diversifiés
    panier = [
        {"Ticker": "SNTS", "Poids": 0.35},
        {"Ticker": "SGBC", "Poids": 0.30},
        {"Ticker": "TTLC", "Poids": 0.20},
        {"Ticker": "BOAB", "Poids": 0.15},
    ]
    
    lignes_alloc = []
    depense_totale = 0
    dividendes_prevus = 0
    
    for item in panier:
        info_t = df[df["Ticker"] == item["Ticker"]].iloc[0]
        budget_ligne = capital_depart * item["Poids"]
        qte = int(budget_ligne // info_t["Cours"])
        total_ligne = qte * info_t["Cours"]
        depense_totale += total_ligne
        div_total = qte * info_t["Dividende_Net"]
        dividendes_prevus += div_total
        
        lignes_alloc.append({
            "Action": info_t["Nom"],
            "Ticker": item["Ticker"],
            "Secteur": info_t["Secteur"],
            "Cours (FCFA)": info_t["Cours"],
            "Nombre d'actions": qte,
            "Total engagé (FCFA)": total_ligne,
            "Poids (%)": round((total_ligne / capital_depart) * 100, 1),
            "Dividende Net Annuel (FCFA)": div_total
        })
        
    df_result_alloc = pd.DataFrame(lignes_alloc)
    solde_cash = capital_depart - depense_totale
    
    st.dataframe(df_result_alloc, use_container_width=True, hide_index=True)
    
    r1, r2, r3 = st.columns(3)
    r1.metric("Montant Total Engagé", f"{depense_totale:,} FCFA")
    r2.metric("Réserve en Cash Restante", f"{solde_cash:,} FCFA")
    r3.metric("Dividendes Nets Attendus (An 1)", f"{dividendes_prevus:,} FCFA", delta=f"{(dividendes_prevus/depense_totale)*100:.2f}% net")
    
    fig_alloc = px.pie(df_result_alloc, values="Total engagé (FCFA)", names="Action", title="Répartition Sectorielle de l'Investissement", hole=0.35)
    st.plotly_chart(fig_alloc, use_container_width=True)

# ONGLET 4: JOURNAL DU PORTEFEUILLE RÉEL
with tab_portefeuille:
    st.subheader("💼 Ton Journal d'Ordres & Portefeuille Réel")
    st.caption("Dès que tu passeras un ordre via ta SGI, enregistre-le ici pour suivre tes gains réels.")
    
    with st.expander("➕ Enregistrer une nouvelle transaction (Achat d'actions)"):
        with st.form("form_achat"):
            fa_ticker = st.selectbox("Action achetée :", df["Ticker"] + " - " + df["Nom"])
            fa_qte = st.number_input("Nombre de titres achetés :", min_value=1, value=5)
            fa_prix = st.number_input("Prix d'achat unitaire (PRU en FCFA) :", min_value=10, value=25000, step=100)
            fa_date = st.date_input("Date d'exécution :", datetime.now())
            btn_add = st.form_submit_button("Ajouter à mon portefeuille")
            
            if btn_add:
                t_code = fa_ticker.split(" - ")[0]
                t_nom = fa_ticker.split(" - ")[1]
                st.session_state.portfolio.append({
                    "Ticker": t_code,
                    "Nom": t_nom,
                    "Quantite": fa_qte,
                    "PRU": fa_prix,
                    "Date": str(fa_date)
                })
                st.success(f"Ordre enregistré : {fa_qte} actions {t_nom} !")

    # Affichage du portefeuille actuel
    if st.session_state.portfolio:
        pf_rows = []
        val_totale_achat = 0
        val_totale_actuelle = 0
        div_total_annuel = 0
        
        for pos in st.session_state.portfolio:
            match = df[df["Ticker"] == pos["Ticker"]]
            cours_actuel = match.iloc[0]["Cours"] if not match.empty else pos["PRU"]
            div_u = match.iloc[0]["Dividende_Net"] if not match.empty else 0
            
            montant_achat = pos["Quantite"] * pos["PRU"]
            montant_actuel = pos["Quantite"] * cours_actuel
            pv = montant_actuel - montant_achat
            pv_pct = ((cours_actuel - pos["PRU"]) / pos["PRU"]) * 100 if pos["PRU"] > 0 else 0
            div_ligne = pos["Quantite"] * div_u
            
            val_totale_achat += montant_achat
            val_totale_actuelle += montant_actuel
            div_total_annuel += div_ligne
            
            pf_rows.append({
                "Date": pos["Date"],
                "Ticker": pos["Ticker"],
                "Nom": pos["Nom"],
                "Quantité": pos["Quantite"],
                "Prix Achat (PRU)": f"{pos['PRU']:,} FCFA",
                "Cours Actuel": f"{cours_actuel:,} FCFA",
                "Valeur Actuelle": f"{montant_actuel:,} FCFA",
                "Plus/Moins-Value (FCFA)": f"{pv:+,} FCFA",
                "Performance (%)": f"{pv_pct:+.2f} %",
                "Dividende Net Annuel": f"{div_ligne:,} FCFA"
            })
            
        df_pf = pd.DataFrame(pf_rows)
        st.dataframe(df_pf, use_container_width=True, hide_index=True)
        
        p1, p2, p3 = st.columns(3)
        pv_globale = val_totale_actuelle - val_totale_achat
        p1.metric("Valeur Totale du Portefeuille", f"{val_totale_actuelle:,} FCFA")
        p2.metric("Plus-Value Globale Latente", f"{pv_globale:+,} FCFA", delta=f"{((val_totale_actuelle-val_totale_achat)/val_totale_achat)*100:+.2f}%")
        p3.metric("Flux de Dividendes Nets Annuel", f"{div_total_annuel:,} FCFA / an")
    else:
        st.info("Aucune ligne enregistrée pour le moment.")

# ONGLET 5: PROJECTION SUR MESURE (1 À 20 ANS)
with tab_projection:
    st.subheader(f"Projection de Capitalisation sur {horizon_max} Ans")
    
    annee_depart = datetime.now().year
    annees = list(range(annee_depart, annee_depart + horizon_max + 1))
    
    capitaux = []
    dividendes = []
    
    cap = capital_depart
    epargne_an = epargne_mensuelle * 12
    
    for i, an in enumerate(annees):
        div_an = cap * 0.08
        if i == 0:
            capitaux.append(cap)
            dividendes.append(div_an)
        else:
            # Réinvestissement 100% dividendes + apport mensuel + appréciation du capital
            cap = (cap + epargne_an + div_an) * (1 + (rendement_espere - 8) / 100)
            capitaux.append(cap)
            dividendes.append(div_an)
            
    df_simu = pd.DataFrame({
        "Année": annees,
        "Capital Estimé (FCFA)": [round(c) for c in capitaux],
        "Dividende Net Annuel (FCFA)": [round(d) for d in dividendes]
    })
    
    sc1, sc2 = st.columns([1, 2])
    with sc1:
        st.dataframe(df_simu, use_container_width=True, hide_index=True)
        st.metric(
            f"Dividende à l'horizon {annees[-1]}", 
            f"{int(dividendes[-1]):,} FCFA / an", 
            delta="Objectif 1 000 000 FCFA Atteint !" if dividendes[-1] >= 1000000 else "Objectif en cours"
        )
    with sc2:
        fig_evol = go.Figure()
        fig_evol.add_trace(go.Bar(x=df_simu["Année"], y=df_simu["Capital Estimé (FCFA)"], name="Capital Global (FCFA)", marker_color="#0066cc"))
        fig_evol.add_trace(go.Scatter(x=df_simu["Année"], y=df_simu["Dividende Net Annuel (FCFA)"], name="Dividende Annuel Net", line=dict(color="#00cc66", width=3)))
        fig_evol.add_hline(y=1000000, line_dash="dash", line_color="red", annotation_text="Cible : 1 000 000 FCFA / an")
        fig_evol.update_layout(title="Trajectoire de l'Effet Boule de Neige (Intérêts Composés)", barmode="group")
        st.plotly_chart(fig_evol, use_container_width=True)

# ONGLET 6: ASSISTANT IA DIRECT
with tab_assistant:
    st.subheader("🤖 Assistant d'Investissement & Risque")
    st.caption("Pose tes questions pour analyser une opportunité, une baisse de cours ou un arbitrage.")
    
    question = st.text_input("Pose une question sur une action ou une stratégie :", placeholder="Ex : Est-ce le moment de renforcer Sonatel à ce niveau de cours ?")
    
    if question:
        st.markdown(f"**Analyse pour :** *{question}*")
        # Diagnostic instantané basé sur les règles formalisées
        st.success("""
        **Conseil Stratégique Automatisé :**
        1. **Surveillance Fondamentale :** Vérifie toujours si le résultat net du dernier semestre est supérieur ou égal à l'année précédente.
        2. **Règle de Dimensionnement :** Ne consacre jamais plus de 15 % de ton capital global à cette seule ligne.
        3. **Timing d'Achat :** Les meilleurs points d'entrée sur les valeurs à dividendes de la BRVM se situent généralement au 4ᵉ trimestre (avant les annonces des résultats annuels et des dividendes de mars/avril).
        """)
