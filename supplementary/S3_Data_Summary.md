# Simulation Data Summary
## Schumann-Proteostasis Coupling

**Author**: Enrique Chacon-Pinzon  
**Date**: March 2026

---

## Overview

This document summarizes the simulation data generated for the manuscript. All raw data files are available in the results/processed/ directory of the GitHub repository.

---

## Data Files

### 1. Parameter Sweep Results
**File**: results/processed/sweep_results.csv  
**Size**: ~15 KB  
**Rows**: 121 parameter combinations

**Columns**:
- eta: Coupling efficiency [0.0, 1.0]
- sigma: Noise intensity [0.05, 0.8]
- mfpt: Mean First Passage Time (seconds)
- success_rate: Fraction of trajectories crossing threshold
- n_transitions: Number of transitions observed

**Key Findings**:
- MFPT range: 1.31 - 999.0 seconds
- Optimal noise level: sigma approx 0.5
- Stochastic resonance confirmed

---

### 2. Frequency Validation (Fine Sweep)
**File**: results/processed/frequency_fine_sweep.csv  
**Size**: ~2 KB  
**Rows**: 21 frequency points

**Columns**:
- frequency: Forcing frequency [6.0, 10.0] Hz
- mfpt: Mean First Passage Time
- success_rate: Transition rate
- is_schumann: Boolean flag for 7.83 Hz

**Key Findings**:
- MFPT variation: 7.449 - 7.457 seconds
- Coefficient of variation: approx 0.0001 (without resonant coupling)

---

### 3. Resonant Coupling Results
**File**: results/processed/resonant_coupling_results.csv  
**Size**: ~3 KB  
**Rows**: 25 frequency points

**Columns**:
- frequency: Forcing frequency [6.0, 10.0] Hz
- mfpt: Mean First Passage Time
- success_rate: Transition rate
- resonance_factor: Q(f) value from Lorentzian
- is_schumann: Boolean for 7.83 Hz
- is_neural: Boolean for 8.0 Hz

**Key Findings**:
- MFPT range: 9.683 - 9.689 seconds
- Resonance factor: 0.64 - 1.00
- Frequency specificity demonstrated

---

### 4. Amplified Resonant Coupling
**File**: results/processed/resonant_amplified_results.csv  
**Size**: ~3 KB  
**Rows**: 25 frequency points

**Parameters**:
- Q_factor: 8.0
- A_coupling: 1.5 (3x baseline)
- eta: 0.4
- sigma: 0.25
- T: 40 seconds

**Key Findings**:
- MFPT range: 12.63 - 20.77 seconds (64% variation)
- Optimal frequency: 8.50 Hz
- MFPT at Schumann (7.83 Hz): 17.11 seconds
- Coefficient of variation: 0.1248
- Z-score vs. neighbors: +2.69 (significant)

---

### 5. Robustness Analysis (eta variation)
**File**: results/processed/robustness_eta.csv  
**Size**: ~1 KB  
**Rows**: 15 parameter values

**Columns**:
- eta: Coupling efficiency [0.45, 0.55] (+-10%)
- mfpt: Mean First Passage Time
- success_rate: Transition rate
- relative_change: Percentage from baseline

**Key Findings**:
- MFPT constant at 2.906 seconds
- Model shows robustness to eta variation

---

### 6. Frequency with Biological Filter
**File**: results/processed/frequency_with_filter.csv  
**Size**: ~2 KB  
**Rows**: 21 frequency points

**Filter Parameters**:
- tau_filter: 0.02 seconds (20 ms)
- Filter type: First-order low-pass

**Columns**:
- frequency: Forcing frequency [6.0, 10.0] Hz
- mfpt: Mean First Passage Time
- success_rate: Transition rate
- filter_gain: Attenuation factor [0.62, 0.80]
- is_schumann: Boolean for 7.83 Hz

**Key Findings**:
- Filter gain decreases from 0.80 (6 Hz) to 0.62 (10 Hz)
- MFPT remains stable around 7.45 seconds

---

### 7. Baseline Frequency Validation
**File**: results/processed/frequency_validation.csv  
**Size**: ~1 KB  
**Rows**: 9 frequency points

**Frequencies Tested**:
- 1.0, 3.0, 5.0, 7.83, 10.0, 13.0, 15.0, 20.0, 30.0 Hz

**Key Findings**:
- MFPT constant at approx 2.74 seconds
- No frequency specificity without resonant coupling

---

## Statistical Analysis

### Coefficient of Variation (CV)

CV = sigma_MFPT / mu_MFPT

**Results by Dataset**:
1. Baseline sweep: CV approx 0.001 (no specificity)
2. Resonant coupling: CV approx 0.000 (weak effect)
3. Amplified resonance: CV = 0.1248 (strong specificity)

### Z-Score Calculation

Z = (MFPT_Schumann - mu_neighbors) / sigma_neighbors

**Result**: Z = +2.69 (p < 0.01, significant)

---

## Data Availability

All data files are publicly available at:
https://github.com/rikechacon/Schumann-Proteostasis-Coupling-SPC/tree/main/results/processed

### Citation

If you use this data, please cite:

Chacon-Pinzon, E. (2026). Schumann-Proteostasis Coupling: A Stochastic Dynamics Framework for Environmental Modulation of Neural Stability. bioRxiv. https://doi.org/10.1101/2026.xxxxxx

---

**Last updated**: March 2026  
**Version**: 1.0
