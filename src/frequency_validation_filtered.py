"""
Validación de frecuencia CON FILTRO BIOLÓGICO.
Compara MFPT bajo diferentes frecuencias con respuesta frecuencial realista.
"""

import numpy as np
import pandas as pd
from .model import SchumannProteostasisModel


def sweep_frequency_filtered(
    frequency_range=None,
    base_params=None,
    tau_filter=0.02,  # Tiempo de relajación del filtro
    n_trials=30,
    output_file=None
):
    """
    Barrido sobre frecuencia usando campo filtrado biológicamente.
    """
    if frequency_range is None:
        frequency_range = [1.0, 3.0, 5.0, 7.83, 10.0, 13.0, 15.0, 20.0, 30.0]
    
    if base_params is None:
        base_params = {'eta': 0.5, 'sigma': 0.3, 'T': 5.0, 'dt': 0.001}
    
    results = []
    
    print(f"🔍 Validación de frecuencia CON FILTRO BIOLÓGICO (τ={tau_filter}s)")
    print(f"   Frecuencias a probar: {len(frequency_range)}\n")
    
    for f in frequency_range:
        params = base_params.copy()
        params['f_schumann'] = f
        params['n_trials'] = n_trials
        
        model = SchumannProteostasisModel(params)
        well1, _ = model.find_well_positions()
        
        # Simulación con campo filtrado
        # Necesitamos modificar temporalmente el método
        original_field = model.schumann_field
        model.schumann_field = lambda t, tau=tau_filter: model.schumann_field_filtered(t, tau)
        
        trajectories = model.simulate_euler_maruyama(x0=well1, n_trials=n_trials)
        mfpt, success = model.calculate_mfpt(trajectories, threshold=0.0)
        
        # Calcular ganancia del filtro para esta frecuencia
        omega = 2 * np.pi * f
        gain = 1 / np.sqrt(1 + (omega * tau_filter)**2)
        
        results.append({
            'frequency': f,
            'mfpt': float(mfpt) if np.isfinite(mfpt) else 999.0,
            'success_rate': float(success),
            'filter_gain': float(gain),
            'is_schumann': np.isclose(f, 7.83, atol=0.01)
        })
        
        marker = "🎯 SCHUMANN" if np.isclose(f, 7.83, atol=0.01) else ""
        print(f"   f={f:5.2f} Hz → MFPT={mfpt:6.2f}s, gain={gain:.3f} {marker}")
    
    results_df = pd.DataFrame(results)
    
    if output_file:
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        results_df.to_csv(output_file, index=False)
        print(f"\n💾 Resultados guardados: {output_file}")
    
    return results_df
