"""
Análisis de robustez: variabilidad en parámetros del modelo.
Análogo a análisis PVT (Process-Voltage-Temperature) en hardware.
"""

import numpy as np
import pandas as pd
from .model import SchumannProteostasisModel


def robustness_sweep(
    param_name,
    nominal_value,
    variation_percent=10,
    n_samples=20,
    base_params=None,
    n_trials=20
):
    """
    Barrido de robustez sobre un parámetro específico.
    
    Args:
        param_name: Nombre del parámetro a variar
        nominal_value: Valor nominal del parámetro
        variation_percent: Porcentaje de variación a explorar
        n_samples: Número de puntos en el barrido
        base_params: Parámetros base
        n_trials: Trayectorias por punto
    
    Returns:
        results_df: MFPT vs valor del parámetro
    """
    # Rango de variación
    min_val = nominal_value * (1 - variation_percent/100)
    max_val = nominal_value * (1 + variation_percent/100)
    param_values = np.linspace(min_val, max_val, n_samples)
    
    if base_params is None:
        base_params = {'eta': 0.5, 'sigma': 0.3, 'T': 5.0, 'dt': 0.001}
    
    results = []
    
    print(f"🔧 Robustez: {param_name} ±{variation_percent}% alrededor de {nominal_value}\n")
    
    for val in param_values:
        params = base_params.copy()
        params[param_name] = val
        params['n_trials'] = n_trials
        
        model = SchumannProteostasisModel(params)
        well1, _ = model.find_well_positions()
        
        trajectories = model.simulate_euler_maruyama(x0=well1, n_trials=n_trials)
        mfpt, success = model.calculate_mfpt(trajectories, threshold=0.0)
        
        results.append({
            param_name: float(val),
            'mfpt': float(mfpt) if np.isfinite(mfpt) else 999.0,
            'success_rate': float(success),
            'relative_change': float((val - nominal_value) / nominal_value * 100)
        })
    
    return pd.DataFrame(results)


def compute_robustness_metric(results_df, param_name):
    """
    Calcula métrica cuantitativa de robustez.
    
    Returns:
        dict: Coeficiente de variación, sensibilidad, etc.
    """
    mfpt_values = results_df['mfpt'].replace(999.0, np.nan).dropna()
    
    if len(mfpt_values) < 2:
        return None
    
    cv = float(mfpt_values.std() / mfpt_values.mean())  # Coeficiente de variación
    sensitivity = float(np.polyfit(results_df[param_name], results_df['mfpt'], 1)[0])  # Pendiente
    
    return {
        'coefficient_of_variation': cv,
        'sensitivity_slope': sensitivity,
        'mfpt_mean': float(mfpt_values.mean()),
        'mfpt_std': float(mfpt_values.std()),
        'robust': cv < 0.3  # Umbral heurístico
    }
