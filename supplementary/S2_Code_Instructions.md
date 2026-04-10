# Complete Source Code for Reproducibility

## Repository Structure

The complete source code is available at:
**https://github.com/rikechacon/Schumann-Proteostasis-Coupling-SPC**

## Key Files

### Core Model
- `src/model.py`: SchumannProteostasisModel class with Langevin dynamics
- `src/parametric_sweep.py`: Functions for systematic parameter exploration
- `src/frequency_validation.py`: Frequency sweep and validation functions
- `src/advanced_plotting.py`: Publication-ready figure generation

### Simulation Scripts
- `run_first_simulation.py`: Basic simulation and visualization
- `run_parametric_sweep.py`: Complete parameter sweep (121 combinations)
- `test_resonant_coupling.py`: Resonant coupling validation
- `test_resonant_coupling_amplified.py`: Amplified resonance tests

### Analysis Tools
- `visualize_sweep_results.py`: Heatmap and curve generation
- `generate_publication_figures.py`: Final figure production
- `run_additional_analyses.py`: Robustness and convergence tests

### Configuration
- `config/default_params.yaml`: Default model parameters
- `requirements.txt`: Python dependencies

## How to Reproduce Results

### 1. Install Dependencies

