import numpy as np
from mpmath import mp, zeta, dirichlet

# ==============================================================================
# 🧪 M I C R O - L A B   [ Core Engine ]
# ------------------------------------------------------------------------------
# 📜 الغاية من الكود: المحرك الرياضي الموحد (ZetaLab Supreme) لنظرية الرنين الأساسي
# 🎓 المرحلة: البنية التحتية (Laboratory Heart)
# 📐 المبدأ الرياضي: Unified Dirichlet Engines & Geometric Tail Corrections
# ⚡ النتيجة المتوقعة: توفير كافة الدوال الحسابية عالية الدقة لجميع سكريبتات المختبر
# ==============================================================================

mp.dps = 50 # Default high precision for all research

class ZetaLab:
    def __init__(self, precision=50):
        mp.dps = precision
        
    # --- CORE MATHEMATICAL FUNCTIONS ---
    @staticmethod
    def get_zeta(s):
        return zeta(mp.mpc(s))
    
    @staticmethod
    def get_zeta_derivative(s, order=1):
        return zeta(mp.mpc(s), derivative=order)
    
    @staticmethod
    def calculate_partial_sum(s, N, coefficients_func=lambda n: 1):
        """
        Calculates the partial sum S_N(s) = sum a_n * n^-s
        """
        s_mp = mp.mpc(s)
        total = mp.mpc(0)
        for n in range(1, int(N) + 1):
            a_n = coefficients_func(n)
            if a_n != 0:
                total += mp.mpc(a_n) * (mp.mpf(n) ** -s_mp)
        return total

    # --- THE GEOMETRIC TAIL (EULER-MACLAURIN) ---
    @staticmethod
    def get_tower_tail(s, N, mu=1.0, a_N=1.0):
        """
        Calculates the geometric 'Tower tail' correction.
        Sn approx L(s,a) + mu*N^(1-s)/(1-s) + 0.5*a_N*N^-s + (s/12)*a_N*N^(-s-1)
        Returns the correction to be ADDED to Sn to get the exact value L(s,a).
        """
        s_mp = mp.mpc(s)
        N_mp = mp.mpf(N)
        
        # Correction = Tail_EM(N, s)
        # S_N + Tail_EM = Exact_Value
        # Tail_EM = mu*N^(1-s)/(s-1) - 0.5*a_N*N^-s - (s/12)*a_N*N^(-s-1)
        tail = (mu * (N_mp ** (1-s_mp)) / (s_mp - 1)) - (0.5 * mp.mpc(a_N) * (N_mp ** -s_mp))
        # Optional: higher order term
        # (s/12) * a_N * N^(-s-1)
        return tail

    # --- THE HYPOTENUSE LAW (BASIL DENOMINATOR) ---
    @staticmethod
    def get_basil_denominator(sigma, t):
        """
        The Hypotenuse Law: H = sqrt((1-sigma)^2 + t^2)
        """
        return mp.sqrt((1 - mp.mpf(sigma))**2 + mp.mpf(t)**2)

    @staticmethod
    def predict_depth_resonance(sigma, t):
        """
        Predicts the normalized magnitude at a non-zero: |Sn| / N^(1-sigma) approx 1/H
        """
        H = ZetaLab.get_basil_denominator(sigma, t)
        return 1.0 / H

    # --- THE MOEBIUS POLE LAW ---
    @staticmethod
    def predict_moebius_tower_growth_rate(rho):
        """
        The Logarithmic Pole Law: |M_N(rho)| approx ln(N) / |zeta'(rho)|
        Returns the slope: 1 / |zeta'(rho)|
        """
        z_prime = zeta(mp.mpc(rho), derivative=1)
        return 1.0 / abs(z_prime)

    # --- UTILITIES ---
    @staticmethod
    def sieve_mu(N_max):
        mu = np.zeros(N_max + 1, dtype=int)
        mu[1] = 1
        primes = []
        is_prime = np.ones(N_max + 1, dtype=bool)
        for i in range(2, N_max + 1):
            if is_prime[i]:
                primes.append(i)
                mu[i] = -1
            for p in primes:
                if i * p > N_max: break
                is_prime[i * p] = False
                if i % p == 0:
                    mu[i * p] = 0
                    break
                else:
                    mu[i * p] = -mu[i]
        return mu

class DirichletCharacters:
    @staticmethod
    def eta(n): return (-1)**(n-1)
    @staticmethod
    def l_mod3(n): return [0, 1, -1][n % 3]
    @staticmethod
    def l_mod4(n): return [0, 1, 0, -1][n % 4]

