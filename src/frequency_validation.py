"""
Validación de especificidad de frecuencia: ¿Es Schumann especial?
Compara MFPT bajo diferentes frecuencias de forzamiento.
"""

import numpy as np
import pandas as pd
from .model import SchumannProteostasisModel


def sweep_frequency(
    frequency_range=None,
    base_params=None,
    n_trials=30,
    output_file=None
):
    """
    Barrido sobre frecuencia de forzamiento para testear especificidad.
    
    Args:
        frequency_range: Lista de frecuencias a probar (Hz)
        base_params: Parámetros base del modelo
        n_trials: Trayectorias por frecuencia
        output_file: Ruta para guardar resultados
    
    Returns:
        results_df: DataFrame con MFPT por frecuencia
    """
    if frequency_range is None:
        # Rango que incluye Schumann y controles
        frequency_range = [1.0, 3.0, 5.0, 7.83, 10.0, 13.0, 15.0, 20.0, 30.0]
    
    if base_params is None:
        base_params = {'eta': 0.5, 'sigma': 0.3, 'T': 5.0, 'dt': 0.001}
    
    results = []
    
    print(f"🔍 Validación de frecuencia: {len(frequency_range)} valores\n")
    
    for f in frequency_range:
        params = base_params.copy()
        params['f_schumann'] = f
        params['n_trials'] = n_trials
        
        model = SchumannProteostasisModel(params)
        well1, _ = model.find_well_positions()
        
        trajectories = model.simulate_euler_maruyama(x0=well1, n_trials=n_trials)
        mfpt, success = model.calculate_mfpt(trajectories, threshold=0.0)
        
        results.append({
            'frequency': f,
            'mfpt': float(mfpt) if np.isfinite(mfpt) else 999.0,
            'success_rate': float(success),
            'is_schumann': np.isclose(f, 7.83, atol=0.01)
        })
        
        marker = "🎯 SCHUMANN" if np.isclose(f, 7.83, atol=0.01) else ""
        print(f"   f={f:5.2f} Hz → MFPT={mfpt:6.2f}s {marker}")
    
    results_df = pd.DataFrame(results)
    
    if output_file:
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        results_df.to_csv(output_file, index=False)
        print(f"\n💾 Resultados guardados: {output_file}")
    
    return results_df


def analyze_frequency_specificity(results_df):
    """
    Analiza si Schumann produce MFPT significativamente mayor.
    
    Returns:
        dict: Estadísticos de comparación
    """
    schumann = results_df[results_df['is_schumann']]['mfpt'].values[0]
    others = results_df[~results_df['is_schumann']]['mfpt']
    
    analysis = {
        'mfpt_schumann': float(schumann),
        'mfpt_others_mean': float(others.mean()),
        'mfpt_others_std': float(others.std()),
        'enhancement_factor': float(schumann / others.mean()) if others.mean() > 0 else np.inf,
        'schumann_is_optimal': bool(schumann >= others.max())
    }
    
    return analysis
