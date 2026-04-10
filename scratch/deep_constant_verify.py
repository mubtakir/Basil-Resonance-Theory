import numpy as np
from mpmath import mp, zetazero, zeta, log, sqrt, pi
import os

def compute_mobius_upto(N):
    mu = np.ones(N + 1, dtype=int)
    primes = []
    is_prime = np.ones(N + 1, dtype=bool)
    for i in range(2, N + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > N:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def verify_constants(num_zeros=10, N=1000000):
    mp.dps = 30
    print(f"Verifying constants for {num_zeros} zeros with N = {N:,}...")
    
    mu = compute_mobius_upto(N)
    n_vals = np.arange(1, N + 1)
    
    results = []
    
    c8 = pi / sqrt(8)
    c3 = pi / 3
    
    print(f"\nTarget Constants:")
    print(f"pi/3 approx {float(c8):.10f}")
    print(f"pi/3       approx {float(c3):.10f}")
    print("-" * 50)
    
    for i in range(1, num_zeros + 1):
        rho = zetazero(i)
        t = float(rho.imag)
        z_prime = abs(zeta(rho, derivative=1))
        
        # Calculate M_N(rho) with high precision
        # Using vectorized approach for speed, then refining if needed
        # Actually, for N=1M, simple sum might take a bit.
        powers = n_vals**(-0.5 - 1j * t)
        m_n_val = abs(np.sum(mu[1:] * powers))
        
        ratio = (m_n_val * float(z_prime)) / np.log(N)
        results.append(ratio)
        
        err8 = abs(ratio - float(c8))
        err3 = abs(ratio - float(c3))
        winner = "pi/3" if err8 < err3 else "pi/3"
        
        print(f"Zero {i:2} (t={t:8.4f}): Ratio = {ratio:.10f} | Winner: {winner}")

    avg_ratio = np.mean(results)
    print("\n" + "="*50)
    print(f"Average Ratio (N={N:,}): {avg_ratio:.10f}")
    print(f"Closest to pi/3: {abs(avg_ratio - float(c8)) < abs(avg_ratio - float(c3))}")
    print(f"Closest to pi/3:       {abs(avg_ratio - float(c3)) < abs(avg_ratio - float(c8))}")
    print("="*50)

def verify_convergence(num_zeros=3):
    mp.dps = 30
    Ns = [100000, 500000, 1000000, 2000000, 5000000]
    
    print(f"[/] Run Convergence Sweep (N up to 5,000,000) for {num_zeros} zeros...")
    c8 = pi / sqrt(8)
    c3 = pi / 3
    
    print(f"pi/3 approx {float(c8):.10f}")
    print(f"pi/3       approx {float(c3):.10f}\n")
    
    for N in Ns:
        mu = compute_mobius_upto(N)
        n_vals = np.arange(1, N + 1)
        ratios = []
        for i in range(1, num_zeros + 1):
            rho = zetazero(i)
            t = float(rho.imag)
            z_prime = abs(zeta(rho, derivative=1))
            powers = n_vals**(-0.5 - 1j * t)
            m_n_val = abs(np.sum(mu[1:] * powers))
            ratio = (m_n_val * float(z_prime)) / np.log(N)
            ratios.append(ratio)
        
        avg = np.mean(ratios)
        print(f"N = {N:9,} | Avg Ratio = {avg:.10f}")

if __name__ == "__main__":
    verify_convergence(num_zeros=3)
