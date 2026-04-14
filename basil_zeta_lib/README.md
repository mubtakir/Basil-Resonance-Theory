# Basil Zeta Library (`basil_zeta_lib`)

A scientific Python library for the geometric reconstruction of the Riemann Zeta Function and the implementation of the Integrative Generative Model (IGM).

## Features
- **Geometric Reconstruction**: Rebuild $\zeta(s)$ from first principles (Chord, Cone, Spherical Shells).
- **Impedance Physics**: Model the kinematic properties of Zeta zeros and the critical line $\sigma = 0.5$.
- **IGM Engine**: Solve inverse problems and generate patterns using generalized sigmoidal kernels.

## Installation
Currently, this is a research library. You can include it in your project by adding the folder `basil_zeta_lib` to your working directory.

## Quick Start

### 1. Reconstructing Zeta
```python
from basil_zeta_lib import GeometricZeta

engine = GeometricZeta(precision_level=3)
s = 0.5 + 14.134725j  # First Non-trivial Zero
result = engine.compute(s, N=10000)
print(f"Geometric Zeta at {s} = {result}")
print(f"Magnitude: {abs(result)}")
```

### 2. Checking Impedance
```python
from basil_zeta_lib import ZetaMechanics

mechanics = ZetaMechanics()
stats = mechanics.calculate_impedance(sigma=0.5, t=14.134725)
print(f"Impedance at critical line: {stats['z_residual']}")

stats_off = mechanics.calculate_impedance(sigma=0.3, t=14.134725)
print(f"Impedance off critical line: {stats_off['z_residual']}")
```

### 3. IGM Signal Reconstruction
```python
from basil_zeta_lib import IGM_Engine
import numpy as np

igm = IGM_Engine(k=2.0, n_exponent=1.5)
x_range = np.linspace(-5, 5, 100)
signal = igm.reconstruct_signal([1.0, 0.5], [-1.0, 1.0], x_range)
```

## Scientific Foundations
This library implements the findings of the **Basil Resonance Theory**, specifically:
- **Chapter 16**: The Kinematic-Impedance Model.
- **Chapter 17**: The Geometric Reconstruction Theorem.
- **Filament Theory Part 10**: The Integrative Generative Model.

---
Produced by Basel Yahya Abdullah & Antigravity AI (April 2026).
