"""Economics for screening: capital recovery, levelised cost, break-even volume, cost of carrying work
ahead, ratio vs baseline and the gate verdict, cost per recovered unit, parity recovery, loss tolerance,
market share, rate x time season capacity.

Currency-agnostic: use one currency per call (kit.data has FX 84 RUB/USD [L]).
"""
import math

from . import data


def _pos(name, v):
    if v is None or not v > 0:
        raise ValueError(f"{name} must be > 0 (got {v})")


def crf(r, n):
    """Capital recovery factor r(1+r)^n/((1+r)^n - 1) (annual payment per unit capex); r=0 -> 1/n.
    Typical screening: 10-15%/yr; ledger B implies 0.124/yr; CBR key rate 14% (Sep 2026)."""
    _pos("n", n)
    if r < 0:
        raise ValueError("r >= 0")
    if r == 0:
        return 1.0 / n
    return r * (1 + r) ** n / ((1 + r) ** n - 1)


def annualised_capex(capex, r, n, om_frac=0.0):
    """Annual capital charge + fixed O&M = capex (crf + om_frac)."""
    if capex < 0 or om_frac < 0:
        raise ValueError("capex, om_frac >= 0")
    return capex * (crf(r, n) + om_frac)


def levelised_cost(capex, annual_opex, annual_output, r, n, om_frac=0.0):
    """Levelised cost per unit of output = (capex (crf + om) + opex) / output."""
    _pos("annual_output", annual_output)
    if annual_opex < 0:
        raise ValueError("opex >= 0")
    return (annualised_capex(capex, r, n, om_frac) + annual_opex) / annual_output


def breakeven_volume(fixed_cost, price_or_saving_per_unit, variable_cost_per_unit=0.0):
    """Units per period at which fixed costs are covered: F / (p - v). Raises if p <= v (never breaks even).
    Use for: minimum market (t/yr) for a plant; minimum haul length (km) for a fixed handling cost to beat a
    per-km freight saving (erp2_a: $960/t Ni extra / $0.20 per t-km -> 4,800 km)."""
    margin = price_or_saving_per_unit - variable_cost_per_unit
    if margin <= 0:
        raise ValueError("unit margin <= 0: never breaks even")
    if fixed_cost < 0:
        raise ValueError("fixed cost >= 0")
    return fixed_cost / margin


def carry_forward_cost(cost_now, r, years):
    """Value at the time of use of a cost paid 'years' earlier: cost (1+r)^years (work done ahead,
    pre-stripping, pre-thaw, stockpiles). Source: genius/audit_evo_1 ($0.30/m3 carried 4-9 yr at 10-15%
    -> $0.44-1.06/m3)."""
    if cost_now < 0 or r < 0 or years < 0:
        raise ValueError("inputs >= 0")
    return cost_now * (1 + r) ** years


def delay_pv_factor(r, years):
    """Present-value factor of revenue delayed by 'years': 1/(1+r)^years (3-5 yr at 10-15% -> 0.75-0.50)."""
    if r < 0 or years < 0:
        raise ValueError("inputs >= 0")
    return (1 + r) ** -years


def inventory_carry_cost(value, r, years):
    """Financing cost of goods in transit/storage = value((1+r)^years - 1) (drift pods, multi-year stocks)."""
    return carry_forward_cost(value, r, years) - value


def ratio_vs_baseline(baseline_cost, new_cost):
    """'How many times cheaper' = baseline/new (per the SAME delivered unit: $/oz, $/t Cu, RUB/GJ at the
    boiler). The baseline must be current BEST practice for the same deposit/site, not a straw man."""
    _pos("baseline_cost", baseline_cost)
    _pos("new_cost", new_cost)
    return baseline_cost / new_cost


def ceiling_ratio(removed_share):
    """Upper bound on the chain ratio if a cost share is removed completely: 1/(1-share).
    E.g. outbound logistics 5% of Cu concentrate cost -> 1.05x max; washing 7% -> 1.08x."""
    if not 0 <= removed_share < 1:
        raise ValueError("share in [0,1)")
    return 1.0 / (1.0 - removed_share)


