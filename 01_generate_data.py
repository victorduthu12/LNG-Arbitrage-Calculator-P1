"""
Étape 1 — Génération de données de prix simulées réalistes
============================================================
On simule 24 mois de prix mensuels pour les 3 références mondiales du gaz/GNL :
- Henry Hub (US)   : point de départ, prix du gaz américain avant liquéfaction
- TTF (Europe)     : prix du gaz européen (Title Transfer Facility, Pays-Bas)
- JKM (Asie)       : prix du GNL livré en Asie (Japan-Korea Marker)

On simule volontairement avec :
- Une tendance saisonnière (prix plus hauts en hiver, demande de chauffage)
- Du bruit aléatoire réaliste (les marchés ne sont jamais parfaitement lisses)
- Un spread JKM/TTF cohérent avec les ordres de grandeur réels du marché
"""

import numpy as np
import pandas as pd

np.random.seed(42)  # pour que les résultats soient reproductibles à chaque exécution

# 24 mois de données, démarrage janvier 2025
dates = pd.date_range(start="2025-01-01", periods=24, freq="MS")

# Saisonnalité : on modélise un pic hiver (mois 0,1,11,12,13,23 -> hiver) avec un cosinus
mois_de_lannee = dates.month
saisonnalite = 1.0 + 0.25 * np.cos((mois_de_lannee - 1) * (2 * np.pi / 12))
# cos atteint son max en janvier (mois=1) -> prix plus hauts en hiver, plus bas en été

# --- Henry Hub (US) — en $/MMBtu, ordre de grandeur réel : 2 à 4.5 $/MMBtu ---
base_henry_hub = 3.0
bruit_hh = np.random.normal(0, 0.3, size=len(dates))
henry_hub = base_henry_hub * saisonnalite + bruit_hh
henry_hub = np.clip(henry_hub, 1.5, None)  # le prix ne descend pas sous 1.5 (plancher réaliste)

# --- TTF (Europe) — en $/MMBtu, généralement 2 à 3x Henry Hub ---
base_ttf = 9.5
bruit_ttf = np.random.normal(0, 0.8, size=len(dates))
ttf = base_ttf * saisonnalite + bruit_ttf
ttf = np.clip(ttf, 5.0, None)

# --- JKM (Asie) — en $/MMBtu, historiquement proche ou légèrement au-dessus du TTF ---
base_jkm = 10.0
bruit_jkm = np.random.normal(0, 0.9, size=len(dates))
jkm = base_jkm * saisonnalite + bruit_jkm
jkm = np.clip(jkm, 5.5, None)

# Construction du tableau de données (DataFrame = la structure centrale de Pandas,
# l'équivalent d'une feuille Excel mais manipulable par code)
df = pd.DataFrame({
    "date": dates,
    "henry_hub_us": henry_hub.round(2),
    "ttf_europe": ttf.round(2),
    "jkm_asie": jkm.round(2),
})

df.to_csv("/home/claude/lng_arbitrage/prix_simules.csv", index=False)

print("Aperçu des données générées :")
print(df.head(12))
print(f"\nFichier sauvegardé : prix_simules.csv ({len(df)} lignes)")
