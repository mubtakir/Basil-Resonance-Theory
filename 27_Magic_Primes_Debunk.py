# ============================================================
# اختبار فرضية "العوامل الأولية السحرية" {2,5,7,17}
# هل هي فريدة في الرنين مع أصفار زيتا؟
# ============================================================

import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations, product
from collections import defaultdict

# ضبط الدقة
mp.dps = 50
print("✅ تم ضبط الدقة إلى 50 خانة عشرية")
print("=" * 80)

# ============================================================
# الجزء 1: تعريف أصفار زيتا الأولى (قيم معروفة بدقة عالية)
# ============================================================
print("\n📊 الجزء 1: أصفار زيتا الأولى المستخدمة في الاختبار")
print("-" * 50)

# القيم الدقيقة للأصفار الأولى (من جداول أودليزكو)
ZETA_ZEROS = {
    1: mp.mpf('14.1347251417346937904572519835624702707842571156992'),
    2: mp.mpf('21.0220396387715549926284795938969027773343405249028'),
    3: mp.mpf('25.0108575801456887632137909925628218186595496725579'),
    4: mp.mpf('30.4248761258595132103118975305840913201815600237154'),
    5: mp.mpf('32.9350615877391896906623689640749034888127156035170'),
    6: mp.mpf('37.5861781588256712572177634807053328214055973508307'),
    7: mp.mpf('40.9187190121474951873981269146332543957261659627772'),
    8: mp.mpf('43.3270732809149995194961221654068057826456683718368'),
    9: mp.mpf('48.0051508811671597279424727495505163434839909982112'),
    10: mp.mpf('49.7738324776723021819167846785637240577231782996766'),
}

print("أول 10 أصفار:")
for i, t in ZETA_ZEROS.items():
    print(f"   Z{i:2d}: t = {float(t):.6f}")

# ============================================================
# الجزء 2: توليد قيم N من عوامل أولية مختلفة
# ============================================================
print("\n" + "=" * 80)
print("🧪 الجزء 2: اختبار فرضية العوامل {2,5,7,17}")
print("-" * 50)

# العوامل المزعومة "السحرية"
MAGIC_PRIMES = [2, 5, 7, 17]

# توليد جميع الأعداد الممكنة من هذه العوامل حتى حد معين
def generate_numbers_from_primes(primes, max_val):
    """توليد جميع الأعداد التي تتكون فقط من العوامل الأولية المعطاة"""
    numbers = [1]
    for p in primes:
        new_numbers = []
        for n in numbers:
            val = n
            while val <= max_val:
                if val not in numbers:
                    new_numbers.append(val)
                val *= p
        numbers.extend(new_numbers)
    return sorted(set(numbers))

# مجموعة الأعداد "السحرية" (تتكون فقط من 2,5,7,17)
magic_numbers = generate_numbers_from_primes(MAGIC_PRIMES, 500)
# استبعاد 1
magic_numbers = [n for n in magic_numbers if n > 1]
print(f"\n📦 الأعداد المتكونة من العوامل {MAGIC_PRIMES} حتى 500:")
print(f"   {magic_numbers[:20]}..." if len(magic_numbers) > 20 else f"   {magic_numbers}")

# مجموعة تحكم: أعداد عشوائية (غير سحرية)
import random
random.seed(42)  # للتكرار
control_numbers = [random.randint(20, 500) for _ in range(50)]
control_numbers = list(set(control_numbers))  # إزالة التكرار
control_numbers = [n for n in control_numbers if n not in magic_numbers]

print(f"\n🎲 مجموعة التحكم (أعداد عادية): {len(control_numbers)} عدد")
print(f"   أول 10: {control_numbers[:10]}")

# ============================================================
# الجزء 3: قياس "عمق الرنين" لكل N
# ============================================================
print("\n" + "=" * 80)
print("📐 الجزء 3: قياس عمق الرنين (كلما كان العمق أكبر، كلما كان الرنين أقوى)")
print("-" * 50)

def resonance_depth(zero_t, N):
    """
    حساب "عمق الرنين" - مقياس لمدى قرب المجموع من القيمة المتوقعة
    العمق الأكبر = رنين أقوى
    """
    sigma = mp.mpf('0.5')
    s = mp.mpc(sigma, zero_t)
    
    # حساب S_N
    S_N = mp.mpc(0)
    for n in range(1, N + 1):
        S_N += mp.mpf(n) ** (-s)
    
    # القيمة النظرية (قانون الوتر)
    theoretical = mp.mpf(1) / mp.sqrt((1 - sigma)**2 + zero_t**2)
    actual = mp.fabs(S_N) / (mp.mpf(N) ** (1 - sigma))
    
    # العمق = مقلوب الخطأ النسبي (كلما كان الخطأ أصغر، العمق أكبر)
    error = mp.fabs(actual - theoretical)
    if error == 0:
        return float('inf')
    depth = 1 / float(error)
    return depth

def test_number_for_zeros(number, zeros_dict):
    """اختبار عدد معين على جميع الأصفار وجمع النتائج"""
    results = {}
    for idx, t in zeros_dict.items():
        depth = resonance_depth(t, number)
        results[idx] = depth
    return results

# اختبار جميع الأعداد السحرية على أول 8 أصفار (كما في البحث الأصلي)
print("\n🔍 اختبار الأعداد السحرية على أول 8 أصفار:")
print(f"{'N':>5} | {'متوسط العمق':>15} | {'مرتبة':>6} | {'التركيب':>20}")
print("-" * 55)

magic_scores = {}
for N in magic_numbers[:30]:  # نأخذ أول 30 عددًا سحريًا
    depths = test_number_for_zeros(N, {k: ZETA_ZEROS[k] for k in range(1, 9)})
    avg_depth = np.mean([d for d in depths.values() if d != float('inf')])
    magic_scores[N] = avg_depth

