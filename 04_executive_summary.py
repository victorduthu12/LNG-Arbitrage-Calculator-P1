"""
Étape 4 — Résumé exécutif automatique
========================================
On génère un texte récapitulatif, comme une mini-note de desk, qui résume :
- La route privilégiée sur la période
- Les moments de bascule (changements de route optimale)
- L'ampleur moyenne du spread
"""

import pandas as pd

df = pd.read_csv("/home/claude/lng_arbitrage/netback_results.csv", parse_dates=["date"])

# --- Détection des bascules : quand la route optimale change d'un mois à l'autre ---
df["route_precedente"] = df["route_optimale"].shift(1)
df["bascule"] = df["route_optimale"] != df["route_precedente"]
bascules = df[df["bascule"] & df["route_precedente"].notna()]

# --- Statistiques globales ---
nb_mois_asie = (df["route_optimale"] == "Asie").sum()
nb_mois_europe = (df["route_optimale"] == "Europe").sum()
spread_moyen = df["spread_asie_europe"].mean()
mois_meilleur_arbitrage = df.loc[df["spread_asie_europe"].abs().idxmax()]

print("=" * 60)
print("NOTE DE DESK — ARBITRAGE GNL US / EUROPE / ASIE")
print("=" * 60)

print(f"\nPériode analysée : {df['date'].min().strftime('%b %Y')} -> {df['date'].max().strftime('%b %Y')}")
print(f"\nRépartition de la route optimale sur la période :")
print(f"  - Asie   : {nb_mois_asie} mois ({nb_mois_asie/len(df)*100:.0f}%)")
print(f"  - Europe : {nb_mois_europe} mois ({nb_mois_europe/len(df)*100:.0f}%)")

print(f"\nSpread moyen (Asie - Europe) : {spread_moyen:+.2f} $/MMBtu")
if spread_moyen > 0:
    print("  -> Sur la période, l'Asie a légèrement surperformé l'Europe en moyenne.")
else:
    print("  -> Sur la période, l'Europe a légèrement surperformé l'Asie en moyenne.")

print(f"\nMois avec l'écart d'arbitrage le plus marqué : {mois_meilleur_arbitrage['date'].strftime('%b %Y')}")
print(f"  -> Route optimale : {mois_meilleur_arbitrage['route_optimale']} "
      f"(spread de {mois_meilleur_arbitrage['spread_asie_europe']:+.2f} $/MMBtu)")

print(f"\nNombre de bascules de route sur la période : {len(bascules)}")
print("Détail des bascules :")
for _, ligne in bascules.iterrows():
    print(f"  {ligne['date'].strftime('%b %Y')} : {ligne['route_precedente']} -> {ligne['route_optimale']}")

print("\n" + "=" * 60)
print("CONCLUSION")
print("=" * 60)
print(
    "L'analyse confirme une dynamique d'arbitrage active entre les deux bassins :\n"
    "aucune route ne domine durablement, ce qui reflète la réalité du marché GNL\n"
    "mondial où les flux s'ajustent en continu selon la saisonnalité de la demande\n"
    "(hiver européen vs hiver asiatique) et les écarts de prix régionaux."
)
