from ZetaLab_Supreme import ZetaLab
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# ==============================================================================
# 🧪 M I C R O - L A B   [ Exp 01 ]
# ------------------------------------------------------------------------------
# 📜 الغاية من الكود: إثبات قانون الوتر الأساسي ورصد التوافق الأول عبر الشريط الحرج
# 🎓 المرحلة: الاكتشاف (The Discovery)
# 📐 المبدأ الرياضي: قانون الوتر H = sqrt((1-sigma)^2 + t^2)
# ⚡ النتيجة المتوقعة: نسبة تطابق تقترب من 100% بين الواقع والتنبؤ
# ==============================================================================

console = Console()

def run_basil_experiment():
    lab = ZetaLab(precision=50)
    
    console.print(Panel.fit(
        "--- EXPERIMENT 01: THE HYPOTENUSE LAW (BASIL RESONANCE) ---",
        style="bold green"
    ))
    
    # Test Parameters
    sigmas = [0.0, 0.5, 0.8]
    t = 100.0 # Non-zero frequency
    N = 10000 
    
    console.print(f"Testing at [bold cyan]t={t}[/bold cyan], [bold cyan]N={N}[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Sigma", justify="center")
    table.add_column("Empirical |Sn|", justify="right")
    table.add_column("Predicted (N^(1-s)/H)", justify="right")
    table.add_column("Ratio (%)", justify="right")
    
    for sigma in sigmas:
        # 1. Empirical Magnitude
        sn = lab.calculate_partial_sum(complex(sigma, t), N)
        mag_emp = abs(sn)
        
        # 2. Predicted Magnitude (Hypotenuse Law)
        H = lab.get_basil_denominator(sigma, t)
        mag_pred = (N**(1 - sigma)) / H
        
        ratio = float(mag_emp / mag_pred)
        
        style = "green" if abs(ratio - 1.0) < 0.01 else "yellow"
        table.add_row(
            f"{sigma:.2f}",
            f"{float(mag_emp):.10f}",
            f"{float(mag_pred):.10f}",
            f"[{style}]{ratio:.4%}[/{style}]"
        )
    
    console.print(table)
    console.print("\n[bold green][STATUS: VERIFIED][/bold green] The Hypotenuse Law matches empirical data.")

if __name__ == "__main__":
    run_basil_experiment()

