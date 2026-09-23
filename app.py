import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="BRVM Alpha Decision Cockpit",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style personnalisé
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .metric-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2d3139;
    }
    </style>
""", unsafe_allow_html=True)

# Données de référence du panier BRVM
DATA_BRVM = [
    {
        "Ticker": "SNTS",
        "Nom": "Sonatel Sénégal",
        "Secteur": "Télécoms",
        "Cours": 23500,
        "Dividende_Net": 1750,
        "Rendement_Net": 7.45,
        "PER": 7.8,
        "ROE": 28.5,
        "Payout": 72.0,
        "Liquidite": "Très Élevée",
        "Score": 88,
        "Statut": "Achat Fort",
        "Raison": "Leader incontesté de la BRVM, trésorerie robuste, dividende versé sans interruption depuis plus de 15 ans."
    },
    {
        "Ticker": "SGBC",
        "Nom": "Société Générale CI",
        "Secteur": "Banque",
        "Cours": 19800,
        "Dividende_Net": 1650,
        "Rendement_Net": 8.33,
        "PER": 6.5,
        "ROE": 24.0,
        "Payout": 65.0,
        "Liquidite": "Élevée",
        "Score": 84,
        "Statut": "Achat Fort",
        "Raison": "Première banque de Côte d'Ivoire, rentabilité très solide, dividende en constante progression."
    },
    {
        "Ticker": "BOAB",
        "Nom": "Bank of Africa Bénin",
        "Secteur": "Banque",
        "Cours": 7100,
        "Dividende_Net": 680,
        "Rendement_Net": 9.58,
        "PER": 5.9,
        "ROE": 21.0,
        "Payout": 75.0,
        "Liquidite": "Moyenne",
        "Score": 79,
        "Statut": "Achat Renforcé",
        "Raison": "Rendement de dividende parmi les plus élevés de la zone UEMOA, bilan maîtrisé."
    },
    {
        "Ticker": "TTLC",
        "Nom": "TotalEnergies Marketing CI",
        "Secteur": "Distribution & Énergie",
        "Cours": 2450,
        "Dividende_Net": 220,
        "Rendement_Net": 8.98,
        "PER": 8.2,
        "ROE": 19.5,
        "Payout": 80.0,
        "Liquidite": "Élevée",
        "Score": 76,
        "Statut": "Achat / Conservation",
        "Raison": "Réseau de distribution n°1, flux de trésorerie régulier, valeur défensive par excellence."
    },
    {
        "Ticker": "CFAC",
        "Nom": "CFAO Motors CI",
        "Secteur": "Distribution",
        "Cours": 850,
        "Dividende_Net": 60,
        "Rendement_Net": 7.05,
        "PER": 9.1,
        "ROE": 15.0,
        "Payout": 60.0,
        "Liquidite": "Moyenne",
        "Score": 68,
        "Statut": "Neutre / Surveillance",
        "Raison": "Secteur cyclique lié aux importations automobiles, marge sous pression ponctuelle."
    }
]

df_market = pd.DataFrame(DATA_BRVM)

# Barre latérale (Paramètres de l'investisseur)
st.sidebar.title("⚙️ Paramètres Portefeuille")
st.sidebar.markdown("---")

capital_depart = st.sidebar.number_input(
    "Capital d'amorçage (FCFA)", 
    min_value=100000, 
    max_value=50000000, 
    value=600000, 
    step=50000
)

epargne_mensuelle = st.sidebar.number_input(
    "Épargne mensuelle injectée (FCFA)", 
    min_value=0, 
    max_value=5000000, 
    value=175000, 
    step=25000
)

horizon_annees = st.sidebar.slider("Horizon de capitalisation (Années)", min_value=1, max_value=10, value=4)
rendement_moyen = st.sidebar.slider("Rendement annuel estimé (Dividendes + PV %)", min_value=5.0, max_value=20.0, value=10.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Règle d'or :** Tous les dividendes touchés entre mai et septembre sont 100% réinvestis jusqu'en 2030.")

# Entête Principal
st.title("🏛️ BRVM Decision Cockpit & Risk Manager")
st.caption("Outil d'aide à la décision boursière et de gestion du risque — UEMOA")

# Onglets
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Screener & Matrice de Score", 
    "🎯 Allocation de tes 600 000 FCFA", 
    "🚀 Projection 2026 - Fin 2030", 
    "🛡️ Gestionnaire de Risque & Volatilité"
])

# ONGLET 1: Screener
with tab1:
    st.subheader("Matrice de notation des opportunités BRVM (Score / 100)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Valeurs suivies", len(df_market))
    col2.metric("Rendement Net Moyen", f"{df_market['Rendement_Net'].mean():.2f} %")
    col3.metric("Score Moyen", f"{df_market['Score'].mean():.1f} / 100")
    
    st.dataframe(
        df_market[["Ticker", "Nom", "Secteur", "Cours", "Rendement_Net", "PER", "ROE", "Score", "Statut"]],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("### Analyse détaillée d'une valeur")
    selected_ticker = st.selectbox("Sélectionne une entreprise pour voir l'audit :", df_market["Ticker"].tolist())
    val = df_market[df_market["Ticker"] == selected_ticker].iloc[0]
    
    c_a, c_b = st.columns([1, 2])
    with c_a:
        st.markdown(f"**{val['Nom']} ({val['Ticker']})**")
        st.write(f"- Cours actuel : **{val['Cours']:,} FCFA**")
        st.write(f"- Dividende net estimé : **{val['Dividende_Net']:,} FCFA**")
        st.write(f"- Rendement net : **{val['Rendement_Net']} %**")
        st.write(f"- Ratio cours/bénéfice (PER) : **{val['PER']}**")
        st.write(f"- Rentabilité capitaux propres (ROE) : **{val['ROE']} %**")
    with c_b:
        st.success(f"**Recommandation de l'outil : {val['Statut']}** (Score: {val['Score']}/100)")
        st.write(f"**Thèse d'investissement :** {val['Raison']}")

# ONGLET 2: Allocation 600 000 FCFA
with tab2:
    st.subheader("Proposition d'achat équilibrée pour démarrer")
    st.write(f"Budget à allouer : **{capital_depart:,} FCFA** (Réparti sur les meilleures valeurs sans concentration excessive)")
    
    # Répartition prudente recommandée : 40% Sonatel, 30% SGBCI, 20% Total CI, 10% BOA Bénin
    alloc = [
        {"Ticker": "SNTS", "Poids": 0.40, "Cours": 23500},
        {"Ticker": "SGBC", "Poids": 0.30, "Cours": 19800},
        {"Ticker": "TTLC", "Poids": 0.20, "Cours": 2450},
        {"Ticker": "BOAB", "Poids": 0.10, "Cours": 7100},
    ]
    
    lignes = []
    total_investi = 0
    total_dividendes_attendus = 0
    
    for a in alloc:
        montant_alloue = capital_depart * a["Poids"]
        qte = int(montant_alloue // a["Cours"])
        cout_total = qte * a["Cours"]
        total_investi += cout_total
        info = df_market[df_market["Ticker"] == a["Ticker"]].iloc[0]
        div_net = qte * info["Dividende_Net"]
        total_dividendes_attendus += div_net
        
        lignes.append({
            "Action": info["Nom"],
            "Ticker": a["Ticker"],
            "Cours (FCFA)": a["Cours"],
            "Quantité d'actions": qte,
            "Montant total (FCFA)": cout_total,
            "Part (%)": round((cout_total / capital_depart) * 100, 1),
            "Dividende Net Annuel (FCFA)": div_net
        })
        
    df_alloc = pd.DataFrame(lignes)
    cash_restant = capital_depart - total_investi
    
    st.dataframe(df_alloc, use_container_width=True, hide_index=True)
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Capital Utilisé", f"{total_investi:,} FCFA")
    k2.metric("Reste en Cash (Réserve)", f"{cash_restant:,} FCFA")
    k3.metric("Dividendes Nets An 1", f"{total_dividendes_attendus:,} FCFA", delta=f"{(total_dividendes_attendus/total_investi)*100:.2f}% net")

    fig_pie = px.pie(df_alloc, values="Montant total (FCFA)", names="Action", title="Répartition du portefeuille initial", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# ONGLET 3: Projection 2026 - 2030
with tab3:
    st.subheader("Trajectoire vers l'objectif de 1 000 000 FCFA / an")
    
    annees = list(range(2026, 2026 + horizon_annees + 1))
    valeurs_portefeuille = []
    dividendes_annuels = []
    
    capital_courant = capital_depart
    apport_annuel = epargne_mensuelle * 12
    
    for i, an in enumerate(annees):
        if i == 0:
            div = capital_courant * 0.08
            valeurs_portefeuille.append(capital_courant)
            dividendes_annuels.append(div)
        else:
            div = capital_courant * 0.08
            capital_courant = (capital_courant + apport_annuel + div) * (1 + (rendement_moyen - 8)/100)
            valeurs_portefeuille.append(capital_courant)
            dividendes_annuels.append(div)
            
    df_proj = pd.DataFrame({
        "Année": annees,
        "Capital Estimé (FCFA)": [round(c) for c in valeurs_portefeuille],
        "Dividende Annuel Projeté (FCFA)": [round(d) for d in dividendes_annuels]
    })
    
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        st.dataframe(df_proj, use_container_width=True, hide_index=True)
        st.metric(
            f"Dividende à l'horizon {annees[-1]}", 
            f"{int(dividendes_annuels[-1]):,} FCFA / an",
            delta=f"{'Objectif 1M atteint !' if dividendes_annuels[-1] >= 1000000 else 'En progression'}"
        )
    with col_p2:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df_proj["Année"], y=df_proj["Capital Estimé (FCFA)"], name="Capital Global (FCFA)", marker_color="#1f77b4"))
        fig_bar.add_trace(go.Scatter(x=df_proj["Année"], y=[1000000]*len(annees), mode="lines", name="Ligne Objectif 1M Dividende", line=dict(color="red", dash="dash")))
        fig_bar.update_layout(title="Croissance du Capital et Rente de Dividendes (2026-2030)", barmode="group")
        st.plotly_chart(fig_bar, use_container_width=True)

# ONGLET 4: Gestionnaire de Risque
with tab4:
    st.subheader("Moteur de décision en cas de baisse du marché")
    st.markdown("""
    Quand une action baisse de **plus de 10%**, l'outil applique ton arbitrage prédéfini :
    """)
    
    test_ticker = st.selectbox("Simuler une chute de cours sur :", df_market["Ticker"].tolist(), key="risk_select")
    baisse_pct = st.slider("Chute observée du cours (%)", min_value=5, max_value=40, value=12)
    
    t_val = df_market[df_market["Ticker"] == test_ticker].iloc[0]
    nouveau_cours = int(t_val["Cours"] * (1 - baisse_pct/100))
    
    st.warning(f"Le cours de **{t_val['Nom']}** passe de **{t_val['Cours']:,} FCFA** à **{nouveau_cours:,} FCFA** (-{baisse_pct}%)")
    
    if t_val["Score"] >= 75:
        st.success(f"""
        ### 🟢 SIGNAL : ACHETER SUR FAIBLESSE (Option C)
        - **Diagnostic :** La note de solidité de {t_val['Nom']} est de **{t_val['Score']}/100** (Excellente).
        - **Cause probable :** Mouvement technique général ou panique irrationnelle, mais les fondamentaux restent intacts.
        - **Action recommandée :** Racheter des titres pour abaisser ton Prix Moyen Unitaire (PRU) et maximiser ton futur dividende net.
        """)
    else:
        st.error(f"""
        ### 🔴 SIGNAL : PROTÉGER LE CAPITAL (Option A)
        - **Diagnostic :** La note de solidité est modérée ({t_val['Score']}/100).
        - **Action recommandée :** Ne pas renforcer à l'aveugle. Couper la position ou réorienter le cash vers une valeur pilier (Sonatel / SGBCI).
        """)
