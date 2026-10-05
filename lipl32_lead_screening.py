"""
Multi-Parameter Screening & Lead Optimization Pipeline for Leptospirosis LipL32
Author: Taban Tavanmand
Description:
    Automated Python pipeline to screen LipL32 docking and ADMET profiles.
    Filters hits based on thermodynamic affinity (binding energy <= -6.0 kcal/mol),
    high gastrointestinal absorption (HIA >= 80%), and safety profiles (non-carcinogenic).
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def clean_and_load_data(file_path):
    """Loads the dataset and cleans duplicate headers and empty rows."""
    df = pd.read_excel(file_path)
    
    # Drop rows where 'ligand' is null or repeats header name
    df = df.dropna(subset=['ligand'])
    df = df[df['ligand'].astype(str).str.lower() != 'ligand'].copy()
    
    # Clean numeric columns (handle asterisks if present)
    numeric_cols = ['energy binding', 'ki', 'HIA', 'Bioavalabilitiy']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('*', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

def run_screening_pipeline(df, energy_threshold=-6.0, hia_threshold=80.0):
    """Applies multi-parametric biological filters."""
    # Filter 1: Binding energy cutoff
    affinity_filter = df['energy binding'] <= energy_threshold
    
    # Filter 2: Intestinal absorption
    absorption_filter = df['HIA'] >= hia_threshold
    
    # Filter 3: Carcinogenicity safety profile
    safety_filter = df['Carcino-Mouse'].astype(str).str.strip().str.lower() == 'negative'
    
    screened_df = df[affinity_filter & absorption_filter & safety_filter].copy()
    screened_df = screened_df.sort_values(by='energy binding', ascending=True)
    
    return screened_df

def plot_screening_results(df, screened_df, output_img="lipl32_screening_summary.png"):
    """Generates comparative visualizations of binding energies and ADMET safety."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Top Candidates Binding Energy
    top_candidates = screened_df.head(8)
    bars = ax1.bar(top_candidates['ligand'], top_candidates['energy binding'], 
                   color='#2b5c8f', edgecolor='black', alpha=0.85)
    ax1.set_title("Top Screened Leads: LipL32 Binding Affinity", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Ligand Code", fontsize=10)
    ax1.set_ylabel("Binding Energy (kcal/mol)", fontsize=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f"{height:.2f}",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, -12),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, color='white', fontweight='bold')
        
    # Plot 2: Binding Energy vs Inhibition Constant (Ki)
    scatter = ax2.scatter(df['energy binding'], df['ki'], 
                          c=df['HIA'], cmap='viridis', 
                          s=70, edgecolor='black', alpha=0.75)
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label("Human Intestinal Absorption (HIA %)", fontsize=10)
    
    ax2.set_title("Thermodynamic Affinity vs Inhibition Constant (Ki)", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Binding Energy (kcal/mol)", fontsize=10)
    ax2.set_ylabel("Inhibition Constant Ki (uM)", fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(output_img, dpi=300)
    print(f"[+] Visualization exported successfully: {output_img}")
    plt.show()

def main():
    # File path for raw docking/ADMET dataset
    excel_file = "docking_and_admet_results.xlsx"
    
    if not os.path.exists(excel_file):
        alt_names = ["docking_and_admet_results.xlsx.xlsx", "www.xlsx"]
        for alt in alt_names:
            if os.path.exists(alt):
                excel_file = alt
                break
              print(f"[*] Processing dataset: {excel_file}")
    df = clean_and_load_data(excel_file)
    print(f"[*] Total compounds evaluated: {len(df)}")
    
    screened_df = run_screening_pipeline(df)
    print(f"[+] Compounds passing multi-parameter criteria: {len(screened_df)}")
    
    # Save top screened leads to CSV
    output_csv = "top_screened_leads.csv"
    screened_df.to_csv(output_csv, index=False)
    print(f"[+] Screened results saved to: {output_csv}")
    
    # Generate visualization
    plot_screening_results(df, screened_df)

if name == "main":
    main()
