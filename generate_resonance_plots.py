import json
import matplotlib.pyplot as plt
import numpy as np

# --- RESONANCE VISUALIZER ---
# Data Source: resonance_data.json
# Outputs: basil_resonance_unity.png

def generate_plots():
    with open("resonance_data.json", "r") as f:
        data = json.load(f)
    
    COSMIC = np.pi / np.sqrt(8)
    zeros = list(data.keys())
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    plt.style.use('dark_background') # Aesthetic choice for premium look
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Basil Resonance Theory: Million-Step Unity Dashboard', fontsize=24, fontweight='bold', color='cyan', y=0.98)
    
    # 1. Pulse Convergence (The Active Pulse)
    ax1 = axes[0, 0]
    for i, z in enumerate(zeros):
        n = [d['N'] for d in data[z]]
        pulse = [d['Pulse'] for d in data[z]]
        ax1.semilogx(n, pulse, marker='o', label=z, color=colors[i], linewidth=2)
    ax1.axhline(y=COSMIC, color='white', linestyle='--', alpha=0.8, label=f'pi/3 ~ {COSMIC:.4f}')
    ax1.set_title('Pulse Convergence (|M_N|*|zeta\'|/ln N)', fontsize=14, color='yellow')
    ax1.set_xlabel('N (log scale)')
    ax1.set_ylabel('Pulse Value')
    ax1.legend()
    ax1.grid(alpha=0.2)

    # 2. Ratio to Unity
    ax2 = axes[0, 1]
    for i, z in enumerate(zeros):
        n = [d['N'] for d in data[z]]
        ratio = [d['Ratio'] for d in data[z]]
        ax2.semilogx(n, ratio, marker='s', label=z, color=colors[i], linewidth=2)
    ax2.axhline(y=1.0, color='white', linestyle='-', alpha=0.5)
    ax2.set_title('Ratio to Cosmic Constant', fontsize=14, color='yellow')
    ax2.set_xlabel('N (log scale)')
    ax2.set_ylabel('Ratio')
    ax2.grid(alpha=0.2)

    # 3. Shadow Expansion (The Critical Contrast)
    ax3 = axes[0, 2]
    for i, z in enumerate(zeros):
        n = [d['N'] for d in data[z]]
        shadow = [d['Shadow'] for d in data[z]]
        ax3.loglog(n, shadow, marker='^', label=z, color=colors[i], linewidth=2)
    # Background growth reference sqrt(N)
    n_ref = np.array([1000, 1000000])
    ax3.loglog(n_ref, np.sqrt(n_ref)/5, color='gray', linestyle=':', label='~sqrt(N)')
    ax3.set_title('Shadow Field Growth (|S_N|)', fontsize=14, color='red')
    ax3.set_xlabel('N (log scale)')
    ax3.set_ylabel('Magnitude')
    ax3.legend()
    ax3.grid(alpha=0.2)

    # 4. Error Decay Analysis
    ax4 = axes[1, 0]
    for i, z in enumerate(zeros):
        n = [d['N'] for d in data[z]]
        error = [abs(d['Ratio'] - 1) * 100 for d in data[z]]
        ax4.loglog(n, error, marker='D', label=z, color=colors[i], linewidth=2)
    ax4.set_title('Absolute Error (%)', fontsize=14, color='cyan')
    ax4.set_xlabel('N (log scale)')
    ax4.set_ylabel('Error (%)')
    ax4.grid(alpha=0.2)

    # 5. Final Unity Score (at N=1M)
    ax5 = axes[1, 1]
    final_ratios = [data[z][-1]['Ratio'] for z in zeros]
    bars = ax5.bar(zeros, final_ratios, color=colors, alpha=0.8)
    ax5.axhline(y=1.0, color='white', linestyle='--')
    ax5.set_title('Unity Score at N=1,000,000', fontsize=14, color='cyan')
    ax5.set_ylabel('Final Ratio')
    ax5.set_ylim(0.8, 1.2)
    for bar in bars:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{height:.4f}', ha='center', va='bottom', color='white')

    # 6. Statistical Variance
    ax6 = axes[1, 2]
    all_ratios = []
    for z in zeros:
        all_ratios.extend([d['Ratio'] for d in data[z]])
    ax6.hist(all_ratios, bins=15, color='cyan', alpha=0.5, orientation='horizontal')
    ax6.axhline(y=1.0, color='white', linestyle='--')
    ax6.set_title('Statistical Distribution', fontsize=14, color='cyan')
    ax6.set_xlabel('Frequency')
    ax6.set_ylabel('Ratio Value')
    ax6.grid(alpha=0.2)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("basil_resonance_unity.png", dpi=200)
    print("✓ Visualization saved as 'basil_resonance_unity.png'")

if __name__ == "__main__":
    generate_plots()

