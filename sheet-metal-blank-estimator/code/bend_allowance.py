"""
Bend allowance and developed length calculations.
Methods: K-factor (standard), OSSB (outside setback), DIN 6935 bend deduction.
"""
import math

# Recommended K-factors by material and ir/t ratio
# K-factor: position of neutral axis = K × t from inner surface
# Source: SolidWorks Sheet Metal Guide, Machinery's Handbook

K_DEFAULTS = {
    "soft_al":    {0: 0.33, 1: 0.38, 2: 0.40, 4: 0.42, 8: 0.44},
    "hard_al":    {0: 0.38, 1: 0.41, 2: 0.43, 4: 0.45, 8: 0.46},
    "mild_steel": {0: 0.33, 1: 0.38, 2: 0.42, 4: 0.44, 8: 0.46},
    "stainless":  {0: 0.38, 1: 0.42, 2: 0.44, 4: 0.46, 8: 0.47},
    "copper":     {0: 0.35, 1: 0.40, 2: 0.42, 4: 0.44, 8: 0.45},
}

MATERIAL_K_GROUP = {
    "6061-T6 Al":   "hard_al",
    "5052-H32 Al":  "soft_al",
    "304 SS":       "stainless",
    "316 SS":       "stainless",
    "1018 CRS":     "mild_steel",
    "Galv. Steel":  "mild_steel",
    "Mild Steel HR":"mild_steel",
    "C260 Brass":   "copper",
    "C110 Copper":  "copper",
    "Ti Gr2":       "stainless",
}


def get_k_factor(material, ir_mm, t_mm):
    """
    Interpolate K-factor from table based on ir/t ratio.
    ir = inner bend radius [mm], t = material thickness [mm]
    """
    group = MATERIAL_K_GROUP.get(material, "mild_steel")
    tbl   = K_DEFAULTS[group]
    ratio = ir_mm / t_mm
    keys  = sorted(tbl.keys())
    # Clamp to table range
    if ratio <= keys[0]:  return tbl[keys[0]]
    if ratio >= keys[-1]: return tbl[keys[-1]]
    # Linear interpolation between bracketing entries
    for i in range(len(keys)-1):
        if keys[i] <= ratio <= keys[i+1]:
            lo, hi = keys[i], keys[i+1]
            frac = (ratio - lo) / (hi - lo)
            return tbl[lo] + frac * (tbl[hi] - tbl[lo])
    return 0.42  # fallback


def bend_allowance(bend_angle_deg, ir_mm, t_mm, k=None, material=None):
    """
    Calculate bend allowance (BA) using K-factor method.
    BA = (π/180) × angle × (ir + K × t)

    bend_angle_deg: included/bend angle (e.g., 90 for a 90° bend)
    ir_mm: inner radius
    t_mm: material thickness
    k: explicit K-factor (if None, looks up from material)
    material: material name for K-factor lookup
    Returns BA in mm.
    """
    if k is None:
        k = get_k_factor(material or "mild_steel", ir_mm, t_mm)
    angle_rad = math.radians(bend_angle_deg)
    return angle_rad * (ir_mm + k * t_mm)


def outside_setback(bend_angle_deg, ir_mm, t_mm):
    """
    Outside SetBack (OSSB): distance from bend apex to mold line.
    OSSB = tan(angle/2) × (ir + t)
    """
    half = math.radians(bend_angle_deg / 2)
    return math.tan(half) * (ir_mm + t_mm)


def bend_deduction(bend_angle_deg, ir_mm, t_mm, k=None, material=None):
    """
    Bend Deduction (BD): amount to subtract from total folded flat dimension.
    BD = 2×OSSB − BA
    """
    ba   = bend_allowance(bend_angle_deg, ir_mm, t_mm, k, material)
    ossb = outside_setback(bend_angle_deg, ir_mm, t_mm)
    return 2 * ossb - ba


def developed_length(flat_legs_mm, bends):
    """
    Calculate total developed (flat) length.
    flat_legs_mm: list of flat leg lengths between bends [mm]
    bends: list of dicts with keys: angle, ir, t, material (or k)
    Returns total developed length in mm.
    """
    total = sum(flat_legs_mm)
    for b in bends:
        ba = bend_allowance(
            b["angle"], b["ir"], b["t"],
            k=b.get("k"), material=b.get("material")
        )
        total += ba
    return total
