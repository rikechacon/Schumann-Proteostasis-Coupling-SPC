# Supplementary Appendix: Mathematical Derivations
## Schumann-Proteostasis Coupling

**Author**: Enrique Chacón-Pinzón  
**Date**: March 2026  
**Contact**: rikechaconpi@gmail.com

---

## Table of Contents

1. [Derivation of the Forced Langevin Equation](#sec:langevin)
2. [Double-Well Potential Analysis](#sec:potential)
3. [Kramers' Escape Rate Calculation](#sec:kramers)
4. [Resonant Coupling Factor Derivation](#sec:resonance)
5. [Euler-Maruyama Discretization](#sec:numerical)
6. [Parameter Sensitivity Analysis](#sec:sensitivity)

---

## 1. Derivation of the Forced Langevin Equation {#sec:langevin}

### 1.1 General Form

The proteostatic state evolution is modeled by the stochastic differential equation:

$$\gamma \frac{dx}{dt} = -\frac{\partial V(x)}{\partial x} + \eta \cdot F_{\text{SR}}(t) + \sqrt{2\gamma k_B T} \cdot \xi(t)$$

where:
- $x(t)$: proteostatic state variable (protein aggregation load)
- $\gamma$: viscous friction coefficient of cytoplasm
- $V(x)$: double-well potential
- $\eta$: electromagnetic coupling efficiency
- $F_{\text{SR}}(t)$: Schumann resonance forcing term
- $\xi(t)$: Gaussian white noise with $\langle \xi(t)\xi(t') \rangle = \delta(t-t')$

### 1.2 Physical Interpretation

**Deterministic terms:**
- $-\partial V/\partial x$: gradient force driving system toward potential minima
- $\eta F_{\text{SR}}(t)$: external electromagnetic forcing

**Stochastic term:**
- $\sqrt{2\gamma k_B T}\xi(t)$: thermal and biological fluctuations
- Satisfies fluctuation-dissipation theorem

---

## 2. Double-Well Potential Analysis {#sec:potential}

### 2.1 Potential Function

$$V(x) = \frac{a}{2}x^2 + \frac{b}{4}x^4 - \mu x$$

with $a < 0$, $b > 0$, and $\mu$ representing metabolic bias.

### 2.2 Fixed Points

Fixed points satisfy $\frac{dV}{dx} = 0$:

$$\frac{dV}{dx} = ax + bx^3 - \mu = 0$$

For $\mu = 0$ (symmetric case):
$$x(ax^2 + b) = 0$$

Solutions:
- $x_0 = 0$ (unstable maximum)
- $x_{\pm} = \pm\sqrt{-a/b}$ (stable minima)

### 2.3 Barrier Height

For symmetric case ($\mu = 0$):

$$\Delta V = V(0) - V(x_{\pm}) = \frac{a^2}{4b}$$

With our parameters ($a = -1.0$, $b = 1.0$):
$$\Delta V = \frac{(-1)^2}{4(1)} = 0.25$$

---

## 3. Kramers' Escape Rate {#sec:kramers}

### 3.1 Transition Rate Formula

For weak noise ($k_B T \ll \Delta V$), the transition rate from healthy to pathological well is:

$$k_{\text{trans}} = \frac{\omega_0 \omega_b}{2\pi\gamma} \exp\left(-\frac{\Delta V_{\text{eff}}}{k_B T}\right)$$

where:
- $\omega_0 = \sqrt{V''(x_{\text{min}})/m}$: frequency at well minimum
- $\omega_b = \sqrt{|V''(x_{\text{max}})|/m}$: frequency at barrier top
- $\Delta V_{\text{eff}}$: effective barrier height (modified by forcing)

### 3.2 Mean First Passage Time

The MFPT is the inverse of the transition rate:

$$\text{MFPT} = \frac{1}{k_{\text{trans}}} = \frac{2\pi\gamma}{\omega_0 \omega_b} \exp\left(\frac{\Delta V_{\text{eff}}}{k_B T}\right)$$

### 3.3 Effect of Resonant Forcing

The resonant coupling modifies the effective barrier:

$$\Delta V_{\text{eff}} = \Delta V_0 - \delta V(\eta, Q, f)$$

where $\delta V$ depends on:
- Coupling efficiency $\eta$
- Quality factor $Q$
- Frequency detuning $|f - f_{\text{neural}}|$

---

## 4. Resonant Coupling Factor {#sec:resonance}

### 4.1 Lorentzian Lineshape

The frequency-selective coupling factor follows a Lorentzian profile:

$$Q(f) = \frac{1}{1 + \left(\dfrac{f - f_{\text{neural}}}{f_{\text{neural}}/Q_{\text{factor}}}\right)^2}$$

### 4.2 Derivation from Damped Harmonic Oscillator

Consider a damped oscillator driven at frequency $f$:

$$\ddot{x} + 2\beta\dot{x} + \omega_0^2 x = F_0 \cos(2\pi f t)$$

The steady-state amplitude is:

$$A(f) = \frac{F_0}{\sqrt{(\omega_0^2 - (2\pi f)^2)^2 + (4\pi\beta f)^2}}$$

Near resonance ($f \approx f_0 = \omega_0/2\pi$), this reduces to Lorentzian form with:
$$Q_{\text{factor}} = \frac{f_0}{2\beta}$$

### 4.3 Full Width at Half Maximum (FWHM)

The resonance bandwidth is:

$$\text{FWHM} = \frac{2f_{\text{neural}}}{Q_{\text{factor}}}$$

For $f_{\text{neural}} = 7.83$ Hz and $Q_{\text{factor}} = 8$:
$$\text{FWHM} = \frac{2(7.83)}{8} \approx 1.96 \text{ Hz}$$

---

## 5. Numerical Implementation {#sec:numerical}

### 5.1 Euler-Maruyama Discretization

The continuous SDE is discretized as:

$$x_{n+1} = x_n + \frac{dt}{\gamma}\left[-\frac{\partial V}{\partial x}(x_n) + \eta F_{\text{SR}}(t_n)\right] + \sqrt{\frac{2k_B T dt}{\gamma}} \cdot \mathcal{N}(0,1)$$

where $\mathcal{N}(0,1)$ is a standard normal random variable.

### 5.2 Stability Criterion

For numerical stability, the time step must satisfy:

$$dt < \frac{2\gamma}{|a| + 3b x_{\text{max}}^2}$$

With our parameters and $x_{\text{max}} \approx 2$:
$$dt < \frac{2(1)}{1 + 3(1)(4)} \approx 0.15 \text{ s}$$

We use $dt = 0.001$ s for high accuracy.

### 5.3 Convergence Analysis

The weak convergence order of Euler-Maruyama is $\mathcal{O}(dt)$, meaning:

$$|\mathbb{E}[x(T)] - \mathbb{E}[x_N]| \leq C \cdot dt$$

where $N = T/dt$ is the number of steps.

---

## 6. Parameter Sensitivity {#sec:sensitivity}

### 6.1 Dimensionless Groups

Define dimensionless parameters:

$$\Pi_1 = \frac{\eta A}{\gamma \omega_0 x_0} \quad \text{(forcing strength)}$$
$$\Pi_2 = \frac{k_B T}{\Delta V} \quad \text{(noise strength)}$$
$$\Pi_3 = \frac{f_{\text{SR}}}{f_{\text{neural}}} \quad \text{(frequency ratio)}$$

### 6.2 Sensitivity Coefficients

The sensitivity of MFPT to parameter $p$ is:

$$S_p = \frac{\partial \ln(\text{MFPT})}{\partial \ln p} = \frac{p}{\text{MFPT}} \frac{\partial \text{MFPT}}{\partial p}$$

For barrier height $\Delta V$:
$$S_{\Delta V} = \frac{\Delta V}{k_B T}$$

With $\Delta V = 0.25$ and $k_B T = 0.1$:
$$S_{\Delta V} = \frac{0.25}{0.1} = 2.5$$

This means a 1% change in $\Delta V$ produces a 2.5% change in MFPT.

### 6.3 Robustness Analysis

Our robustness tests show that under $\pm 10\%$ parameter variation:

$$\text{CV}_{\text{MFPT}} = \frac{\sigma_{\text{MFPT}}}{\mu_{\text{MFPT}}} < 0.3$$

This indicates the model predictions are stable under realistic parameter uncertainty.

---

## References

1. Kramers, H.A. (1940). Brownian motion in a field of force and the diffusion model of chemical reactions. *Physica*, 7(4):284-304.

2. Hänggi, P., Talkner, P., and Borkovec, M. (1990). Reaction-rate theory: fifty years after Kramers. *Reviews of Modern Physics*, 62(2):251.

3. Kloeden, P.E. and Platen, E. (1992). *Numerical Solution of Stochastic Differential Equations*. Springer.

4. Gammaitoni, L., Hänggi, P., Jung, P., and Marchesoni, F. (1998). Stochastic resonance. *Reviews of Modern Physics*, 70(1):223.

---

**Last updated**: March 2026  
**Version**: 1.0
