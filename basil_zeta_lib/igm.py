"""
Basil Zeta Library - Integrative Generative Model (IGM)
========================================================
A framework for function approximation and signal deconvolution 
using generalized sigmoidal kernels.

Author: Basel Yahya Abdullah & Antigravity AI
Date: April 2026
"""

import numpy as np

class IGM_Engine:
    def __init__(self, k=1.0, n_exponent=1.0):
        self.k = k
        self.n_exponent = n_exponent

    def kernel(self, x, x0=0):
        """
        The basic IGM Response Kernel K_n(x).
        K_n(x) is the derivative of the generalized sigmoid.
        """
        k = self.k
        n = self.n_exponent
        
        # Shifted x
        dx = x - x0
        
        # Generalized sigmoid: s = 1 / (1 + exp(-k * dx^n))
        # K_n = d(sigmoid)/dx
        exp_term = np.exp(-k * (dx**n))
        denom = (1 + exp_term)**2
        
        # Handle cases where n might be complex or fractional
        kn_term = k * n * (dx**(n-1))
        
        return (kn_term * exp_term) / denom

    def reconstruct_signal(self, stimulus_coeffs, x_positions, x_range):
        """
        f(x) = sum(alpha_i * K_n(x - x_i))
        Discrete generative assembly.
        """
        output = np.zeros_like(x_range, dtype=complex)
        for alpha, xi in zip(stimulus_coeffs, x_positions):
            output += alpha * self.kernel(x_range, x0=xi)
        return output

    def adaptive_regularization(self, freq, noise_level=0.1):
        """
        Lambda(omega) for inverse problem stability.
        """
        return noise_level * (1 + freq**2)
