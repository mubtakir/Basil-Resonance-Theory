from ZetaLab_Supreme import ZetaLab
import numpy as np

# --- EXPERIMENT 03: THE PRIME RESONANCE FAMILIES ---
# Objective: Systematically identify the "Resonance Depth" peaks for the first 10 zeros
# and confirm their alignment with the Prime {2, 5, 7, 17} families.

def get_depth_for_N(lab, t, N):
    H = lab.get_basil_denominator(0.5, t)
    theo_val = 1.0 / H
    
    # 1. Error at the exact zero
    sn = lab.calculate_partial_sum(complex(0.5, t), N)
    err_zero = abs(abs(sn)/np.sqrt(N) - theo_val)
    
    # 2. Mean background error (at slightly different t)
    bg_errs = []
    for off in [-0.1, 0.1]:
        t_bg = t + off
        sn_bg = lab.calculate_partial_sum(complex(0.5, t_bg), N)
        H_bg = lab.get_basil_denominator(0.5, t_bg)
        err_bg = abs(abs(sn_bg)/np.sqrt(N) - (1.0 / H_bg))
        bg_errs.append(err_bg)
        
    depth = np.mean(bg_errs) / (err_zero + 1e-15)
    return float(depth)

def run_prime_families_experiment():
    lab = ZetaLab(precision=50)
    print("======================================================================")
    print("EXPERIMENT 03: THE PRIME RESONANCE MATRIX (SYSTEMATIC)")
    print("======================================================================")
    
    zeros = [
        14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 
        37.5862, 40.9187, 43.3271, 48.0052, 49.7738
    ]
    
    allowed_primes = {2, 5, 7, 17}
    
    print(f"{'Zero':<6} | {'t':<8} | {'Best N':<8} | {'Depth':<10} | {'Factors'}")
    print("-" * 65)
    
    for i, t in enumerate(zeros):
        best_N = 0
        best_depth = 0
        
        # In this systematic approach, we scan a range of N that includes
        # the magical numbers 25, 70, 98, 34, 119 etc.
        for N in range(10, 150):
            d = get_depth_for_N(lab, t, N)
            if d > best_depth:
                best_depth = d
                best_N = N
        
        # Check factors of best_N
        temp_N = best_N
        factors = []
        for p in [2, 3, 5, 7, 11, 13, 17, 19]:
            while temp_N % p == 0:
                temp_N //= p
                factors.append(p)
        
        f_str = "x".join(map(str, factors)) if temp_N == 1 else str(best_N)
        print(f"Z{i+1:<5} | {t:<8.4f} | {best_N:<8} | {best_depth:<10.2f} | {f_str}")

if __name__ == "__main__":
    run_prime_families_experiment()

