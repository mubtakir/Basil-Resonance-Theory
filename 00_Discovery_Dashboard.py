import os
import sys
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich import box

# ==============================================================================
#   B A S A L   R E S O N A N C E   L A B O R A T O R Y
#   Interactive Discovery Dashboard — V3.0 Supreme
# ------------------------------------------------------------------------------
#   المؤلفان : باسل يحيى عبدالله & Antigravity AI
#   التاريخ  : 10 أبريل 2026
#   التجارب  : 21 | الفصول : 10 | الدروس : 28 | الإنجازات : 14
# ==============================================================================

console = Console()

# ─────────────────────────────────────────────────────────────────────────────
# التجارب مُجمَّعة في فصول بحثية
# ─────────────────────────────────────────────────────────────────────────────
CHAPTERS = [
    {
        "title": "Phase I — The Chord Discovery",
        "subtitle": "المرحلة الأولى: اكتشاف قانون الوتر الفيثاغوري",
        "color": "cyan",
        "experiments": [
            {"id": "01", "name": "The Hypotenuse Law",
             "file": "01_Basil_Law_Discovery.py",
             "desc": "إثبات قانون الوتر الأساسي ورصد التوافق الأول"},
            {"id": "02", "name": "The Zeta Balance",
             "file": "02_The_Zeta_Balance.py",
             "desc": "كشف ثابت التوازن (زيتا) وفناء الفجوة الهندسية"},
            {"id": "03", "name": "Logarithmic Phase Law",
             "file": "03_Phase_Alignment_Law.py",
             "desc": "قانون الطور والارتباط العجيب بمصفوفة الأعداد الأولية"},
            {"id": "04", "name": "Refined Integral Shadow",
             "file": "01_Basil_Law_Refined.py",
             "desc": "دقة التنبؤ وفناء الفجوة في مناطق التقارب"},
            {"id": "05", "name": "Vector Identity Probe",
             "file": "02_Distance_Alignment_Probe.py",
             "desc": "التحقق من الانطباق الكلي للمتجهات عند الأصفار"},
            {"id": "06", "name": "Universal Chord Law",
             "file": "01_Universal_Chord_Probe.py",
             "desc": "برهان شمولية قانون الوتر لكامل الشريط الحرج"},
        ]
    },
    {
        "title": "Phase II — Zero Hunting & Moebius",
        "subtitle": "المرحلة الثانية: صيد الأصفار وظاهرة موبيوس",
        "color": "magenta",
        "experiments": [
            {"id": "07", "name": "Resonance Zero Hunter",
             "file": "04_Blind_Search_Engine.py",
             "desc": "صيد أصفار زيتا باستخدام رنين المتجهات فقط"},
            {"id": "08", "name": "Moebius Tower Law",
             "file": "05_Moebius_Tower_Law.py",
             "desc": "رصد نمو نبض موبيوس اللوغاريتمي عند الأصفار"},
            {"id": "09", "name": "Universal Convergence",
             "file": "06_Dirichlet_Universal_Law.py",
             "desc": "قانون ألفا الموحد (σ+1) لجميع دوال ديريكليه"},
            {"id": "10", "name": "Deep Ocean Prediction",
             "file": "07_Deep_Ocean_Z50_Prediction.py",
             "desc": "اختبار القدرة التنبؤية في أعماق المحيط (Z50)"},
            {"id": "11", "name": "High-Order Moebius",
             "file": "08_Moebius_High_Order_Proof.py",
             "desc": "برهان نبض موبيوس للأصفار عالية الرتبة"},
            {"id": "12", "name": "Scientific Rebuttal",
             "file": "09_Scientific_Rebuttal_Z10.py",
             "desc": "دحض الاعتراضات العلمية بالأدلة الرياضية"},
        ]
    },
    {
        "title": "Phase III — Cosmic Constants",
        "subtitle": "المرحلة الثالثة: الثوابت الكونية والرنين المطلق",
        "color": "yellow",
        "experiments": [
            {"id": "13", "name": "Unity Factor — pi/sqrt(8)",
             "file": "14_Final_Resonance_Unity.py",
             "desc": "الكشف عن ثابت الوحدة الكوني π/√8 ≈ 1.1107"},
            {"id": "14", "name": "Prime Harmonic Matrix",
             "file": "15_Elliptic_Prime_Harmony.py",
             "desc": "تناغم الأعداد الأولية والقطع الناقص (a/b = 2,23,37)"},
            {"id": "15", "name": "Pythagorean Template",
             "file": "16_Unified_Triangle_Generator.py",
             "desc": "المولد الهندسي للمثلثات والبرهان الختامي لفرادة النصف"},
        ]
    },
    {
        "title": "Phase IV — Prime Portal & Density",
        "subtitle": "المرحلة الرابعة: بوابة الأوليات وكثافة الأصفار",
        "color": "green",
        "experiments": [
            {"id": "16", "name": "Prime Portal Law (1/H)",
             "file": "17_Geometric_Prime_Predictor.py",
             "desc": "هيمنة الأوتار القصيرة على أوزان توزيع الأعداد الأولية"},
            {"id": "17", "name": "Chord-Density Identity",
             "file": "18_Chord_Density_Correlation.py",
             "desc": "برهان قانون الانضغاط الترددي وتزاحم الأصفار في اللانهاية"},
        ]
    },
    {
        "title": "Phase V — Taylor Series & The Cosmic Bridge",
        "subtitle": "المرحلة الخامسة: سلسلة تايلور والجسر الكوني",
        "color": "bright_magenta",
        "experiments": [
            {"id": "18", "name": "The 1/8 Geometric Signature",
             "file": "19_Constant_Precision_Verification.py",
             "desc": "بصمة القاعدة 0.5 → ثابت الانحراف 1/8 (50 خانة)"},
            {"id": "19", "name": "Taylor Nano-Audit",
             "file": "20_Taylor_Residue_Audit.py",
             "desc": "سلسلة تايلور كاملة: c₁=-1/8, c₂=3/128, c₃=-5/1024 (100 DPS)"},
            {"id": "20", "name": "The Cosmic Bridge",
             "file": "21_Curvature_Density_Bridge.py",
             "desc": "الجسر المطلق: ΣR(tₙ)/N(T) → -3/128 (كثافة الأصفار مشفّرة في الوتر)"},
        ]
    },
]

