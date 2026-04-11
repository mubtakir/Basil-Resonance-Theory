import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
import time

# High precision setup for scientific verification
mp.dps = 50

def to_float(x):
    return float(x)

def ghost_extraction_probe(sigma, t, N_values):
    """
    Enhanced Ghost Extraction Probe: Measures both magnitude and phase alignment.
    This demonstrates the structural nature of the Basil Resonance Law.
    """
    s = mp.mpc(sigma, t)
    z_val = mp.zeta(s)
    
    results_raw = []
    results_extracted = []
    angle_deviations = []
    
    current_S = mp.mpc(0, 0)
    current_N = 0
    
    # Asymptotic Identity: S_N - zeta(s) ~ N^(1-s)/(1-s)
    
    for target_N in sorted(N_values):
        for n in range(current_N + 1, target_N + 1):
            current_S += 1 / (mp.mpf(n) ** s)
        
        norm = mp.mpf(target_N) ** (1 - sigma)
        
        # 1. Raw magnitude (As measured by the Undersecretary)
        val_raw = to_float(mp.fabs(current_S) / norm)
        results_raw.append(val_raw)
        
        # 2. Extracted magnitude (The Resonance Law)
        v_actual = current_S - z_val
        val_extracted = to_float(mp.fabs(v_actual) / norm)
        results_extracted.append(val_extracted)
        
        # 3. Phase Alignment (Directional Harmony)
        v_theory = (mp.mpf(target_N) ** (1 - s)) / (1 - s)
        
        angle_actual = mp.arg(v_actual)
        angle_theory = mp.arg(v_theory)
        
        # Correct diff to range [-pi, pi]
        diff = angle_actual - angle_theory
        while diff > mp.pi: diff -= 2 * mp.pi
        while diff < -mp.pi: diff += 2 * mp.pi
        
        angle_deviations.append(to_float(mp.degrees(mp.fabs(diff))))
        current_N = target_N
        
    chord_theory = 1.0 / mp.fabs(1 - s)
    return results_raw, results_extracted, angle_deviations, to_float(chord_theory)

# ============================================================================
# Running Final Verification (Point: sigma=0.8, t=10.0)
# ============================================================================
sigma_test = 0.8
t_test = 10.0
# Logarithmic N distribution for clear visual pattern
N_values = [int(x) for x in np.logspace(2, 6, 60)] 

start_time = time.time()
raw, extracted, angles, theory = ghost_extraction_probe(sigma_test, t_test, N_values)
print(f"Scientific verification completed in {time.time() - start_time:.2f} seconds")

# ============================================================================
# Generating the Definitive Rebuttal Visual
# ============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 11))

# Plot 1: Magnitude Analysis (Shadow vs. Pillar)
ax1.semilogx(N_values, raw, 'r--', alpha=0.4, label='Raw Ratio (Shadow/Oscillatory)')
ax1.semilogx(N_values, extracted, 'b-', linewidth=3, label='Extracted Ratio (The Resonance Law)')
ax1.axhline(y=theory, color='green', linestyle=':', label=f'Theoretical Objective = {theory:.6f}')
ax1.set_title(f'Visual Rebuttal: Magnitude Stability (sigma={sigma_test}, t={t_test})', fontsize=16)
ax1.set_ylabel('|Residual| / N^{1-sigma}', fontsize=12)
ax1.legend(fontsize=12)
ax1.grid(True, alpha=0.3)

# Plot 2: Directional Harmony (The Final Proof)
ax2.semilogx(N_values, angles, 'm-o', markersize=4, label='Phase Deviation (Degrees)')
ax2.set_title('Directional Harmony: Angle Deviation between Actual and Theoretical Vectors', fontsize=16)
ax2.set_xlabel('N (Number of terms)', fontsize=12)
ax2.set_ylabel('Deviation (Degrees)', fontsize=12)
ax2.set_ylim(-0.1, max(angles[10:]) * 4 if len(angles)>10 else 5)
ax2.legend(fontsize=12)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('24_Ghost_Extraction_Verification.png', dpi=200)

# Final Rigor Check
final_mag_err = abs(extracted[-1] - theory) / theory
final_ang_err = angles[-1]

print(f"\n--- Final Verification Summary ---")
print(f"Relative Magnitude Error: {final_mag_err:.2e}")
print(f"Final Angle Deviation   : {final_ang_err:.6f} degrees")
print(f"\n[CONCLUSION] The Resonance Law is a structural identity: S_N - zeta(s) ~ N^(1-s)/(1-s)")
