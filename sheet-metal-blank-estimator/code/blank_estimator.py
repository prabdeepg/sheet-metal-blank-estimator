"""
Sheet Metal Blank Weight Estimator
Prabdeep Singh Ghatora | github.com/prabdeepg

Run: python blank_estimator.py
     python blank_estimator.py --demo
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bend_allowance import bend_allowance, developed_length, get_k_factor
from gauge_table import gauge_to_mm, mm_to_nearest_gauge

# Material: density [g/cm³], cost [$/kg], typical K-group
MATERIALS = {
    "6061-T6 Al":    {"density": 2.70,  "cost_usd_kg": 2.20},
    "5052-H32 Al":   {"density": 2.68,  "cost_usd_kg": 2.40},
    "304 SS":        {"density": 8.00,  "cost_usd_kg": 3.80},
    "316 SS":        {"density": 8.00,  "cost_usd_kg": 5.20},
    "1018 CRS":      {"density": 7.87,  "cost_usd_kg": 1.10},
    "Galv. Steel":   {"density": 7.87,  "cost_usd_kg": 1.30},
    "Mild Steel HR": {"density": 7.85,  "cost_usd_kg": 0.90},
    "C260 Brass":    {"density": 8.53,  "cost_usd_kg": 8.50},
    "C110 Copper":   {"density": 8.94,  "cost_usd_kg": 9.50},
    "Ti Gr2":        {"density": 4.51,  "cost_usd_kg": 28.00},
}


def estimate_blank(material, thickness_mm, folded_l, folded_w,
                   bends_l, bends_w, sheet_l=1000, sheet_w=2000):
    """
    material: string key from MATERIALS
    thickness_mm: sheet thickness
    folded_l, folded_w: outer folded dimensions in L and W directions [mm]
    bends_l: list of bend dicts for length direction [{angle, ir, t, material}]
    bends_w: list of bend dicts for width direction
    sheet_l, sheet_w: stock sheet dimensions [mm]
    """
    mat = MATERIALS[material]
    density = mat["density"]   # g/cm³
    cost_kg  = mat["cost_usd_kg"]

    # Developed dimensions
    # For each direction: developed = folded dim + sum(BA) for bends in that direction
    # (folded dim already includes the mold lines; we just add the bend allowance)
    ba_l = sum(bend_allowance(b["angle"], b["ir"], b.get("t", thickness_mm),
                              material=material) for b in bends_l)
    ba_w = sum(bend_allowance(b["angle"], b["ir"], b.get("t", thickness_mm),
                              material=material) for b in bends_w)

    dev_l = folded_l + ba_l
    dev_w = folded_w + ba_w

    # Blank area and volume
    area_mm2  = dev_l * dev_w
    vol_mm3   = area_mm2 * thickness_mm
    vol_cm3   = vol_mm3 / 1000
    weight_kg = (vol_cm3 * density) / 1000

    # Material cost per part
    cost_part = weight_kg * cost_kg

    # Sheet utilization
    parts_per_sheet_l = int(sheet_l / dev_l)
    parts_per_sheet_w = int(sheet_w / dev_w)
    parts_per_sheet   = parts_per_sheet_l * parts_per_sheet_w
    if parts_per_sheet < 1: parts_per_sheet = 1
    used_area  = parts_per_sheet * area_mm2
    sheet_area = sheet_l * sheet_w
    utilization_pct = (used_area / sheet_area) * 100
    scrap_pct = 100 - utilization_pct

    nearest_ga, nearest_t = mm_to_nearest_gauge(thickness_mm, "USS")
    k = get_k_factor(material, bends_l[0]["ir"] if bends_l else 3.0, thickness_mm)

    return {
        "material": material,
        "thickness_mm": thickness_mm,
        "nearest_gauge": nearest_ga,
        "k_factor": round(k, 3),
        "ba_l_mm": round(ba_l, 3),
        "ba_w_mm": round(ba_w, 3),
        "dev_l_mm": round(dev_l, 2),
        "dev_w_mm": round(dev_w, 2),
        "area_mm2": round(area_mm2, 1),
        "area_cm2": round(area_mm2/100, 2),
        "weight_kg": round(weight_kg, 4),
        "cost_per_part": round(cost_part, 3),
        "parts_per_sheet": parts_per_sheet,
        "utilization_pct": round(utilization_pct, 1),
        "scrap_pct": round(scrap_pct, 1),
    }


def print_result(r, folded_l, folded_w, n_bends_l, n_bends_w):
    print()
    print("══" * 27)
    print("  SHEET METAL BLANK ESTIMATOR")
    print("══" * 27)
    print(f"  Material       : {r['material']}")
    print(f"  Thickness      : {r['thickness_mm']:.3f} mm  (~{r['nearest_gauge']} ga USS)")
    print(f"  K-factor       : {r['k_factor']}")
    print(f"  Part dims      : {folded_l} × {folded_w} mm  (folded)")
    print(f"  Bends          : {n_bends_l} L-dir + {n_bends_w} W-dir")
    print("──" * 27)
    print(f"  BA (L-dir)     : {r['ba_l_mm']:.3f} mm total")
    print(f"  BA (W-dir)     : {r['ba_w_mm']:.3f} mm total")
    print(f"  Developed L    : {r['dev_l_mm']:.2f} mm")
    print(f"  Developed W    : {r['dev_w_mm']:.2f} mm")
    print(f"  Blank Area     : {r['area_mm2']:,.0f} mm²  ({r['area_cm2']} cm²)")
    print(f"  Blank Weight   : {r['weight_kg']:.4f} kg  ({r['weight_kg']*1000:.1f} g)")
    print(f"  Cost/part      : ${r['cost_per_part']:.3f}")
    print(f"  Parts/sheet    : {r['parts_per_sheet']}")
    print(f"  Sheet util.    : {r['utilization_pct']:.1f}%")
    print(f"  Scrap          : {r['scrap_pct']:.1f}%")
    print("══" * 27)
    print()


def demo():
    # Case 1: 304 SS enclosure, 1.626mm (16ga), 200×150mm folded, 2 bends each direction
    t = 1.626
    bends_90 = [{"angle": 90, "ir": 3.2, "t": t, "material": "304 SS"}]
    r = estimate_blank("304 SS", t, 200, 150, bends_90, bends_90)
    print_result(r, 200, 150, len(bends_90), len(bends_90))

    # Case 2: 6061-T6 bracket, 2.032mm (12ga), 100×80mm, 1 bend L-direction
    t2 = 2.032
    b2 = [{"angle": 90, "ir": 4.0, "t": t2, "material": "6061-T6 Al"}]
    r2 = estimate_blank("6061-T6 Al", t2, 100, 80, b2, [])
    print_result(r2, 100, 80, 1, 0)


if __name__ == "__main__":
    if "--demo" in sys.argv or len(sys.argv) == 1:
        demo()
