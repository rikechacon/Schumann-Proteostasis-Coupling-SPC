"""
EJECUCIÓN: Análisis Adicionales para Fortalecer el Paper
=========================================================
Validación de frecuencia, convergencia y robustez.
"""

import sys
sys.path.insert(0, 'src')
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.model import SchumannProteostasisModel
from src.frequency_validation import sweep_frequency, analyze_frequency_specificity
from src.initial_condition_sensitivity import analyze_convergence
from src.robustness_analysis import robustness_sweep, compute_robustness_metric

print("\n" + "="*70)
print("ANÁLISIS ADICIONALES: Fortaleciendo Evidencia Científica")
print("="*70 + "\n")

os.makedirs('results/processed', exist_ok=True)
os.makedirs('results/figures', exist_ok=True)

# ============================================================================
# ANÁLISIS A: Validación de Frecuencia
# ============================================================================

print("🔬 ANÁLISIS A: Especificidad de Frecuencia")
print("-" * 50)

freq_results = sweep_frequency(
    frequency_range=[1.0, 3.0, 5.0, 7.83, 10.0, 13.0, 15.0, 20.0, 30.0],
    base_params={'eta': 0.5, 'sigma': 0.3, 'T': 5.0, 'dt': 0.001},
    n_trials=30,
    output_file='results/processed/frequency_validation.csv'
)

# Visualizar
plt.figure(figsize=(8, 5))
plt.plot(freq_results['frequency'], freq_results['mfpt'], 'bo-', linewidth=2, markersize=6)
# Marcar Schumann
schumann_idx = freq_results['is_schumann'].idxmax()
plt.plot(freq_results.loc[schumann_idx, 'frequency'], 
         freq_results.loc[schumann_idx, 'mfpt'], 
         'r*', markersize=20, label='Schumann 7.83 Hz')
plt.xlabel('Frecuencia de forzamiento (Hz)')
plt.ylabel('MFPT (s)')
plt.title('Especificidad de Frecuencia: ¿Es Schumann especial?')
plt.axvline(x=7.83, color='r', linestyle='--', alpha=0.3)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('results/figures/07_frequency_specificity.png', dpi=300)
plt.close()

# Analizar
freq_analysis = analyze_frequency_specificity(freq_results)
print(f"\n📊 Resultado: MFPT en Schumann = {freq_analysis['mfpt_schumann']:.2f}s")
print(f"   MFPT promedio en otras frecuencias = {freq_analysis['mfpt_others_mean']:.2f} ± {freq_analysis['mfpt_others_std']:.2f}s")
print(f"   Factor de mejora: {freq_analysis['enhancement_factor']:.2f}x")
print(f"   ¿Schumann es óptimo? {'✅ SÍ' if freq_analysis['schumann_is_optimal'] else '❌ No'}\n")

# ============================================================================
# ANÁLISIS B: Sensibilidad a Condiciones Iniciales
# ============================================================================

print("🔬 ANÁLISIS B: Convergencia desde Condiciones Iniciales")
print("-" * 50)

convergence_results = analyze_convergence(
    initial_conditions=np.linspace(-2.5, 2.5, 11),
    base_params={'eta': 0.5, 'sigma': 0.3, 'T': 10.0, 'dt': 0.001},
    simulation_time=10.0,
    n_trials=20
)
convergence_results.to_csv('results/processed/convergence_analysis.csv', index=False)

# Visualizar
plt.figure(figsize=(8, 5))
plt.plot(convergence_results['x0'], convergence_results['fraction_healthy'], 'go-', linewidth=2)
plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
plt.xlabel('Condición inicial x₀')
plt.ylabel('Fracción que converge a estado saludable')
plt.title('Sensibilidad a Condiciones Iniciales')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/figures/08_convergence_sensitivity.png', dpi=300)
plt.close()

healthy_frac = convergence_results['fraction_healthy'].mean()
print(f"\n📊 Resultado: Fracción promedio convergente a saludable = {healthy_frac:.1%}")
print(f"   El sistema muestra {'buena' if healthy_frac > 0.6 else 'moderada'} independencia de condiciones iniciales\n")

# ============================================================================
# ANÁLISIS C: Robustez Paramétrica
# ============================================================================

print("🔬 ANÁLISIS C: Robustez ante Variabilidad de Parámetros")
print("-" * 50)

# Probar robustez en eta y sigma
robustness_results = {}

for param, nominal in [('eta', 0.5), ('sigma', 0.3)]:
    print(f"\n   Variando {param} ±10% alrededor de {nominal}...")
    results = robustness_sweep(
        param_name=param,
        nominal_value=nominal,
        variation_percent=10,
        n_samples=15,
        base_params={'T': 5.0, 'dt': 0.001},
        n_trials=20
    )
    results.to_csv(f'results/processed/robustness_{param}.csv', index=False)
    
    metric = compute_robustness_metric(results, param)
    robustness_results[param] = metric
    
    # Visualizar
    plt.figure(figsize=(6, 4))
    plt.plot(results[param], results['mfpt'], 'bo-')
    plt.xlabel(f'{param}')
    plt.ylabel('MFPT (s)')
    plt.title(f'Robustez: MFPT vs {param}')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'results/figures/09_robustness_{param}.png', dpi=300)
    plt.close()
    
    print(f"   Coeficiente de variación: {metric['coefficient_of_variation']:.3f}")
    print(f"   ¿Robusto? {'✅ SÍ (CV < 0.3)' if metric['robust'] else '⚠️ Sensible'}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "="*70)
print("✅ ANÁLISIS ADICIONALES COMPLETADOS")
print("="*70)

print(f"\n📊 Archivos generados:")
print(f"   results/processed/")
print(f"   ├─ frequency_validation.csv")
print(f"   ├─ convergence_analysis.csv")
print(f"   ├─ robustness_eta.csv")
print(f"   └─ robustness_sigma.csv")
print(f"   results/figures/")
print(f"   ├─ 07_frequency_specificity.png")
print(f"   ├─ 08_convergence_sensitivity.png")
print(f"   ├─ 09_robustness_eta.png")
print(f"   └─ 09_robustness_sigma.png")

print(f"\n💡 Hallazgos para el paper:")
print(f"   1. Especificidad: Schumann {'MUESTRA' if freq_analysis['schumann_is_optimal'] else 'no muestra'} ventaja significativa")
print(f"   2. Convergencia: Sistema {'robusto' if healthy_frac > 0.6 else 'sensible'} a condiciones iniciales")
print(f"   3. Robustez: Parámetros {'estables' if all(r['robust'] for r in robustness_results.values()) else 'variables'} ante ±10% variación")

print(f"\n🎯 Estos resultados fortalecen:")
print(f"   • Validez del modelo frente a controles negativos")
print(f"   • Generalidad de las predicciones")
print(f"   • Confiabilidad para aplicaciones futuras")

print("\n" + "="*70 + "\n")
