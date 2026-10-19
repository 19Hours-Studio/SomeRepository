"""Statistics for 'can a pilot prove it?' checks: exact Poisson interval, zero-failure bounds, sample sizes
for a mean, a proportion and a two-arm comparison, counting precision. stdlib only.
"""
import math


def normal_cdf(z):
    """Standard normal CDF."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def normal_ppf(p):
    """Standard normal quantile by bisection (|error| < 1e-10)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p in (0,1)")
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if normal_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _gammainc_lower_reg(a, x):
    """Regularized lower incomplete gamma P(a,x) (Numerical Recipes series / continued fraction)."""
    if x <= 0:
        return 0.0
    lnpre = -x + a * math.log(x) - math.lgamma(a)
    if x < a + 1.0:
        term = s = 1.0 / a
        n = 0
        while abs(term) > abs(s) * 1e-15 and n < 10000:
            n += 1
            term *= x / (a + n)
            s += term
        return s * math.exp(lnpre)
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, 10000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        d = tiny if abs(d) < tiny else d
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < 1e-15:
            break
    return 1.0 - math.exp(lnpre) * h


def _gamma_quantile(a, p):
    lo, hi = 0.0, max(10.0, a * 10 + 50)
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if _gammainc_lower_reg(a, mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def poisson_ci(count, conf=0.95):
    """Exact (Garwood) two-sided interval for a Poisson mean given an observed count:
    lower = Gamma^-1(alpha/2; n), upper = Gamma^-1(1-alpha/2; n+1) (= chi2/2). Returns (low, high).
    n=5 -> (1.62, 11.67), i.e. 0.32-2.3x the observed rate (genius/audit_evo_1: 3-10 detachment cycles a
    season cannot pin a rate). Reference: Garwood 1936."""
    if count < 0 or int(count) != count:
        raise ValueError("count must be a non-negative integer")
    if not 0 < conf < 1:
        raise ValueError("conf in (0,1)")
    a = 1 - conf
    low = 0.0 if count == 0 else _gamma_quantile(count, a / 2)
    high = _gamma_quantile(count + 1, 1 - a / 2)
    return low, high


def zero_failure_upper_bound(n_trials, conf=0.95):
    """Exact one-sided upper bound on a failure/loss probability after n trials with ZERO failures:
    p < 1 - (1-conf)^(1/n). n=20 -> 13.9%, 59 -> 5.0%, 299 -> 1.0% (roast/roast.py).
    DISAGREEMENT resolved: several runs used the rule of three (3/n), an approximation good for n > ~30;
    the exact form is used here (see rule_of_three)."""
    if n_trials < 1:
        raise ValueError("n_trials >= 1")
    if not 0 < conf < 1:
        raise ValueError("conf in (0,1)")
    return 1.0 - (1.0 - conf) ** (1.0 / n_trials)


def rule_of_three(n_trials):
    """Approximate 95% upper bound 3/n for zero events in n trials (Hanley & Lippman-Hand 1983)."""
    if n_trials < 1:
        raise ValueError("n_trials >= 1")
    return 3.0 / n_trials


def trials_for_zero_failure(p_max, conf=0.95):
    """Failure-free trials needed to show p < p_max: n = ln(1-conf)/ln(1-p) (5% -> 59; 1% -> 299)."""
    if not 0 < p_max < 1:
        raise ValueError("p_max in (0,1)")
    return math.ceil(math.log(1 - conf) / math.log(1 - p_max) - 1e-9)


def sample_size_mean(cv, rel_error, z=1.96):
    """Samples to estimate a mean to +/- rel_error (fraction) with coefficient of variation cv:
    n = (z cv / e)^2. Placer grade CV 0.6-1.0 between 1 m3 samples -> 580-1,600 samples to see 5% at 2 sigma
    (round2/critic_b)."""
    if cv <= 0 or rel_error <= 0 or z <= 0:
        raise ValueError("cv, rel_error, z > 0")
    return (z * cv / rel_error) ** 2


def sample_size_two_arms(cv, ratio, alpha=0.05, power=0.80):
    """Samples per arm to detect a multiplicative difference 'ratio' between two lognormal-ish arms:
    n = 2 (z_{1-a/2} + z_{power})^2 cv^2 / ln(ratio)^2. Source: genius/audit_final (cv 0.3-0.5, 1.16x ->
    64-178 block-months per arm)."""
    if cv <= 0 or ratio <= 0 or ratio == 1:
        raise ValueError("cv > 0, ratio > 0 and != 1")
    za, zb = normal_ppf(1 - alpha / 2), normal_ppf(power)
    return 2 * (za + zb) ** 2 * cv ** 2 / math.log(ratio) ** 2


def sample_size_proportion(p, half_width, conf=0.95):
    """Trials to estimate a proportion p to +/- half_width (absolute): n = z^2 p(1-p)/hw^2.
    5% +/- 2% -> 456 (critic_b); a 45% split +/- 3 points -> ~1,060 tracer grains (audit_a)."""
    if not 0 < p < 1 or half_width <= 0:
        raise ValueError("0<p<1, half_width>0")
    z = normal_ppf(1 - (1 - conf) / 2)
    return z * z * p * (1 - p) / half_width ** 2


def counts_for_precision(rel_error, z=2.0):
    """Poisson counts (e.g. gold grains) needed for relative precision e at z sigma: N = (z/e)^2
    (5% at 2 sigma -> 1,600 grains; Clifton et al. 1969: ~20 particles for +/-50%)."""
    if rel_error <= 0 or z <= 0:
        raise ValueError("rel_error, z > 0")
    return (z / rel_error) ** 2


def all_succeed(p_each, n):
    """Probability that n independent trials all succeed = p^n (e.g. 8 random-polarity stages: 0.5^8 = 0.4%)."""
    if not 0 <= p_each <= 1 or n < 0:
        raise ValueError("0<=p<=1, n>=0")
    return p_each ** n
