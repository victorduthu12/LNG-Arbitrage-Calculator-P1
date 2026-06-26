"""
Étape 3 — Visualisation
=========================
Deux graphiques :
1. Évolution des netbacks Europe vs Asie dans le temps (la courbe que tout trader
   regarderait pour décider où envoyer ses cargaisons)
2. Le spread Asie-Europe avec une ligne à zéro, pour visualiser clairement
   les moments de bascule entre les deux routes
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("/home/claude/lng_arbitrage/netback_results.csv", parse_dates=["date"])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

# --- Graphique 1 : Netback Europe vs Asie ---
ax1.plot(df["date"], df["netback_europe"], label="Netback Europe (TTF)", 
         color="#2563eb", linewidth=2, marker="o", markersize=4)
ax1.plot(df["date"], df["netback_asie"], label="Netback Asie (JKM)", 
         color="#dc2626", linewidth=2, marker="o", markersize=4)
ax1.set_ylabel("Netback ($/MMBtu)")
ax1.set_title("Arbitrage GNL — Netback Europe vs Asie (cargaison US)", fontsize=13, fontweight="bold")
ax1.legend(loc="upper left")
ax1.grid(alpha=0.3)
ax1.axhline(0, color="grey", linewidth=0.8)

# --- Graphique 2 : Spread Asie - Europe (la "boussole" de décision) ---
couleurs = ["#dc2626" if v > 0 else "#2563eb" for v in df["spread_asie_europe"]]
ax2.bar(df["date"], df["spread_asie_europe"], color=couleurs, width=20)
ax2.axhline(0, color="black", linewidth=1)
ax2.set_ylabel("Spread Asie - Europe ($/MMBtu)")
ax2.set_title("Spread d'arbitrage — Rouge = Asie plus rentable, Bleu = Europe plus rentable", 
              fontsize=11)
ax2.grid(alpha=0.3)

ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/lng_arbitrage_chart.png", dpi=150, bbox_inches="tight")
print("Graphique sauvegardé : lng_arbitrage_chart.png")
