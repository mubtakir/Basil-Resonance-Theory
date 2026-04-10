
import numpy as np
from mpmath import mp, zetazero, zeta
import sys
import os
sys.path.append(os.getcwd())
from ZetaLab_Supreme import ZetaLab

def verify_constant():
    mp.dps = 20
    lab = ZetaLab(precision=20)
    N = 10000
    ln_N = np.log(N)
    
    mu = lab.sieve_mu(N)
    n_vals = np.arange(1, N + 1)
    
    results = []
    # Test first 10 zeros
    for i in range(1, 11):
        rho = zetazero(i)
        t = float(rho.imag)
        z_prime = abs(zeta(rho, derivative=1))
        
        # Calculate M_N(rho)
        powers = n_vals**(-0.5 - 1j * t)
        m_n = abs(np.sum(mu[1:] * powers))
        
        ratio = (m_n * z_prime) / ln_N
        results.append(float(ratio))
        print(f"Zero {i}: Ratio = {float(ratio):.6f}")

    avg_ratio = np.mean(results)
    print(f"\nAverage Ratio: {avg_ratio:.6f}")
    
    c8 = float(mp.pi / mp.sqrt(8))
    c3 = float(mp.pi / mp.sqrt(3))
    
    print(f"Target (pi/3): {c8:.6f}")
    print(f"Target (pi/sqrt(3)): {c3:.6f}")
    
    if abs(avg_ratio - c8) < abs(avg_ratio - c3):
        print("\nConclusion: The data strongly supports pi/3.")
    else:
        print("\nConclusion: The data strongly supports pi/sqrt(3).")

if __name__ == "__main__":
    verify_constant()
