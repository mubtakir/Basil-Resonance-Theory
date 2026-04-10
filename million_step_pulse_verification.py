import mpmath as mp
import time
import json

# --- BASIL RESONANCE: MILLION-STEP PULSE VERIFICATION ---
# Precision: 50 decimal places
# Target: N = 1,000,000
# Zeros: Z1 to Z5

mp.dps = 50
COSMIC_CONSTANT = mp.pi / mp.sqrt(8)

def compute_mobius_sieve(N):
    """Fast linear sieve for Mobius mu(n)"""
    mu = [0] * (N + 1)
    mu[1] = 1
    primes = []
    is_prime = [True] * (N + 1)
    for i in range(2, N + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > N: break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def run_verification():
    N_MAX = 1000000
    N_SAMPLES = [1000, 10000, 100000, 500000, 1000000]
    
    print("="*90)
    print("BASIL RESONANCE THEORY: 1,000,000-STEP HIGH-PRECISION VERIFICATION")
    print("="*90)
    print(f"Target Cosmic Constant pi/sqrt(8) ~ {float(COSMIC_CONSTANT):.10f}")
    
    start_sieve = time.time()
    print(f"\n[1/3] Computing Mobius Sieve up to {N_MAX:,}...")
    mu = compute_mobius_sieve(N_MAX)
    print(f"      Sieve completed in {time.time() - start_sieve:.2f}s")
    
    results_manifest = {}

    for i in range(1, 6):
        rho = mp.zetazero(i)
        t = float(rho.imag)
        z_prime = abs(mp.zeta(rho, derivative=1))
        
        print(f"\n[2/3] Analyzing Zero Z{i} at t = {t:.6f} (|zeta'| = {float(z_prime):.6f})")
        
        m_sum = mp.mpc(0)
        s_sum = mp.mpc(0) # Shadow Field for contrast
        
        zero_results = []
        current_n_idx = 0
        
        for n in range(1, N_MAX + 1):
            term_z = mp.mpf(n)**-rho
            s_sum += term_z
            if mu[n] != 0:
                m_sum += mu[n] * term_z
            
            if n == N_SAMPLES[current_n_idx]:
                pulse = (abs(m_sum) * z_prime) / mp.log(n)
                ratio = pulse / COSMIC_CONSTANT
                shadow = abs(s_sum)
                
                print(f"      N={n:10,d} | Pulse={float(pulse):.6f} | Ratio={float(ratio):.4f} | Shadow={float(shadow):.4f}")
                
                zero_results.append({
                    "N": n,
                    "Pulse": float(pulse),
                    "Ratio": float(ratio),
                    "Shadow": float(shadow)
                })
                current_n_idx += 1
        
        results_manifest[f"Z{i}"] = zero_results

    # Save to JSON for the visualizer
    with open("resonance_data.json", "w") as f:
        json.dump(results_manifest, f, indent=4)
    
    print("\n" + "="*90)
    print("VERIFICATION COMPLETE. DATA SAVED TO 'resonance_data.json'.")
    print("="*90)

if __name__ == "__main__":
    run_verification()

