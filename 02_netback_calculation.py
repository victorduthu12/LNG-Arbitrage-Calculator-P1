"""
Étape 2 — Calcul du netback par route
========================================
LOGIQUE MÉTIER (la partie la plus importante à comprendre) :

Une cargaison de GNL part des US. Elle peut être envoyée vers l'Europe ou vers l'Asie.
Le "netback" = combien d'argent il reste une fois TOUS les coûts payés.

netback_destination = prix_de_vente_destination
                       - prix_achat_gaz (Henry Hub)
                       - coût_liquéfaction
                       - coût_transport_maritime (différent selon la distance)
                       - coût_régazéification (remettre le GNL en gaz à l'arrivée)

On compare netback_europe vs netback_asie : la route avec le netback le plus élevé
est celle que choisirait un trader physique.

Tous les coûts sont en $/MMBtu pour rester cohérent avec les prix (gaz coté en $/MMBtu).
"""

import pandas as pd

df = pd.read_csv("/home/claude/lng_arbitrage/prix_simules.csv", parse_dates=["date"])

# --- Hypothèses de coûts (ordres de grandeur réalistes du marché GNL) ---
COUT_LIQUEFACTION = 2.50      # coût fixe pour liquéfier le gaz aux US ($/MMBtu)
COUT_REGAZEIFICATION = 0.40   # coût fixe pour regazéifier à l'arrivée ($/MMBtu)

# Le transport maritime dépend de la distance : l'Asie est plus loin que l'Europe
# depuis la côte US (Gulf Coast), donc le coût de transport y est plus élevé
COUT_TRANSPORT_EUROPE = 0.90  # $/MMBtu (trajet plus court, ex: Gulf Coast -> Rotterdam)
COUT_TRANSPORT_ASIE = 1.80    # $/MMBtu (trajet plus long, ex: Gulf Coast -> Japon via Panama/Cap)

# --- Calcul du netback vers l'Europe ---
df["netback_europe"] = (
    df["ttf_europe"]
    - df["henry_hub_us"]
    - COUT_LIQUEFACTION
    - COUT_TRANSPORT_EUROPE
    - COUT_REGAZEIFICATION
)

# --- Calcul du netback vers l'Asie ---
df["netback_asie"] = (
    df["jkm_asie"]
    - df["henry_hub_us"]
    - COUT_LIQUEFACTION
    - COUT_TRANSPORT_ASIE
    - COUT_REGAZEIFICATION
)

# --- Décision : quelle route est la plus rentable ce mois-ci ? ---
df["route_optimale"] = df.apply(
    lambda ligne: "Asie" if ligne["netback_asie"] > ligne["netback_europe"] else "Europe",
    axis=1
)

# --- Spread entre les deux routes (utile pour visualiser l'ampleur de l'arbitrage) ---
df["spread_asie_europe"] = df["netback_asie"] - df["netback_europe"]

df.to_csv("/home/claude/lng_arbitrage/netback_results.csv", index=False)

print(df[["date", "netback_europe", "netback_asie", "route_optimale", "spread_asie_europe"]].to_string(index=False))

print("\n--- Résumé ---")
print(df["route_optimale"].value_counts())
print(f"\nNetback moyen Europe : {df['netback_europe'].mean():.2f} $/MMBtu")
print(f"Netback moyen Asie   : {df['netback_asie'].mean():.2f} $/MMBtu")
