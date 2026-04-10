import numpy as np

def basil_stress_test(t_target, N_limit=1000000):
    """اختبار فرضية باسل عند ترددات عالية جداً"""
    n = np.arange(1, N_limit + 1, dtype=np.float64)
    
    # حساب المجموع بدقة عالية
    S = np.sum(n**(-0.5 + 1j * t_target))
    
    # القيمة المقاربية المتوقعة (صيغة باسل)
    theory_magnitude = 1.0 / np.sqrt(0.25 + t_target**2)
    computed_magnitude = np.abs(S) / np.sqrt(N_limit)
    
    error = abs(computed_magnitude - theory_magnitude)
    return computed_magnitude, theory_magnitude, error

# اختبار عند قيمة t ضخمة (ليست صفراً) وأخرى قريبة من صفر معروف
t_normal = 1000.0
t_near_zero = 1000.153  # قيمة افتراضية قريبة من صفر ضخم

print(f"--- اختبار التردد العالي (N = 1,000,000) ---")
for t in [t_normal, t_near_zero]:
    comp, theo, err = basil_stress_test(t)
    print(f"\nعند t = {t}:")
    print(f"المقدار المحسوب: {comp:.10f}")
    print(f"المقدار النظري:  {theo:.10f}")
    print(f"الخطأ المطلق:   {err:.10e}")
