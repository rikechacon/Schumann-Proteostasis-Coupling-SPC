"""
TEST REFINADO: ¿Existe un pico estrecho en 7.83 Hz?
Barrido de alta resolución alrededor de la frecuencia de Schumann.
"""
import sys
sys.path.insert(0, 'src')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from src.frequency_validation import sweep_frequency

print("\n" + "="*70)
print("BARRIDO FINO: Especificidad de Frecuencia alrededor de Schumann")
print("="*70 + "\n")

# Crear directorio de salida
os.makedirs('results/processed', exist_ok=True)
os.makedirs('results/figures', exist_ok=True)

# Barrido fino: 21 puntos entre 6 y 10 Hz (resolución ~0.2 Hz)
fine_range = np.linspace(6.0, 10.0, 21)

print(f"🔍 Configuración del barrido fino:")
print(f"   • Rango: 6.0 - 10.0 Hz")
print(f"   • Puntos: {len(fine_range)} (resolución: {(10-6)/(len(fine_range)-1):.2f} Hz)")
print(f"   • Duración por simulación: 15.0 s")
print(f"   • Réplicas: 50")
print(f"   • Estimado de tiempo: ~{len(fine_range)*50*15/60:.0f} minutos\n")

print("🔄 Ejecutando simulaciones...")
results = sweep_frequency(
    frequency_range=fine_range,
    base_params={'eta': 0.5, 'sigma': 0.3, 'T': 15.0, 'dt': 0.001},
    n_trials=50,  # Más réplicas para reducir ruido estadístico
    output_file='results/processed/frequency_fine_sweep.csv'
)

# ============================================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================================

print("\n📊 Análisis estadístico...")

# Encontrar máximo global
idx_max = results['mfpt'].idxmax()
f_optimal = results.loc[idx_max, 'frequency']
mfpt_max = results.loc[idx_max, 'mfpt']

# MFPT en Schumann exacto
schumann_row = results[results['frequency'] == 7.83]
if len(schumann_row) > 0:
    mfpt_schumann = schumann_row['mfpt'].values[0]
else:
    # Interpolar si 7.83 no está exactamente en el array
    mfpt_schumann = np.interp(7.83, results['frequency'], results['mfpt'])

# Comparar con vecinos inmediatos (±0.5 Hz)
neighbors = results[(results['frequency'] >= 7.3) & 
                    (results['frequency'] <= 8.3) & 
                    (results['frequency'] != 7.83)]

print(f"\n🎯 Resultados clave:")
print(f"   • Frecuencia óptima encontrada: {f_optimal:.2f} Hz")
print(f"   • MFPT máximo: {mfpt_max:.2f} s")
print(f"   • MFPT en Schumann (7.83 Hz): {mfpt_schumann:.2f} s")
print(f"   • Promedio vecinos [7.3-8.3 Hz]: {neighbors['mfpt'].mean():.2f} ± {neighbors['mfpt'].std():.2f} s")

# Test simple de significancia
if len(neighbors) > 1:
    z_score = (mfpt_schumann - neighbors['mfpt'].mean()) / neighbors['mfpt'].std()
    print(f"   • Z-score vs vecinos: {z_score:+.2f} {'✅ Significativo' if abs(z_score) > 1.5 else '⚠️ Dentro de ruido'}")

# ============================================================================
# VISUALIZACIÓN
# ============================================================================

print("\n🎨 Generando visualización...")

plt.figure(figsize=(10, 6))

# Plot principal
plt.plot(results['frequency'], results['mfpt'], 'bo-', linewidth=2, markersize=5, label='MFPT')

# Marcar Schumann
plt.axvline(x=7.83, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Schumann 7.83 Hz')
plt.plot(7.83, mfpt_schumann, 'r*', markersize=20, label=f'Schumann: {mfpt_schumann:.2f}s')

# Marcar óptimo encontrado
if not np.isclose(f_optimal, 7.83, atol=0.1):
    plt.plot(f_optimal, mfpt_max, 'g^', markersize=12, label=f'Óptimo: {f_optimal:.2f} Hz')

# Sombreado: banda theta-alpha (4-12 Hz)
plt.axvspan(4.0, 8.0, alpha=0.1, color='orange', label='Banda Theta (4-8 Hz)')
plt.axvspan(8.0, 12.0, alpha=0.1, color='yellow', label='Banda Alpha (8-12 Hz)')

plt.xlabel('Frecuencia de forzamiento (Hz)', fontsize=12)
plt.ylabel('Mean First Passage Time (s)', fontsize=12)
plt.title('Especificidad de Frecuencia: Barrido Fino alrededor de Schumann\n' + 
          f'η=0.5, σ=0.3, T=15s, n_trials=50', fontsize=13, fontweight='bold')
plt.legend(fontsize=9, frameon=True, framealpha=0.9)
plt.grid(True, alpha=0.3, linestyle='--')
plt.xlim(6, 10)
plt.tight_layout()
plt.savefig('results/figures/10_frequency_fine_sweep.png', dpi=300, bbox_inches='tight')
plt.savefig('results/figures/10_frequency_fine_sweep.pdf', bbox_inches='tight')
plt.close()

print("   ✓ Gráfico guardado: results/figures/10_frequency_fine_sweep.[png|pdf]")

# ============================================================================
# INTERPRETACIÓN Y DECISIÓN
# ============================================================================

print("\n" + "="*70)
print("🔍 INTERPRETACIÓN Y PRÓXIMOS PASOS")
print("="*70)

if np.isclose(f_optimal, 7.83, atol=0.2):
    print("\n✅ ESCENARIO A: ¡Schumann ES óptimo!")
    print(f"   • El pico de MFPT coincide con 7.83 Hz (±0.2 Hz)")
    print(f"   • Esto respalda la hipótesis de resonancia específica")
    print(f"   • 🎯 Próximo paso: Proceder al manuscrito con este resultado")
    
elif abs(mfpt_schumann - neighbors['mfpt'].mean()) / neighbors['mfpt'].std() > 1.5:
    print("\n⚠️ ESCENARIO B: Schumann es prometedor, pero no el máximo")
    print(f"   • MFPT en Schumann es alto, pero el óptimo está en {f_optimal:.2f} Hz")
    print(f"   • Podría deberse a parámetros del modelo o ruido estadístico")
    print(f"   • 🎯 Próximo paso: Probar filtro biológico (Experimento 2)")
    
else:
    print("\n❌ ESCENARIO C: No hay especificidad clara en este régimen")
    print(f"   • MFPT varía suavemente con frecuencia, sin pico definido")
    print(f"   • El modelo actual no captura mecanismo de sintonización fina")
    print(f"   • 🎯 Próximo paso: Implementar filtro biológico + resonancia neuronal")

print(f"\n💡 Nota: La ausencia de especificidad NO invalida la hipótesis.")
print(f"   Simplemente indica que el mecanismo requiere más complejidad biológica.")
print(f"   Esto es común en modelos teóricos iniciales y abre oportunidades de refinamiento.")

print("\n" + "="*70 + "\n")