# ترتيب الأعداد حسب العمق
sorted_magic = sorted(magic_scores.items(), key=lambda x: x[1], reverse=True)

for i, (N, score) in enumerate(sorted_magic[:10]):
    # تحليل التركيب
    factors = []
    n_temp = N
    for p in MAGIC_PRIMES:
        while n_temp % p == 0:
            factors.append(p)
            n_temp //= p
    composition = " × ".join(map(str, factors))
    print(f"{N:5d} | {score:15.2e} | {i+1:4d} | {composition:>20}")

# ============================================================
# الجزء 4: مقارنة مع الأعداد العادية (التحكم السلبي)
# ============================================================
print("\n" + "=" * 80)
print("⚖️ الجزء 4: مقارنة مع الأعداد العادية (ليست من العوامل السحرية)")
print("-" * 50)

control_scores = {}
for N in control_numbers[:30]:
    depths = test_number_for_zeros(N, {k: ZETA_ZEROS[k] for k in range(1, 9)})
    avg_depth = np.mean([d for d in depths.values() if d != float('inf')])
    control_scores[N] = avg_depth

sorted_control = sorted(control_scores.items(), key=lambda x: x[1], reverse=True)

print("\n🏆 أفضل 10 أعداد عادية (غير سحرية):")
print(f"{'N':>5} | {'متوسط العمق':>15} | {'مرتبة مطلقة':>12}")
print("-" * 40)
for i, (N, score) in enumerate(sorted_control[:10]):
    print(f"{N:5d} | {score:15.2e} | {i+1:4d}")

# ============================================================
# الجزء 5: التحليل الإحصائي - هل الأعداد السحرية أفضل حقًا؟
# ============================================================
print("\n" + "=" * 80)
print("📊 الجزء 5: التحليل الإحصائي (هل الفرق معنوي؟)")
print("-" * 50)

# جمع جميع الدرجات
all_magic_scores = list(magic_scores.values())
all_control_scores = list(control_scores.values())

avg_magic = np.mean(all_magic_scores)
avg_control = np.mean(all_control_scores)
std_magic = np.std(all_magic_scores)
std_control = np.std(all_control_scores)

print(f"\n📈 الإحصائيات:")
print(f"   الأعداد السحرية ({len(all_magic_scores)} عدد):")
print(f"      المتوسط: {avg_magic:.2e}")
print(f"      الانحراف المعياري: {std_magic:.2e}")
print(f"\n   الأعداد العادية ({len(all_control_scores)} عدد):")
print(f"      المتوسط: {avg_control:.2e}")
print(f"      الانحراف المعياري: {std_control:.2e}")

# هل المتوسطات مختلفة بشكل معنوي؟
ratio = avg_magic / avg_control if avg_control > 0 else float('inf')
print(f"\n📐 نسبة تحسن الأعداد السحرية: {ratio:.2f} مرة")

if ratio > 1.5:
    print(f"   ✅ الأعداد السحرية أفضل بكثير من العادية (فرق كبير)")
elif ratio > 1.1:
    print(f"   ⚠️ الأعداد السحرية أفضل قليلاً من العادية (فرق طفيف)")
else:
    print(f"   ❌ لا فرق معنوي - الأعداد السحرية ليست أفضل من العادية")

# ============================================================
# الجزء 6: هل تظهر عوامل جديدة عند أصفار أعلى؟
# ============================================================
print("\n" + "=" * 80)
print("🔮 الجزء 6: هل العوامل {2,5,7,17} فريدة عند أصفار أعلى؟")
print("-" * 50)

# اختبار الصفر العاشر (t ≈ 49.77)
print("\n📌 اختبار الصفر العاشر (Z10, t ≈ 49.77):")
print(f"{'N':>5} | {'التركيب':>20} | {'العمق عند Z10':>20}")
print("-" * 55)

# نأخذ أفضل 5 أعداد سحرية وأفضل 5 أعداد عادية
test_numbers = sorted_magic[:5] + sorted_control[:5]

for N, _ in test_numbers:
    depth_z10 = resonance_depth(ZETA_ZEROS[10], N)
    # تحليل التركيب
    factors = []
    n_temp = N
    for p in [2, 3, 5, 7, 11, 13, 17, 19]:
        while n_temp % p == 0:
            factors.append(p)
            n_temp //= p
    if n_temp > 1:
        factors.append(n_temp)
    composition = " × ".join(map(str, factors))
    
    status = "⭐ سحري" if N in magic_scores else "عادي"
    print(f"{N:5d} | {composition:>20} | {float(depth_z10):16.2e} | {status}")

# ============================================================
# الخلاصة النهائية
# ============================================================
print("\n" + "=" * 80)
print("🏁 الخلاصة النهائية: هل العوامل {2,5,7,17} سحرية حقًا؟")
print("=" * 80)

print("""
📋 قراءة النتائج:

1. إذا كانت نسبة التحسن > 1.5:
   → العوامل السحرية أفضل بكثير (قد يكون هناك تأثير حقيقي)

2. إذا كانت نسبة التحسن بين 1.1 و 1.5:
   → فرق طفيف، قد يكون صدفة إحصائية

3. إذا كانت نسبة التحسن < 1.1:
   → لا فرق معنوي، العوامل {2,5,7,17} مجرد صدفة

4. إذا ظهرت عوامل جديدة عند Z10:
   → العوامل تعتمد على نطاق التردد، وليست عالمية

═══════════════════════════════════════════════════════════════
🔬 الحكم النهائي سيصدر بناءً على الأرقام أعلاه.
═══════════════════════════════════════════════════════════════
""")