def gate_verdict(margin, ratio):
    """Gate rule used in genius/gate_*: ALIVE if margin >= 1 and ratio >= 1.5; DEAD if margin < 0.3 or
    ratio < 1.1; else WOUNDED. margin = available/required for the killer quantity."""
    if margin < 0.3 or ratio < 1.1:
        return "DEAD"
    if margin >= 1 and ratio >= 1.5:
        return "ALIVE"
    return "WOUNDED"


def cost_per_recovered_unit(cost_per_unit_feed, grade, recovery):
    """Cost per recovered unit = cost per unit feed / (grade x recovery) (e.g. $/m3 -> $/g)."""
    _pos("grade", grade)
    if not 0 < recovery <= 1:
        raise ValueError("recovery in (0,1]")
    return cost_per_unit_feed / (grade * recovery)


def parity_recovery(baseline_recovery, total_cost, fixed_cost, variable_cost_after_change):
    """Recovery a new method needs to match the baseline's cost per recovered unit when it changes the
    variable cost: R_req = R_base * var_new / (C - fixed). fixed = costs per unit product independent of
    recovery (taxes/MET). Source: genius/gate_1 idea 8 (dry vs wet gold recovery)."""
    _pos("total_cost", total_cost)
    if not total_cost > fixed_cost:
        raise ValueError("total_cost must exceed fixed_cost")
    return baseline_recovery * variable_cost_after_change / (total_cost - fixed_cost)


def breakeven_loss_fraction(saving_per_unit, value_per_unit):
    """Fraction of cargo that may be lost before a cheaper-but-lossy route stops paying:
    saving/(value + saving). Source: roast/roast.py (coal $100/t saving $74.6 -> 42.7%; SC6 $900 -> 7.7%)."""
    _pos("saving_per_unit", saving_per_unit)
    _pos("value_per_unit", value_per_unit)
    return saving_per_unit / (value_per_unit + saving_per_unit)


def market_share(output, market):
    """Share of the accessible market an output would need. Arctic Yakutia utility coal ~205 kt/yr (2016)
    for ~68k people (~3 t/person); all Yakutian waterborne communal coal 122 kt (2024)."""
    _pos("market", market)
    if output < 0:
        raise ValueError("output >= 0")
    return output / market


def six_tenths_scaling(cost_ref, capacity_ref, capacity, exponent=0.6):
    """Capex at another scale = cost_ref (cap/cap_ref)^exponent (exponent 0.6-0.7)."""
    _pos("capacity_ref", capacity_ref)
    _pos("capacity", capacity)
    return cost_ref * (capacity / capacity_ref) ** exponent


def season_capacity(rate_per_h, days, hours_per_day=24.0, availability=1.0):
    """Rate x time: quantity achievable in a seasonal window = rate x hours/day x days x availability.
    The single most common killer: compare with the quantity the idea promises."""
    if rate_per_h < 0 or days < 0 or not 0 < hours_per_day <= 24 or not 0 <= availability <= 1:
        raise ValueError("rate, days >= 0; 0 < hours/day <= 24; 0 <= availability <= 1")
    return rate_per_h * hours_per_day * days * availability


def window_margin(window_days, quantity, rate_per_day):
    """available window / required duration (= window x rate / quantity); < 1 means it does not fit."""
    _pos("quantity", quantity)
    _pos("rate_per_day", rate_per_day)
    return window_days * rate_per_day / quantity


def freight_cost(rate_per_tkm, km):
    """Freight per tonne = rate x distance (winter road 20 RUB/t-km [L]; LORP barge 3-5 RUB/t-km)."""
    if rate_per_tkm < 0 or km < 0:
        raise ValueError("inputs >= 0")
    return rate_per_tkm * km


def rub_to_usd(rub, fx=None):
    """Convert RUB to USD at kit.data FX (84 RUB/USD, CBR Oct 2026) unless fx given."""
    fx = fx or data.get("price.fx_rub_usd")
    _pos("fx", fx)
    return rub / fx
