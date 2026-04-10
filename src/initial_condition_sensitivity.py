"""
Análisis de sensibilidad a condiciones iniciales.
¿Converge el sistema al mismo atractor desde diferentes x0?
"""

import numpy as np
import pandas as pd
from .model import SchumannProteostasisModel


def analyze_convergence(
    initial_conditions=None,
    base_params=None,
    simulation_time=10.0,
    n_trials=20
):
    """
    Evalúa convergencia desde diferentes condiciones iniciales.
    
    Args:
        initial_conditions: Lista de valores x0 a probar
        base_params: Parámetros del modelo
        simulation_time: Duración de cada simulación
        n_trials: Réplicas por condición inicial
    
    Returns:
        convergence_df: DataFrame con tasas de convergencia por x0
    """
    if initial_conditions is None:
        initial_conditions = np.linspace(-2.5, 2.5, 11)
    
    if base_params is None:
        base_params = {'eta': 0.5, 'sigma': 0.3, 'T': simulation_time, 'dt': 0.001}
    
    results = []
    
    print(f"🔄 Analizando convergencia desde {len(initial_conditions)} condiciones iniciales...\n")
    
    for x0 in initial_conditions:
        params = base_params.copy()
        model = SchumannProteostasisModel(params)
        
        well_healthy, well_pathological = model.find_well_positions()
        
        trajectories = model.simulate_euler_maruyama(x0=x0, n_trials=n_trials)
        
        # Clasificar estado final
        final_states = trajectories[:, -1]
        n_healthy = np.sum(final_states < 0)  # Asumimos pozo izquierdo = saludable
        n_pathological = np.sum(final_states >= 0)
        
        results.append({
            'x0': float(x0),
            'n_trials': n_trials,
            'converged_healthy': int(n_healthy),
            'converged_pathological': int(n_pathological),
            'fraction_healthy': float(n_healthy / n_trials),
            'well_healthy': float(well_healthy),
            'well_pathological': float(well_pathological)
        })
        
        print(f"   x0={x0:5.2f} → Saludable: {n_healthy}/{n_trials} ({n_healthy/n_trials:.0%})")
    
    return pd.DataFrame(results)
