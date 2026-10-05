# In-Silico Molecular Docking & ADMET Screening of Phytochemicals Targeting *Leptospira* LipL32

![Target](https://img.shields.io/badge/Target-LipL32_Lipoprotein-blue)
![Method](https://img.shields.io/badge/Methodology-Molecular_Docking_%7C_ADMET-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

## Project Overview
Leptospirosis is a widespread zoonotic infectious disease caused by pathogenic spirochetes of the genus *Leptospira*. LipL32 is the major outer membrane lipoprotein found exclusively in pathogenic *Leptospira* species, playing a crucial role during infection and host-pathogen interactions, making it an ideal therapeutic target.

This computational project evaluates a library of 44 phytochemicals sourced from medicinal plants (notably *Thymus vulgaris*, *Satureja*, and *Mentha*) to identify potential small-molecule inhibitors of the LipL32 protein.

---

## Computational Pipeline & Methodology

1. Target Preparation:
   * Target protein: LipL32 outer membrane lipoprotein.
   * Structure processing: Polar hydrogen addition, Gasteiger charges assignment, and solvation parameters setup.

2. Ligand Library Construction:
   * Sourced 44 phytochemical bioactive compounds.
   * Ligand energy minimization and geometry optimization.

3. Molecular Docking (AutoDock 4):
   * Grid box configured to encompass putative binding pockets.
   * Lamarckian Genetic Algorithm (LGA) deployed with 24 independent docking runs per compound to ensure conformational sampling and reproducibility.
   * Analysis of binding free energies ($\Delta G$), inhibition constants ($K_i$), and hydrogen bonding / hydrophobic contact profiles.

4. Pharmacokinetics & Toxicity (ADMET):
   * Evaluation of drug-likeness (Lipinski's Rule of Five, Veber's rule).
   * Pharmacokinetic prediction: GI absorption, Blood-Brain Barrier (BBB) permeation, and toxicity filters.

---

## Key Findings & Top Lead Compounds

Among the 44 screened compounds, several monoterpenes and phenolics exhibited favorable binding affinities and clean drug-likeness profiles:
* Carvacrol: Strong localized interaction with favorable binding thermodynamics and high intestinal permeability.
* Menthone: Favorable docking scores and compliance with standard pharmacokinetic properties.

---

### Python Screening & Data Automation Pipeline

To automate the multi-parametric screening of raw docking and ADMET datasets (docking_and_admet_results.xlsx), an automated screening script is integrated:
```
# Run lead screening and visualization pipeline
python lipl32_lead_screening.py
```
* Data Cleaning & Standardization: Cleans binding energy metrics, Ki values, and pharmacokinetic properties.
* Lead Filtering: Applies strict thresholding (Binding Energy <= -6.0 kcal/mol, HIA >= 80%, Carcinogenicity = Negative).
* Visualization: Generates comparative multi-panel plots (lipl32_screening_summary.png) showcasing binding affinities and inhibition constants.

---

## Repository Structure
```text
leptospirosis-lipl32-docking-screening/
├── README.md                      # Comprehensive project documentation
├── docking_and_admet_results.xlsx # Complete docking & ADMET raw dataset (40 compounds)
└── lipl32_lead_screening.py       # Python pipeline for data cleaning, filtering & plotting
```
---
## Author & Project Background
- Researcher & Pipeline Developer: Taban Tavanmand *(documented as Atefeh Tavanmand in original academic course records)*
- Original Research & Docking Campaign: BioCamp (Winter 2021) – *Advanced Industrial Drug Design & Bioinformatics Pipeline*
- Automation & Scripting: Python-based screening pipeline implemented for automated post-docking analysis and lead compound prioritization.
- Research Focus: Structural Bioinformatics, In-Silico Molecular Docking, ADMET Profiling & Computational Screening Pipelines


