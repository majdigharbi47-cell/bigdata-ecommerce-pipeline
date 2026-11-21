import os
import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# FIGURE 1 : Top Pays par Revenue (Barplot horizontal)
df1 = pd.read_csv(
    RESULTS_DIR / "revenue_by_country.tsv",
    sep="\t",
    header=None,
    names=["Country", "Revenue"],
)
df1["Revenue"] = pd.to_numeric(df1["Revenue"], errors="coerce")
df1 = df1.dropna(subset=["Country", "Revenue"])
df1 = df1.sort_values("Revenue", ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=df1, x="Revenue", y="Country", hue="Country", palette="viridis", legend=False)
plt.title("Top 10 Pays par Chiffre d'Affaires", fontsize=14, fontweight="bold")
plt.xlabel("Revenue (€)", fontsize=12)
plt.ylabel("Pays", fontsize=12)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "top_countries_revenue.png", dpi=300, bbox_inches="tight")
plt.close()

# FIGURE 2 : Top Produits (Parsing spécial pour le format texte)
products = []
quantities = []
with (RESULTS_DIR / "top_products.tsv").open("r", encoding="utf-8") as f:
    for line in f:
        # Regex pour parser : "1. NOM --> 12345 unites"
        match = re.match(r'^\d+\.\s+(.+?)\s+-->\s+(\d+)', line.strip())
        if match:
            products.append(match.group(1).strip())
            quantities.append(int(match.group(2)))

df2 = pd.DataFrame({"Product": products, "Quantity": quantities})

plt.figure(figsize=(12, 8))
if df2.empty:
    plt.text(0.5, 0.5, "Aucune donnée produit trouvée", ha="center", va="center")
else:
    sns.barplot(data=df2, x="Quantity", y="Product", hue="Product", palette="rocket", legend=False)
plt.title("Top 10 Produits les Plus Vendus", fontsize=14, fontweight="bold")
plt.xlabel("Quantité vendue", fontsize=12)
plt.ylabel("Produit", fontsize=12)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "top_products.png", dpi=300, bbox_inches="tight")
plt.close()

# FIGURE 3 : Matrice de Confusion (ML)
df3 = pd.read_csv(RESULTS_DIR / "predictions.csv")
actual_column = "HighValueCustomer" if "HighValueCustomer" in df3.columns else "actual"
if actual_column not in df3.columns or "prediction" not in df3.columns:
    raise ValueError(
        "predictions.csv doit contenir les colonnes 'prediction' et "
        "'HighValueCustomer' (ou 'actual')"
    )

confusion = pd.crosstab(
    df3[actual_column],
    df3["prediction"],
    rownames=["Réel"],
    colnames=["Prédit"],
)

plt.figure(figsize=(8, 6))
sns.heatmap(
    confusion,
    annot=True,
    fmt="d",
    cmap="Blues",
    cbar_kws={"label": "Nombre de clients"},
)
plt.title(
    "Matrice de Confusion - Régression Logistique",
    fontsize=14,
    fontweight="bold",
)
plt.tight_layout()
plt.savefig("results/figures/confusion_matrix.png", dpi=300)
plt.close()

print("✅ Les 3 figures ont été générées dans results/figures/")