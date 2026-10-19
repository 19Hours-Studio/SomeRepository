"""Climate helpers: hours below a threshold, degree-days, warm-window days, vapour pressure, insolation, wind.

All temperatures in deg C unless a name ends in _K. Monthly normals are dicts {'Jan': -38.6, ...}
(see kit.data.monthly(site)).
"""
import math

from . import data

_MONTHS = data.MONTHS
_DAYS = data.MONTH_DAYS


def _check_monthly(monthly):
    if not isinstance(monthly, dict) or not monthly:
        raise ValueError("monthly must be a non-empty dict like {'Jan': -38.6}")
    for m, t in monthly.items():
        if m not in _DAYS:
            raise ValueError(f"unknown month key {m!r}; use {_MONTHS}")
        if not -90.0 < t < 50.0:
            raise ValueError(f"implausible monthly mean {t} C for {m}")


def normal_cdf(z):
    """Standard normal CDF Phi(z) = 0.5*(1+erf(z/sqrt2))."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def hours_below(monthly, threshold_C, sd_K=6.0):
    """Expected hours per year with air temperature <= threshold.

    Model: hourly T within each month ~ Normal(monthly mean, sd); hours = sum_m 24*days_m*Phi((thr-mu_m)/sd).
    Units: C, K, hours. Validity: screening only; sd 5-8 K spans the plausible range for continental
    Siberia and changes the answer by ~2x near the tail (use the range, not a point).
    Source: used in round2/audit_a, critic_a/calc/climate_hours.py, rt_a, erp2_a (hourly station data were
    unreachable). Only months present in ``monthly`` are counted (missing months contribute 0).
    """
    _check_monthly(monthly)
    if sd_K <= 0:
        raise ValueError("sd_K must be > 0")
    return sum(24.0 * _DAYS[m] * normal_cdf((threshold_C - mu) / sd_K) for m, mu in monthly.items())


def hours_above(monthly, threshold_C, sd_K=6.0):
    """Expected hours with T >= threshold (complement of hours_below over the months given)."""
    _check_monthly(monthly)
    tot = sum(24.0 * _DAYS[m] for m in monthly)
    return tot - hours_below(monthly, threshold_C, sd_K)


def degree_days(monthly, base_C=0.0):
    """Freezing and thawing degree-days from monthly normals: returns (FDD, TDD) in C*day.

    FDD = sum over months with mean < base of (base - T)*days; TDD likewise above base.
    Monthly means understate FDD/TDD slightly near the shoulder months (sign changes within a month).
    Source: genius/audit_final/audit_calc.py (Verkhoyansk ~6,690 C*d); erp2_b/idea3_icefloat.py.
    """
    _check_monthly(monthly)
    fdd = sum((base_C - t) * _DAYS[m] for m, t in monthly.items() if t < base_C)
    tdd = sum((t - base_C) * _DAYS[m] for m, t in monthly.items() if t > base_C)
    return fdd, tdd


def daily_temperatures(monthly12):
    """365 daily means by linear interpolation between mid-month normals (needs all 12 months)."""
    _check_monthly(monthly12)
    if len(monthly12) != 12:
        raise ValueError("daily_temperatures needs all 12 monthly means")
    vals = [monthly12[m] for m in _MONTHS]
    mids, c = [], 0.0
    for m in _MONTHS:
        mids.append(c + _DAYS[m] / 2.0)
        c += _DAYS[m]
    out = []
    for day in range(365):
        d = day + 0.5
        for i in range(12):
            j = (i + 1) % 12
            a = mids[i]
            b = mids[j] + (365 if j == 0 else 0)
            dd = d if d >= mids[0] else d + 365
            if a <= dd < b:
                out.append(vals[i] + (vals[j] - vals[i]) * (dd - a) / (b - a))
                break
    return out


def days_above(monthly12, threshold_C=8.0):
    """Number of days per year whose interpolated daily mean exceeds threshold (e.g. non-heating days > 8 C).

    Source: genius/audit_final/audit_calc.py nonheating(): Verkhoyansk 90 d, Chokurdakh 51 d, Srednekolymsk 78-80 d.
    """
    return sum(1 for t in daily_temperatures(monthly12) if t > threshold_C)


def psat_ice(T_C):
    """Saturation vapour pressure over ice, Pa. Murphy & Koop 2005 (QJRMS 131:1539), valid > 110 K.

    p = exp(9.550426 - 5723.265/T + 3.53068 ln T - 0.00728332 T). Source: roast/roast.py, genius/gate_4.
    """
    T = T_C + 273.15
    if T < 110.0 or T_C > 0.01:
        raise ValueError("psat_ice valid for 110 K < T <= 273.16 K")
    return math.exp(9.550426 - 5723.265 / T + 3.53068 * math.log(T) - 0.00728332 * T)


def psat_water(T_C):
    """Saturation vapour pressure over (supercooled) liquid water, Pa. Magnus/Alduchov-Eskridge form
    611.2*exp(17.62 T/(243.12+T)); valid -45..+60 C to ~0.3%. Source: round2/audit_a/calc_frost_sep.py."""
    if not -45.0 <= T_C <= 60.0:
        raise ValueError("psat_water valid -45..60 C")
    return 611.2 * math.exp(17.62 * T_C / (243.12 + T_C))


def vapour_density(T_C, rh=1.0, over="ice"):
    """Water vapour density kg/m3 at temperature T_C and relative humidity rh (0-1) over ice or water."""
    if not 0.0 <= rh <= 1.0:
        raise ValueError("rh must be 0-1")
    e = psat_ice(T_C) if (over == "ice" and T_C <= 0) else psat_water(T_C)
    return rh * e * 0.018015 / (data.R_GAS * (T_C + 273.15))


def air_density(T_C, p_Pa=101325.0):
    """Dry-air density kg/m3 = p/(287.05 T)."""
    if T_C <= -273.15 or p_Pa <= 0:
        raise ValueError("impossible state")
    return p_Pa / (287.05 * (T_C + 273.15))


def toa_daily_mean_irradiance(lat_deg, doy, solar_constant=1361.0):
    """Extraterrestrial daily-mean irradiance on a horizontal plane, W/m2 (Duffie & Beckman eq. 1.10.3).

    H0/day = S/pi*(1+0.033cos(2 pi n/365))*(cos phi cos d sin ws + ws sin phi sin d), d = 23.45 sin(360(284+n)/365).
    Multiply by a clearness index Kt (0.40-0.60 typical) for surface global irradiance.
    Validity: |lat| <= 90; polar day/night handled (ws clipped). Source: genius/gate_9, audit_evo_2/check5.py.
    """
    if not -90 <= lat_deg <= 90 or not 1 <= doy <= 366:
        raise ValueError("lat -90..90, doy 1..366")
    phi = math.radians(lat_deg)
    d = math.radians(23.45 * math.sin(math.radians(360.0 * (284 + doy) / 365.0)))
    x = max(-1.0, min(1.0, -math.tan(phi) * math.tan(d)))
    ws = math.acos(x)
    E = 1 + 0.033 * math.cos(2 * math.pi * doy / 365.0)
    return solar_constant / math.pi * E * (math.cos(phi) * math.cos(d) * math.sin(ws) + ws * math.sin(phi) * math.sin(d))


def friction_velocity(U10, z0, z=10.0):
    """Neutral log-law friction velocity u* = kappa U(z)/ln(z/z0), m/s. z0 roughness length (m).
    Source: round2/audit_b/c4_deflation.py, critic_b. Valid neutral stratification; stable Arctic air lowers u*."""
    if U10 < 0 or z0 <= 0 or z <= z0:
        raise ValueError("need U10>=0, 0<z0<z")
    return data.KAPPA * U10 / math.log(z / z0)
