"""
LipL32 Phytochemical Screening & Docking Analysis Pipeline
===========================================================
Automated screening, ranking, and visualization pipeline for AutoDock 
binding affinities targeting Leptospirosis LipL32 outer membrane protein.

Author: Taban Tavanmand
License: MIT
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def find_dataset():
    """Locate the docking results dataset dynamically."""
    candidates = [
        "docking_and_admet_results.xlsx",
        "docking_and_admet_results.xlsx.xlsx",
        "www.xlsx",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    xlsx_files = glob.glob("*.xlsx")
    if xlsx_files:
        return xlsx_files[0]
    raise FileNotFoundError(
        "Could not find an Excel dataset (.xlsx) in the working directory."
    )


def identify_columns(df):
    """Dynamically detect compound and binding energy column headers."""
    norm_cols = {col: str(col).strip().lower() for col in df.columns}

    # Detect ligand/compound column
    lig_col = None
    for orig, norm in norm_cols.items():
        if any(k in norm for k in ["ligand", "compound", "name", "molecule", "phytochemical"]):
            lig_col = orig
            break
    if not lig_col:
        lig_col = df.columns[0]

    # Detect binding energy column
    energy_col = None
    for orig, norm in norm_cols.items():
        if "energy" in norm or "affinity" in norm or "kcal" in norm or "binding" in norm:
            energy_col = orig
            break
    if not energy_col:
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                energy_col = col
                break

    return lig_col, energy_col


def run_screening_pipeline(energy_threshold=-6.0):
    """Execute filtering, lead selection, CSV export, and figure rendering."""
    filepath = find_dataset()
    print(f"[*] Loading dataset: {filepath}")
    df = pd.read_excel(filepath)

    lig_col, energy_col = identify_columns(df)
    print(f"[*] Detected columns -> Ligand: '{lig_col}', Energy: '{energy_col}'")

    # Clean numeric binding energies
    df[energy_col] = pd.to_numeric(df[energy_col], errors="coerce")
    cleaned_df = df.dropna(subset=[lig_col, energy_col]).copy()

    # Filter by binding affinity threshold
    screened_leads = cleaned_df[cleaned_df[energy_col] <= energy_threshold].copy()
    screened_leads = screened_leads.sort_values(by=energy_col, ascending=True)

    print(f"[*] Total screened leads meeting criteria (<= {energy_threshold} kcal/mol): {len(screened_leads)}")

    # Export top screened leads
    output_csv = "top_screened_leads.csv"
    screened_leads.to_csv(output_csv, index=False)
    print(f"[+] Saved screened leads to: {output_csv}")

    # Plotting
    sns.set_theme(style="whitegrid", palette="muted")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    plot_data = screened_leads.head(15)
    barplot = sns.barplot(
        data=plot_data,
        x=energy_col,
        y=lig_col,
        palette="viridis",
        ax=ax
    )

    ax.set_title(
        "LipL32 Target Screening: Lead Phytochemicals by Binding Free Energy",
        fontsize=13,
        fontweight="bold",
        pad=15
    )
    ax.set_xlabel("Binding Affinity (kcal/mol)", fontsize=11, labelpad=10)
    ax.set_ylabel("Phytochemical Compound", fontsize=11)
    ax.axvline(energy_threshold, color="crimson", linestyle="--", linewidth=1.2, label=f"Cutoff ({energy_threshold} kcal/mol)")
    ax.legend(loc="lower right")

    plt.tight_layout()
    output_png = "lipl32_screening_summary.png"
    plt.savefig(output_png, bbox_inches="tight")
    plt.close()
    print(f"[+] Figure rendered successfully: {output_png}")


if name == "main":
    run_screening_pipeline()
