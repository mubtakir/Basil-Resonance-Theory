import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
import time

# ضبط الدقة العالية
mp.dps = 50

def to_float(x):
    return float(x)

def ghost_extraction_probe(sigma, t, N_values):
    """
    مسبار استخراج الشبح المطور: يقيس تطابق المقدار والطور (الزاوية)
    """
    s = mp.mpc(sigma, t)
    z_val = mp.zeta(s)
    
    results_raw = []
    results_extracted = []
    angle_deviations = []
    
    current_S = mp.mpc(0, 0)
    current_N = 0
    
    # المتجه النظري الأساسي (بدون القسمة على N^(1-sigma))
    # V_theory = N^(1-s)/(1-s)
    
    for target_N in sorted(N_values):
        for n in range(current_N + 1, target_N + 1):
            current_S += 1 / (mp.mpf(n) ** s)
        
        norm = mp.mpf(target_N) ** (1 - sigma)
        
        # 1. المقدار (طريقة الوكيل)
        val_raw = to_float(mp.fabs(current_S) / norm)
        results_raw.append(val_raw)
        
        # 2. المقدار المستخلص (طريقة التناظر)
        v_actual = current_S - z_val
        val_extracted = to_float(mp.fabs(v_actual) / norm)
        results_extracted.append(val_extracted)
        
        # 3. قياس تناغم الاتجاه (Phase Alignment)
        v_theory = (mp.mpf(target_N) ** (1 - s)) / (1 - s)
        
        # الزاوية بين المتجهين (بالدرجات)
        # نحسب الفرق بين الزوايا ونقيس مدى انطباقهما
        angle_actual = mp.arg(v_actual)
        angle_theory = mp.arg(v_theory)
        
        # تصحيح الفرق ليكون في النطاق [-pi, pi]
        diff = angle_actual - angle_theory
        while diff > mp.pi: diff -= 2 * mp.pi
        while diff < -mp.pi: diff += 2 * mp.pi
        
        angle_deviations.append(to_float(mp.degrees(mp.fabs(diff))))
        
        current_N = target_N
        
    chord_theory = 1.0 / mp.fabs(1 - s)
    return results_raw, results_extracted, angle_deviations, to_float(chord_theory)

# ============================================================================
# Running Experiment
# ============================================================================
sigma_test = 0.8
t_test = 10.0
N_values = [int(x) for x in np.logspace(2, 6, 50)] 

start_time = time.time()
raw, extracted, angles, theory = ghost_extraction_probe(sigma_test, t_test, N_values)
print(f"Calculation finished in {time.time() - start_time:.2f} seconds")

# ============================================================================
# Plotting - Comprehensive Scientific Proof
# ============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# الرسم الأول: المقادير (المقياس الهندسي)
ax1.semilogx(N_values, raw, 'r--', alpha=0.4, label='Raw Magnitude (With Ghost)')
ax1.semilogx(N_values, extracted, 'b-', linewidth=3, label='Extracted Magnitude (Chord Law)')
ax1.axhline(y=theory, color='green', linestyle=':', label=f'Target = {theory:.6f}')
ax1.set_title(f'Magnitude Analysis (sigma={sigma_test}, t={t_test})', fontsize=14)
ax1.set_ylabel('|Residual| / N^{1-sigma}')
ax1.legend()
ax1.grid(True, alpha=0.3)

# الرسم الثاني: الاتجاهات (التناغم الجيومتري)
ax2.semilogx(N_values, angles, 'm-o', markersize=4, label='Angle Deviation (Degrees)')
ax2.set_title('Phase Alignment: Angle Difference between Actual and Theoretical Vectors', fontsize=14)
ax2.set_xlabel('N (Log Scale)')
ax2.set_ylabel('Deviation (Degrees)')
ax2.set_ylim(-0.1, max(angles[10:]) * 2 if len(angles)>10 else 5)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('directional_harmony_results.png', dpi=150)
print("\n[OK] Directional Harmony results saved to 'directional_harmony_results.png'")

# Accuracy Summary
print(f"\n--- Scientific Rigor Report ---")
print(f"Final Magnitude Error: {abs(extracted[-1] - theory)/theory:.2e}")
print(f"Final Angle Deviation: {angles[-1]:.6f} degrees")

if angles[-1] < 0.01:
    print("\n[CONCLUSION] High Scientific Confidence: Directional Harmony Verified.")
    print("The vectors are not just equal in length, they are parallel (Asymptotic Identity).")
