import numpy as np
import matplotlib.pyplot as plt

def chi_4(n):
    """تعريف الشخصية المقياسية 4: 1 للأعداد 1،5،9... و -1 للأعداد 3،7،11... و 0 للزوجي"""
    rem = n % 4
    if rem == 1: return 1
    if rem == 3: return -1
    return 0

def L_sum(t, sigma, N):
    """حساب المجموع الجزئي لدالة L"""
    n = np.arange(1, N + 1)
    # تطبيق الشخصية chi_4 على المصفوفة
    chi_values = np.array([chi_4(x) for x in n])
    
    # حساب الحدود n^(-sigma + it)
    term = chi_values * (n**(-sigma + 1j * t))
    return np.sum(term)

# إعدادات التجربة
N = 100000
sigma = 0.5
# أول صفر معروف لدالة L(s, chi_4) هو تقريبا 6.0209
t_zeros = [6.0209489, 10.2437703, 12.9881038] 
t_test = np.linspace(1, 15, 500)

errors = []
for t in t_test:
    S = L_sum(t, sigma, N)
    # المعادلة المتوقعة لدالة L تختلف قليلاً في المعامل الثابت
    # لكننا سنراقب سلوك "الانهيار" في القيمة المطلقة للمجموع
    errors.append(np.abs(S) / np.sqrt(N))

# الرسم البياني
plt.figure(figsize=(10, 6))
plt.plot(t_test, errors, label='Magnitude |S_N| / sqrt(N)')
for z in t_zeros:
    plt.axvline(x=z, color='r', linestyle='--', alpha=0.5, label=f'Known Zero: {z}' if z==6.0209489 else "")

plt.title('Testing "Basil Hypothesis" on Dirichlet L-function ($\chi_4$)')
plt.xlabel('t (Imaginary part)')
plt.ylabel('Normalized Magnitude')
plt.legend()
plt.grid(True)
plt.show()