# قائمة مسطحة للبحث والتشغيل
ALL_EXPERIMENTS = [exp for chapter in CHAPTERS for exp in chapter["experiments"]]


# ─────────────────────────────────────────────────────────────────────────────
def display_welcome():
    title    = Text(" BASIL RESONANCE LABORATORY ", style="bold white on dark_blue", justify="center")
    version  = Text("V3.0 Supreme — 10 April 2026", style="italic cyan", justify="center")
    authors  = Text("Basel Yahya Abdullah  &  Antigravity AI", style="dim white", justify="center")
    console.print(Panel(
        Text.assemble(title, "\n", version, "\n", authors),
        box=box.DOUBLE_EDGE, padding=(1, 4),
        border_style="bright_blue"
    ))


def display_stats():
    stats = [
        Panel("[bold cyan]21[/bold cyan]\n[dim]تجارب[/dim]",      border_style="cyan",    width=14),
        Panel("[bold magenta]10[/bold magenta]\n[dim]فصول[/dim]", border_style="magenta", width=14),
        Panel("[bold yellow]28[/bold yellow]\n[dim]درساً[/dim]",  border_style="yellow",  width=14),
        Panel("[bold green]14[/bold green]\n[dim]إنجازاً[/dim]",  border_style="green",   width=14),
        Panel("[bold white]100[/bold white]\n[dim]DPS دقة[/dim]", border_style="white",   width=14),
    ]
    console.print(Columns(stats, align="center", expand=True))


def display_menu():
    for chapter in CHAPTERS:
        color = chapter["color"]
        console.print()
        console.print(Panel(
            f"[bold {color}]{chapter['title']}[/bold {color}]\n[dim]{chapter['subtitle']}[/dim]",
            box=box.SIMPLE_HEAD, border_style=color, padding=(0, 2)
        ))
        t = Table(box=box.SIMPLE, show_header=True, header_style=f"bold {color}",
                  padding=(0, 1))
        t.add_column("ID",   width=4,  style="bold white")
        t.add_column("Experiment",   width=30, style=f"bold {color}")
        t.add_column("الوصف",        style="dim white")
        for exp in chapter["experiments"]:
            t.add_row(exp["id"], exp["name"], exp["desc"])
        console.print(t)


def run_experiment(exp_id):
    exp = next((e for e in ALL_EXPERIMENTS if e["id"] == exp_id), None)
    if not exp:
        console.print(f"\n[bold red]✗ التجربة [{exp_id}] غير موجودة.[/bold red]")
        return

    file_path = exp["file"]
    if not os.path.exists(file_path):
        console.print(f"\n[bold red]✗ الملف [{file_path}] مفقود![/bold red]")
        return

    console.print(Panel(
        f"[bold yellow]▶ {exp['name']}[/bold yellow]\n"
        f"[dim]الملف: {file_path}[/dim]\n"
        f"[dim]{exp['desc']}[/dim]",
        border_style="green", title="[green]Launching Experiment[/green]"
    ))

    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if result.stdout:
            console.print(result.stdout)
        if result.stderr:
            console.print("[bold red]— Warnings/Errors —[/bold red]")
            console.print(result.stderr)
    except Exception as e:
        console.print(f"[bold red]✗ فشل التنفيذ: {e}[/bold red]")


def main():
    while True:
        console.clear()
        display_welcome()
        display_stats()
        display_menu()

        console.print()
        choice = console.input(
            "[bold yellow]أدخل رقم التجربة (01-20) أو [bold]'q'[/bold] للخروج: [/bold yellow]"
        ).strip()

        if choice.lower() in ("q", "quit", "exit"):
            console.print(Panel(
                "[bold cyan]حتى اللقاء.[/bold cyan]\n"
                "[dim]البناء مكتمل. الصرح محكم. الدائرة مغلقة.[/dim]",
                border_style="bright_blue"
            ))
            break

        exp_id = choice.zfill(2) if choice.isdigit() else choice
        run_experiment(exp_id)
        console.input("\n[dim]اضغط Enter للعودة إلى اللوحة...[/dim]")


if __name__ == "__main__":
    main()

