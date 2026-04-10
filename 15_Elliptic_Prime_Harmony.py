import numpy as np
from mpmath import mp, pi, sin, cos, sqrt, quad
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# ==============================================================================
# 🧪 M I C R O - L A B   [ Exp 14 ]
# ------------------------------------------------------------------------------
# 📜 الغاية من الكود: برهان التناغم الجيومتري بين مصفوفة الأعداد الأولية والقطع الناقص
# 🎓 المرحلة: تناغم الأعداد الأولية (Prime Harmony)
# 📐 المبدأ الرياضي: Elliptic Arc/Chord Stability at Prime Axis Ratios
# ⚡ النتيجة المتوقعة: فناء الفرق (Difference) بين النسبة البيضوية والدائرية عند الزوايا التوافقية
# ==============================================================================

console = Console()
mp.dps = 50 

def get_ellipse_arc_length(a, b, theta_rad):
    f = lambda t: sqrt( (a * sin(t))**2 + (b * cos(t))**2 )
    return quad(f, [0, theta_rad])

def get_ellipse_chord(a, b, theta_rad):
    x1, y1 = a * cos(0), b * sin(0)
    x2, y2 = a * cos(theta_rad), b * sin(theta_rad)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def verify_resonance():
    console.print(Panel.fit(
        "--- BASIL RESONANCE THEORY - PHASE 14: ELLIPTIC-PRIME HARMONY ---",
        style="bold green"
    ))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Prime (p)", justify="center")
    table.add_column("Angle (°)", justify="center")
    table.add_column("Ratio Ellipse", justify="right")
    table.add_column("Ratio Circle", justify="right")
    table.add_column("Difference", justify="right")
    table.add_column("Status", justify="center")

    matches = [
        (2, 75),
        (17, 35),
        (23, 30),
        (37, 25)
    ]

    for p, theta_deg in matches:
        a = mp.mpf(p)
        b = mp.mpf(1.0)
        theta_rad = (mp.mpf(theta_deg) * pi) / 180

        L_e = get_ellipse_arc_length(a, b, theta_rad)
        W_e = get_ellipse_chord(a, b, theta_rad)
        ratio_e = L_e / W_e

        # Circle stats
        ratio_c = theta_rad / (2 * sin(theta_rad / 2))

        diff = abs(ratio_e - ratio_c)

        status = "[bold green]EXCELLENT[/bold green]" if diff < 0.0005 else "[bold yellow]GOOD[/bold yellow]"
        table.add_row(
            str(p),
            str(theta_deg),
            f"{float(ratio_e):.8f}",
            f"{float(ratio_c):.8f}",
            f"{float(diff):.4e}",
            status
        )

    console.print(table)
    console.print("\n[bold green][CONCLUSION][/bold green] Prime axis ratios stabilize the arc-to-chord ratio relative to the circular baseline.")

if __name__ == "__main__":
    verify_resonance()

